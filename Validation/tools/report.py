#!/usr/bin/env python3
"""Validate the built files and write the reports.

Stages (run as `report.py <stage> <out-dir> [...]`):
  slice-devices [slug ...]     slice full-plate files with Orca (default: all), merged into
                               the existing results
  slice-refs [slug ...]        slice untouched designer references, for the per-part comparison
  slice-catalogue <n> [plate]  slice the plates of catalogue n, one at a time
  write                        write the per-file markdown and summary.csv
"""
import csv, json, os, subprocess, sys, tempfile, zipfile
import validate, devices, build

# what the designer's MakerWorld profile says one copy weighs, for a free cross-check
PAGE_WEIGHT = {
    "bag-carrier-medium": 32, "bottle-cap-opener": 22, "bottle-opener-wide-handle": 35,
    "can-opener": 12, "jar-opener": 74, "keywings": 4, "drag-writer": 76,
    "blister-pack-opener": 33, "pill-popper": 9, "flipper-nail-clipper-large": 30,
    "eating-utensil-aid": 45, "shoe-horn": 25, "tube-opener": 17,
    # batch 2 (per copy or per kit, from the linked profile)
    "bedside-box": 223, "toothpaste-squeezer-gear": 42, "chopstick-helper": 4,
    "soup-can-opener": 13, "jar-opener-vacuum": 22, "younger-grip": 33, "plug-puller": 10,
    "pinky-saver": 9, "cup-holder": 200, "hand-press-light": 39, "hand-press-medium": 45,
    "hand-press-hard": 49, "boot-jack": 141,
}

MESH_FIXES = {
    "flatten_bottom": "four mesh vertices forming a 0.36 mm spike under the flat base were "
                      "moved up onto the base; the part stood on the spike, its first layer "
                      "was empty and the slicer refused it (the designer's own file fails the "
                      "same way in OrcaSlicer)",
}

DESKTOP_M = "/Users/justinrui/Desktop/M"


def plate_path(out, r):
    """Where a full-plate file lives now (stored absolute paths go stale when the folder
    moves; the file name does not)."""
    return os.path.join(out, "Full Plates", r["file"])


def source_label(path):
    """A designer source file, relative to wherever it is kept."""
    for root in (DESKTOP_M, devices.REPO):
        if os.path.abspath(path).startswith(root + os.sep):
            return os.path.relpath(path, root)
    return os.path.basename(path)


def _load(path):
    return _try(path, {})


def unit_word(r, n=None):
    n = r["count"] if n is None else n
    return r["unit"][:-1] if n == 1 else r["unit"]


def refresh(out):
    """Recompute each device's profile summary and advisories from devices.py without
    re-packing its plate (the summary reads what every part actually prints with)."""
    import build
    js = data_path(out, "build_data.json")
    rows = json.load(open(js))
    by_slug = {d["slug"]: d for d in devices.DEVICES}
    for r in rows:
        dev = by_slug[r["slug"]]
        ref, parts = build.load_parts(dev)
        cfg, info = build.device_settings(dev, ref)
        r["profile"] = build.profile_summary(cfg, parts, info)
        r["advisories"], r["metrics"] = build.device_advisories(dev, cfg, parts)
    json.dump(rows, open(js, "w"), indent=2)
    print(f"refreshed {len(rows)} rows")


def data_path(out, name):
    return os.path.join(out, "Validation", "data", name)


def slice_devices(out, slugs=None):
    rows = json.load(open(data_path(out, "build_data.json")))
    res = _load(data_path(out, "slices_devices.json"))
    for r in rows:
        if slugs and r["slug"] not in slugs:
            continue
        with tempfile.TemporaryDirectory() as d:
            s = validate.slice_project(plate_path(out, r), d)
        res[r["slug"]] = s
        p = s["plates"].get(1, {})
        print(f"  {r['id']:02d} {r['title'][:40]:42} {'OK ' if s['ok'] else 'FAIL'} "
              f"{p.get('total_time', '-'):>12} {p.get('used_g', 0):7.1f} g "
              f"{p.get('used_cm3', 0):7.1f} cm3")
        json.dump(res, open(data_path(out, "slices_devices.json"), "w"), indent=2)


def ref_units(dev):
    """How many of OUR units (copies or kits) sit on each plate of the designer's file,
    and whether that plate holds anything else. Only a plate that holds exactly our parts
    can be used for the per-part comparison."""
    import p3mf
    from collections import Counter
    ref = p3mf.Ref(dev["ref"])
    parts = ref.parts()
    # parts are told apart by name, or by object id where names collide
    ident = ((lambda p: p.key.rsplit("::", 1)[1]) if dev.get("objects")
             else (lambda p: p.name))
    if dev.get("split"):                     # one object holding the whole kit
        per_unit = {parts[0].name: 1} if parts else {}
    elif dev.get("objects"):
        per_unit = dict(zip((str(o) for o in dev["objects"]),
                            dev.get("kit") or [1] * len(dev["objects"])))
    elif dev.get("kit"):
        per_unit = dict(zip(dev["names"], dev["kit"]))
    elif dev.get("names"):
        per_unit = {n: 1 for n in dev["names"]}
    else:                                    # selected by index: all objects are the part
        per_unit = {parts[0].name: 1} if parts else {}
    out = {}
    by_plate = {}
    for p in parts:
        by_plate.setdefault(p.plate, []).append(ident(p))
    for plate, names in by_plate.items():
        c = Counter(names)
        if set(c) != set(per_unit):
            continue
        units = min(c[n] // per_unit[n] for n in per_unit)
        leftover = any(c[n] != units * per_unit[n] for n in per_unit)
        if units and not leftover:
            out[plate] = units
    if not out and len(per_unit) > 1:
        # a kit the designer spread over several plates (one plate per part): those plates
        # together are one comparison unit, provided they hold nothing else
        plates = sorted(pl for pl, ids in by_plate.items() if set(ids) <= set(per_unit))
        c = Counter(i for pl in plates for i in by_plate[pl])
        if set(c) == set(per_unit):
            units = min(c[n] // per_unit[n] for n in per_unit)
            if units and all(c[n] == units * per_unit[n] for n in per_unit):
                out["+".join(str(pl) for pl in plates)] = units
    return out


def slice_refs(out, slugs=None):
    res = _load(data_path(out, "slices_refs.json"))
    cache = {}
    for dev in devices.DEVICES:
        if dev.get("stl") or (slugs and dev["slug"] not in slugs):
            continue
        units = ref_units(dev)
        needed = sorted({int(x) for k in units for x in str(k).split("+")})
        # slice only the plates the comparison needs (a reference can carry a heavy
        # multicolour plate that has nothing to do with this device)
        which = needed[0] if len(needed) == 1 else 0
        if (dev["ref"], which) not in cache:
            with tempfile.TemporaryDirectory() as d:
                cache[(dev["ref"], which)] = validate.slice_project(dev["ref"], d, plate=which)
        s = cache[(dev["ref"], which)]
        cm3 = {}
        for plate, n in units.items():
            used = 0.0
            for x in str(plate).split("+"):
                p = (s["plates"] or {}).get(int(x)) or (s["plates"] or {}).get(x) or {}
                used = used + p["used_cm3"] if (p.get("used_cm3") and used is not None) else None
            if used and n:
                cm3[plate] = used / n
        res[dev["slug"]] = dict(ref=dev["ref"], units=units, per_unit_cm3=cm3,
                                ok=s["ok"], plates={k: v for k, v in s["plates"].items()})
        best = min(cm3.values()) if cm3 else None
        print(f"  {dev['id']:02d} {dev['title'][:40]:42} ref {'OK ' if s['ok'] else 'FAIL'} "
              f"units {units} -> {best if best is None else round(best, 2)} cm3 per unit")
        json.dump(res, open(data_path(out, "slices_refs.json"), "w"), indent=2)


def slice_catalogue(out, n=1, only=None):
    """One Orca run per plate: slicing all 30 at once segfaults the slicer, and this way
    a problem on one plate doesn't hide the others."""
    cat = devices.CATALOGUES[int(n)]
    path = os.path.join(out, cat["file"])
    rows = _try(data_path(out, cat["data"]), {}).get("rows", [])
    n_plates = len(rows) or len(cat["ids"])
    res = _load(data_path(out, cat["slices"])) if only else {}
    res = {"plates": {int(k): v for k, v in (res.get("plates") or {}).items()},
           "per_plate": {int(k): v for k, v in (res.get("per_plate") or {}).items()},
           "clamped": res.get("clamped", {}), "ok": True}
    for plate in range(1, n_plates + 1):
        if only and plate not in only:
            continue
        with tempfile.TemporaryDirectory() as d:
            s = validate.slice_project(path, d, plate=plate, timeout=3600)
        res["clamped"] = s["clamped"]
        p = (s.get("plates") or {}).get(plate) or {}
        res["plates"][plate] = p
        res["per_plate"][plate] = dict(ok=s["ok"], warnings=s["warnings"][:4])
        res["ok"] = res["ok"] and s["ok"]
        title = rows[plate - 1]["title"] if plate <= len(rows) else f"plate {plate}"
        print(f"  plate {plate:2} {title[:40]:42} {'OK ' if s['ok'] else 'FAIL'} "
              f"{p.get('total_time','-'):>12} {p.get('used_g',0):7.1f} g")
        res["ok"] = all(v["ok"] for v in res["per_plate"].values())
        json.dump(res, open(data_path(out, cat["slices"]), "w"), indent=2)


def write(out):
    rows = json.load(open(data_path(out, "build_data.json")))
    dslice = json.load(open(data_path(out, "slices_devices.json")))
    rslice = _try(data_path(out, "slices_refs.json"), {})
    cat = _try(data_path(out, "catalogue_data.json"), {})
    cslice = _try(data_path(out, "slices_catalogue.json"), {})
    by_slug = {d["slug"]: d for d in devices.DEVICES}

    summary = []
    for r in rows:
        dev = by_slug[r["slug"]]
        s = dslice.get(r["slug"], {})
        p1 = (s.get("plates") or {}).get("1") or (s.get("plates") or {}).get(1) or {}
        per = None
        if p1.get("used_cm3") and r["count"]:
            per = p1["used_cm3"] / r["count"]
        ref_per = None
        rs = rslice.get(r["slug"])
        if rs and rs.get("per_unit_cm3"):
            ref_per = min(rs["per_unit_cm3"].values())
        summary.append(dict(
            id=r["id"], file=r["file"], device=r["title"], material=r["material"],
            per_plate=f"{r['count']} {unit_word(r)}", objects=r["objects"],
            print_time=p1.get("total_time", ""), grams=round(p1.get("used_g", 0), 1),
            cm3=round(p1.get("used_cm3", 0), 1),
            cm3_per_unit=round(per, 2) if per else "",
            reference_cm3_per_unit=round(ref_per, 2) if ref_per else "",
            match=("-" if not (per and ref_per)
                   else f"{100*per/ref_per:.0f}%"),
            page_grams=PAGE_WEIGHT.get(r["slug"], ""),
            layer=r["profile"]["layer"], walls=r["profile"]["walls"],
            infill=r["profile"]["infill"], supports=r["profile"]["support"],
            brim=r["profile"]["brim"], preset=r["profile"]["preset"],
            slice_ok=s.get("ok", False), geometry_issues=len(r["issues"]),
            advisories=len(r["advisories"])))
        _write_device_md(out, r, dev, s, rs, per, ref_per)

    with open(os.path.join(out, "Validation", "summary.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        w.writeheader()
        w.writerows(summary)
    print(f"wrote {os.path.join(out, 'Validation', 'summary.csv')} ({len(summary)} rows)")
    return summary, cat, cslice


def _try(path, default):
    try:
        return json.load(open(path))
    except Exception:
        return default


def _write_device_md(out, r, dev, s, rs, per, ref_per):
    d = os.path.join(out, "Validation", "per file")
    os.makedirs(d, exist_ok=True)
    p1 = (s.get("plates") or {}).get("1") or (s.get("plates") or {}).get(1) or {}
    L = [f"# {r['id']:02d} {r['title']}", ""]
    L.append(f"- file: `Full Plates/{r['file']}`")
    if dev.get("link"):
        L.append(f"- source: {dev['link']}")
    if len(dev.get("stl") or []) > 1:
        L.append("- source files: " + ", ".join(f"`{source_label(x)}`" for x in dev["stl"]))
    else:
        L.append(f"- reference 3mf: `{source_label(dev.get('ref', dev.get('stl', ['-'])[0]))}`")
    L.append(f"- designer: {dev.get('designer', '-')}")
    if dev.get("license"):
        L.append(f"- license: {dev['license']}")
    L.append(f"- material: {r['material']} ({', '.join(r['filaments'])})")
    L.append(f"- on the plate: {r['count']} {unit_word(r)} ({r['objects']} objects)")
    if r.get("capped_from"):
        L.append(f"- print-time cap: {r['capped_from']} {r['unit']} fit on the plate; trimmed "
                 f"to {r['count']} to stay under {devices.MAX_HOURS:.0f} h")
    if dev.get("hardware"):
        L.append(f"- also needed: {dev['hardware']}")
    L.append("")
    L.append("## Profile")
    pr = r["profile"]
    L.append(f"| preset | layer | first layer | walls | infill | supports | brim | top/bottom |")
    L.append("|---|---|---|---|---|---|---|---|")
    sup = {"1": "on " + pr["support_type"], "some": "some parts, " + pr["support_type"]}
    L.append(f"| {pr['preset']} | {pr['layer']} mm | {pr['first_layer']} mm | {pr['walls']} | "
             f"{pr['infill']} {pr['pattern']} | {sup.get(pr['support'], 'off')} | "
             f"{pr['brim']} | {pr['top']}/{pr['bottom']} |")
    L.append("")
    info = r["info"]
    if info.get("from_reference"):
        L.append("### Taken from the designer's file")
        L.append("| setting | P1S preset | designer |")
        L.append("|---|---|---|")
        for k, (a, b) in sorted(info["from_reference"].items()):
            L.append(f"| `{k}` | {a} | **{b}** |")
        L.append("")
    if info.get("kept_p1s"):
        L.append("### Left at the P1S value (designer never changed it on their printer)")
        L.append("| setting | their file | P1S |")
        L.append("|---|---|---|")
        for k, (a, b) in sorted(info["kept_p1s"].items()):
            if str(a) != str(b):
                L.append(f"| `{k}` | {a} | **{b}** |")
        L.append("")
    fixes = [MESH_FIXES[k] for k in MESH_FIXES if dev.get(k)]
    if info.get("overrides") or fixes:
        L.append("### Deliberate changes")
        for k, (a, b) in sorted(info["overrides"].items()):
            L.append(f"- `{k}`: {a} -> **{b}**")
        for f in fixes:
            L.append(f"- mesh: {f}")
        L.append("")
    if dev.get("part_overrides"):
        L.append("### Per-part settings")
        for part, kv in dev["part_overrides"].items():
            L.append(f"- {part}: " + ", ".join(f"`{k}` = **{v}**" for k, v in kv.items()))
        L.append("")
    L.append("## Validation")
    L.append(f"- Orca slice: {'passed' if s.get('ok') else 'FAILED'}"
             + (f" - {p1.get('total_time')}, {p1.get('used_g', 0):.1f} g, "
                f"{p1.get('used_cm3', 0):.1f} cm3" if p1 else ""))
    if per:
        L.append(f"- per {r['unit'][:-1]}: {per:.2f} cm3")
    if ref_per and per:
        L.append(f"- the designer's own file slices at {ref_per:.2f} cm3 per copy "
                 f"({100 * per / ref_per:.0f}% of that here)")
    elif ref_per:
        L.append(f"- the designer's own file slices at {ref_per:.2f} cm3 per copy")
    if PAGE_WEIGHT.get(r["slug"]):
        L.append(f"- the model page quotes {PAGE_WEIGHT[r['slug']]} g per copy")
    L.append(f"- geometry check: {'clean' if not r['issues'] else 'ISSUES'}")
    for i in r["issues"]:
        L.append(f"  - {i}")
    if s.get("clamped"):
        L.append(f"- clamped for Orca only (the delivered file keeps Bambu's values): "
                 f"{', '.join(s['clamped'])}")
    warnings = [w for w in s.get("warnings") or [] if not validate.BENIGN.search(w)]
    if warnings:
        L.append(f"- slicer warnings: {'; '.join(warnings[:4])}")
    L.append("")
    if r["advisories"]:
        L.append("## Advisories (nothing changed)")
        for a in r["advisories"]:
            L.append(f"- {a}")
        L.append("")
    if dev.get("notes"):
        L.append("## Notes")
        for n in dev["notes"]:
            L.append(f"- {n}")
        L.append("")
    open(os.path.join(d, f"{r['id']:02d} {r['slug']}.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    stage, out, rest = sys.argv[1], sys.argv[2], sys.argv[3:]
    if stage == "slice-devices":
        slice_devices(out, rest or None)
    elif stage == "slice-refs":
        slice_refs(out, rest or None)
    elif stage == "slice-catalogue":
        slice_catalogue(out, int(rest[0]) if rest else 1,
                        [int(x) for x in rest[1:]] or None)
    elif stage == "write":
        write(out)
    elif stage == "refresh":
        refresh(out)
    else:
        raise SystemExit(f"unknown stage {stage}")
