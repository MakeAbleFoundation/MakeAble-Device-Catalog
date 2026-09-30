#!/usr/bin/env python3
"""Structural checks on the delivered files: what's inside them, not how they slice.

Confirms the meshes are the designer's own bytes (only the object id is rewritten),
the printer and filament are what they should be, every object carries its baked
settings, and every object is assigned to a plate.
"""
import json, os, re, sys, zipfile
import xml.etree.ElementTree as ET
import p3mf, devices, build, objectcfg, report

CORE = p3mf.CORE
NS = p3mf.NS


def norm_id(b):
    """Blank out the object id: it is deliberately renumbered when parts are combined."""
    return re.sub(rb'<object id="\d+"', b'<object id="X"', b, count=1)


def mesh_bodies(zf):
    return {n: norm_id(zf.read(n)) for n in zf.namelist() if n.startswith("3D/Objects/")}


EXTRAS = (("layer_heights", p3mf.LAYER_HEIGHTS), ("layer_ranges", p3mf.LAYER_RANGES),
          ("brim_ears", p3mf.BRIM_EARS))


def extras_problems(z, parts_by_name):
    """Every copy of a part whose reference carried a variable layer height, height-range
    modifiers or brim-ear points must still carry them, at the right object index."""
    root = ET.fromstring(z.read("3D/3dmodel.model"))
    ms = ET.fromstring(z.read("Metadata/model_settings.config"))
    name_of = {o.get("id"): next((m.get("value") for m in o.findall("metadata")
                                  if m.get("key") == "name"), "") for o in ms.findall("object")}
    order = [it.get("objectid") for it in root.find("m:build", NS).findall("m:item", NS)]
    problems = []
    for attr, fname in EXTRAS:
        want = {i for i, oid in enumerate(order, 1)
                if getattr(parts_by_name.get(name_of.get(oid)), attr, None)}
        got = set()
        if fname in z.namelist():
            text = z.read(fname).decode()
            got = {int(x) for x in re.findall(r'object_id=(\d+)\|', text)}
            got |= {int(x) for x in re.findall(r'<object id="(\d+)">', text)}
        if want != got:
            problems.append(f"{fname}: expected entries for objects {sorted(want)}, "
                            f"file has {sorted(got)}")
    if p3mf.CUSTOM_GCODE in z.namelist() and b"<layer" in z.read(p3mf.CUSTOM_GCODE):
        problems.append("carries custom gcode (pause / colour change)")
    return problems


def check(path, dev, parts_by_name=None):
    z = zipfile.ZipFile(path)
    problems, notes = [], []
    need = ["[Content_Types].xml", "_rels/.rels", "3D/3dmodel.model",
            "3D/_rels/3dmodel.model.rels", "Metadata/project_settings.config",
            "Metadata/model_settings.config"]
    for n in need:
        if n not in z.namelist():
            problems.append(f"missing {n}")
    cfg = json.loads(z.read("Metadata/project_settings.config"))
    if cfg.get("printer_settings_id") != "Bambu Lab P1S 0.4 nozzle":
        problems.append(f"printer is {cfg.get('printer_settings_id')}")
    if cfg.get("printable_area") != ["0x0", "256x0", "256x256", "0x256"]:
        problems.append(f"printable area is {cfg.get('printable_area')}")
    want_fil = devices.FILAMENT[dev["material"]] if dev else None
    if want_fil and want_fil not in cfg.get("filament_settings_id", []):
        problems.append(f"filament is {cfg.get('filament_settings_id')}, expected {want_fil}")
    if str(cfg.get("enable_prime_tower")) not in ("0", "['0']"):
        # a supplied plate may keep Studio's spare filament slots; what counts is how many
        # its objects and parts actually print with
        used = {m.get("value") for m in
                ET.fromstring(z.read("Metadata/model_settings.config")).iter("metadata")
                if m.get("key") == "extruder"}
        if dev and dev.get("supplied") and len(used) == 1:
            # Studio's default, kept as saved: with one filament the slicer never builds one
            notes.append("prime tower setting left on as saved (one filament, none is printed)")
        else:
            problems.append("prime tower is on with a single filament")
    if cfg.get("curr_bed_type") != "Textured PEI Plate":
        problems.append(f"build plate is {cfg.get('curr_bed_type')}")

    root = ET.fromstring(z.read("3D/3dmodel.model"))
    items = root.find("m:build", NS).findall("m:item", NS)
    objs = root.find("m:resources", NS).findall("m:object", NS)
    ms = ET.fromstring(z.read("Metadata/model_settings.config"))
    ms_objs = ms.findall("object")
    in_plates = [m.get("value") for pl in ms.findall("plate")
                 for mi in pl.findall("model_instance")
                 for m in mi.findall("metadata") if m.get("key") == "object_id"]
    if dev and dev.get("supplied"):
        # arranged by hand in Studio (copies share one object, settings are the project's):
        # what matters is that it is exactly the file that was handed over
        with open(path, "rb") as a, open(dev["ref"], "rb") as b:
            if a.read() != b.read():
                problems.append(f"differs from the supplied file {os.path.basename(dev['ref'])}")
            else:
                notes.append("supplied plate, byte-identical to the file handed over")
    else:
        if not (len(items) == len(objs) == len(ms_objs) == len(in_plates)):
            problems.append(f"object counts disagree: build {len(items)}, resources "
                            f"{len(objs)}, settings {len(ms_objs)}, plate instances "
                            f"{len(in_plates)}")
        for o in ms_objs:
            keys = {m.get("key") for m in o.findall("metadata")}
            if "extruder" not in keys:
                problems.append(f"object {o.get('id')} has no extruder")
            baked = keys & set(objectcfg.OBJECT_SCOPED)
            if len(baked) < 20:
                problems.append(f"object {o.get('id')} only has {len(baked)} baked settings")
    for rel in ("_rels/.rels", "3D/_rels/3dmodel.model.rels"):
        for t in re.findall(r'Target="([^"]+)"', z.read(rel).decode()):
            if t.lstrip("/") not in z.namelist():
                problems.append(f"{rel} points at missing {t}")

    if parts_by_name is None and dev:
        parts_by_name = {p.name: p for p in build.load_parts(dev)[1]}
    if parts_by_name is not None:
        problems += extras_problems(z, parts_by_name)

    # split kits and loose STLs are rebuilt, so check the geometry survived instead
    if dev and (dev.get("stl") or dev.get("split")):
        import numpy as np
        want_tris = 0
        if dev.get("split"):
            src = zipfile.ZipFile(dev["ref"])
            for n in src.namelist():
                if n.startswith("3D/Objects/"):
                    want_tris += src.read(n).count(b"<triangle ")
        else:
            import sources
            want_tris = sum(len(sources.from_stl(p).tris) for p in dev["stl"])
        got = {}
        for n in z.namelist():
            if n.startswith("3D/Objects/"):
                got[n] = z.read(n).count(b"<triangle ")
        if sum(got.values()) != want_tris:
            problems.append(f"triangle count changed: source {want_tris}, file "
                            f"{sum(got.values())}")
        else:
            notes.append(f"geometry intact ({want_tris} triangles)")

    # meshes must be the designer's own bytes, not a re-export. Compare against the
    # payloads taken from the reference for THIS device (some references keep their
    # meshes inside 3dmodel.model, so there is nothing under 3D/Objects/ to compare to).
    if dev and not dev.get("stl") and not dev.get("split"):
        _ref, parts = build.load_parts(dev)
        src = {norm_id(p.mesh_bytes) for p in parts}
        for n, b in mesh_bodies(z).items():
            # Studio saves an empty placeholder per copy when copies share one mesh
            if b not in src and b"<mesh>" in b:
                problems.append(f"{n} does not match the designer's mesh bytes")
        painted_src = any(b"paint_" in p.mesh_bytes for p in parts)
        painted_out = any(b"paint_" in b for b in mesh_bodies(z).values())
        if painted_src and painted_out:
            notes.append("painted seam/support data preserved")
        elif painted_src and not painted_out:
            problems.append("reference had painted faces, output does not")

    return problems, notes


if __name__ == "__main__":
    out = sys.argv[1]
    rows = json.load(open(f"{out}/Validation/data/build_data.json"))
    by_slug = {d["slug"]: d for d in devices.DEVICES}
    bad = 0
    res = {}
    for r in rows:
        p, n = check(report.plate_path(out, r), by_slug[r["slug"]])
        res[r["slug"]] = dict(problems=p, notes=n)
        bad += len(p)
        print(f"  {r['id']:02d} {r['title'][:44]:46} {'clean' if not p else 'PROBLEM'}"
              + ("  " + "; ".join(n) if n else ""))
        for x in p:
            print(f"       - {x}")
    import os
    # the folder must hold exactly the files the build data describes - a plate rebuilt
    # with a different count gets a new name, and the old file must not linger
    have = {f for f in os.listdir(f"{out}/Full Plates") if f.endswith(".3mf")}
    listed = {r["file"] for r in rows}
    if have != listed:
        p = ([f"not in the build data: {f}" for f in sorted(have - listed)]
             + [f"missing: {f}" for f in sorted(listed - have)])
        res["_folder"] = dict(problems=p, notes=[])
        print("  Full Plates folder: PROBLEM")
        for x in p:
            print(f"       - {x}")
        bad += len(p)
    for n, c in devices.CATALOGUES.items():
        cat = f"{out}/{c['file']}"
        if not os.path.exists(cat):
            continue
        parts = {}
        for d in devices.DEVICES:
            if d["id"] in c["ids"]:
                parts.update({p.name: p for p in build.load_parts(d)[1]})
        p, notes = check(cat, None, parts)
        res["_catalogue" if n == 1 else f"_catalogue{n}"] = dict(problems=p, notes=notes)
        print(f"  catalogue {n}: {'clean' if not p else 'PROBLEM'}")
        for x in p:
            print(f"       - {x}")
        bad += len(p)
    json.dump(res, open(f"{out}/Validation/data/selfcheck.json", "w"), indent=2)
    print(f"\n{bad} problem(s)")
