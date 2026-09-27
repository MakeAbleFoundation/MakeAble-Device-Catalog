#!/usr/bin/env python3
"""Build one full-plate 3mf per device (and the per-device data the report needs)."""
import datetime, json, os, sys, time
import p3mf, sources, settings, layout, pack, verify, objectcfg, quality, devices

GAP, MARGIN = 5.0, 5.0


def load_parts(dev):
    """Source parts + the reference project used for settings and provenance."""
    if dev.get("stl"):
        ref = p3mf.Ref(settings.SKELETON_3MF)
        if len(dev["stl"]) == 1:
            parts = [sources.from_stl(dev["stl"][0], dev["title"])]
        else:
            # a kit of loose STLs: one name per file, so parts can be told apart
            names = dev.get("stl_names") or [os.path.splitext(os.path.basename(p))[0]
                                             for p in dev["stl"]]
            parts = [sources.from_stl(p, n) for p, n in zip(dev["stl"], names)]
        return ref, with_part_overrides(dev, parts)
    ref = p3mf.Ref(dev["ref"])
    _mref, parts = sources.from_ref(dev.get("mesh_ref", dev["ref"]),
                                    names=dev.get("names"), indices=dev.get("indices"),
                                    objects=dev.get("objects"))
    if dev.get("split"):
        parts = sources.split_shells(parts[0], names=dev["split"])
    if dev.get("kit") and dev.get("names"):
        # a kit names each distinct part once; the reference may already hold several
        # copies of it (the clothes-button 3mf ships two scales and two pins)
        seen, uniq = set(), []
        for p in parts:
            if p.name not in seen:
                seen.add(p.name)
                uniq.append(p)
        parts = uniq
    for p, name in zip(parts, dev.get("rename") or []):
        p.name = name
    if dev.get("flatten_bottom"):
        for p in parts:
            moved, dz = sources.flatten_bottom(p)
            if not moved:
                raise RuntimeError(f"{dev['slug']}: flatten_bottom found nothing to fix")
    return ref, with_part_overrides(dev, parts)


def with_part_overrides(dev, parts):
    """Per-part settings the designer asked for (a brim on the screw only, supports on one
    part of a kit). Appended after the reference's own per-object values, because the last
    entry wins when they are baked onto the object."""
    ov = dev.get("part_overrides") or {}
    unknown = set(ov) - {p.name for p in parts}
    if unknown:
        raise KeyError(f"{dev['slug']}: part_overrides for unknown parts {sorted(unknown)}")
    for p in parts:
        for k, v in (ov.get(p.name) or {}).items():
            if k not in objectcfg.OBJECT_SCOPED:
                raise KeyError(f"{dev['slug']}: {k} cannot be set per object")
            p.ms_meta = list(p.ms_meta) + [(k, str(v))]
    return parts


def effective_cfg(cfg, part):
    """The settings a part actually prints with: the device profile plus its own
    per-object values."""
    eff = dict(cfg)
    for k, v in part.ms_meta:
        if k in objectcfg.OBJECT_SCOPED:
            eff[k] = v
    return eff


def device_settings(dev, ref):
    ref_settings = {} if dev.get("stl") else ref.settings
    preset = ref_settings.get("print_settings_id", "0.20mm Standard @BBL X1C")
    inh = ref_settings.get("inherits_group")
    fil = [devices.FILAMENT[dev["material"]]]
    return settings.build(ref_settings, preset, inh[0] if inh else None, fil,
                          overrides=dev.get("overrides"),
                          process_from="0.20mm Standard @BBL X1C" if dev.get("stl") else None)


def prepare(parts, cfg, extruder="1"):
    for p in parts:
        p.ms_meta = objectcfg.bake(cfg, p.ms_meta)
        p.extruder = extruder
    return parts


def drop_exclusion_hits(placements):
    """Remove any placement whose convex hull reaches the printer's excluded corner -
    the slicer refuses the whole plate over one such part."""
    import math
    import numpy as np
    keep = []
    for pl in placements:
        t = math.radians(pl.theta)
        R = np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])
        pts = pl.part.verts[:, :2] @ R.T + np.array([pl.x, pl.y])
        if not verify.hull_hits_exclusion(pts):
            keep.append(pl)
    return keep


def trim_to_whole_kits(placements, parts, ratio):
    """After dropping parts, keep only complete kits - half a kit is scrap."""
    want = {p.key: r for p, r in zip(parts, ratio)}
    have = {}
    for pl in placements:
        have.setdefault(pl.part.key, []).append(pl)
    kits = min((len(have.get(k, [])) // r) for k, r in want.items()) if want else 0
    keep = []
    for k, r in want.items():
        keep += have.get(k, [])[:kits * r]
    order = {id(pl): i for i, pl in enumerate(placements)}
    keep.sort(key=lambda pl: order[id(pl)])
    return keep, kits


def placement_centre(pl):
    import math
    import numpy as np
    t = math.radians(pl.theta)
    R = np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])
    pts = pl.part.verts[:, :2] @ R.T + np.array([pl.x, pl.y])
    return (pts.min(axis=0) + pts.max(axis=0)) / 2


def apply_cap(placements, parts, ratio, units):
    """Keep `units` copies (or whole kits) - the ones nearest the middle of the plate, so a
    plate trimmed for print time stays one compact, centred group."""
    import numpy as np
    mid = np.array([pack.BED / 2, pack.BED / 2])
    dist = {id(pl): float(np.hypot(*(placement_centre(pl) - mid))) for pl in placements}
    if ratio:
        keep = []
        for p, r in zip(parts, ratio):
            mine = [pl for pl in placements if pl.part.key == p.key]
            keep += sorted(mine, key=lambda pl: dist[id(pl)])[:r * units]
    else:
        keep = sorted(placements, key=lambda pl: dist[id(pl)])[:units]
    order = {id(pl): i for i, pl in enumerate(placements)}
    keep.sort(key=lambda pl: order[id(pl)])
    return keep


def designer_layout(dev, parts):
    """The designer's own arrangement of one unit, taken from their plate and centred on
    ours. For parts the packer cannot fit inside the margins (the bedside box lies
    diagonally across the whole bed) this is the layout that is known to print."""
    import math
    import numpy as np
    ref = p3mf.Ref(dev["ref"])
    want = {p.name for p in parts}
    plate = dev.get("layout_plate", 1)
    src = [p for p in ref.parts() if p.plate == plate and p.name in want]
    placements = []
    for sp in src:
        canon = next(p for p in parts if p.name == sp.name)
        if selfcheck_norm(sp.mesh_bytes) != selfcheck_norm(canon.mesh_bytes):
            raise RuntimeError(f"{dev['slug']}: {sp.name} copies do not share a mesh")
        Mc = np.array(canon.base_lin, dtype=float).reshape(3, 3)
        Ms = np.array(sp.base_lin, dtype=float).reshape(3, 3)
        Rz = np.linalg.solve(Mc, Ms)             # Ms = Mc . Rz (row-vector convention)
        th = math.degrees(math.atan2(Rz[0, 1], Rz[0, 0]))
        if (not np.allclose(Rz, np.array(p3mf.rot_z(th)).reshape(3, 3), atol=1e-4)
                or abs(sp.base_z - canon.base_z) > 1e-3):
            raise RuntimeError(f"{dev['slug']}: {sp.name} is not a turn of the same part")
        placements.append(p3mf.Placement(part=canon, theta=th, x=sp.base_xy[0],
                                         y=sp.base_xy[1]))
    pts = []
    for pl in placements:
        t = math.radians(pl.theta)
        R = np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])
        pts.append(pl.part.verts[:, :2] @ R.T + np.array([pl.x, pl.y]))
    pts = np.vstack(pts)
    dx = pack.BED / 2 - (pts[:, 0].min() + pts[:, 0].max()) / 2
    dy = pack.BED / 2 - (pts[:, 1].min() + pts[:, 1].max()) / 2
    for pl in placements:
        pl.x += dx
        pl.y += dy
    return placements


def selfcheck_norm(b):
    import re
    return re.sub(rb'<object id="\d+"', b'<object id="X"', b, count=1)


def summarise(values):
    """One value for a device whose parts may print differently."""
    vals = sorted(set(values), key=lambda v: (len(v), v))
    return vals[0] if len(vals) == 1 else "/".join(vals)


def profile_summary(cfg, parts, info):
    """The headline settings, as the parts actually print: a per-object value the designer
    set (5 walls on one part, supports on another) counts, not just the device profile."""
    eff = [effective_cfg(cfg, p) for p in parts]
    one = lambda k: [objectcfg.one(e[k]) for e in eff]
    sup = one("enable_support")
    return dict(preset=info["target_preset"],
                layer=summarise(one("layer_height")),
                first_layer=objectcfg.one(cfg["initial_layer_print_height"]),
                walls=summarise(one("wall_loops")),
                infill=summarise(one("sparse_infill_density")),
                pattern=summarise(one("sparse_infill_pattern")),
                support="1" if all(v == "1" for v in sup) else ("some" if "1" in sup else "0"),
                support_type=summarise([objectcfg.one(e["support_type"])
                                        for e in eff if objectcfg.one(e["enable_support"]) == "1"]
                                       or one("support_type")),
                brim=summarise(one("brim_type")),
                top=summarise(one("top_shell_layers")),
                bottom=summarise(one("bottom_shell_layers")))


def device_advisories(dev, cfg, parts):
    """quality.advise per part. In a kit whose supports are there for one part (the cup of
    the cup holder), 'supports on but nothing to support' on the other parts is noise."""
    import quality
    advisories, metrics = [], {}
    needs = {}
    for p in parts:
        adv, met = quality.advise(p, effective_cfg(cfg, p), z_offset=p.base_z)
        needs[p.name] = met["overhang"]["area"] > 60
        advisories.append((p, adv))
        metrics[p.name] = met
    out = []
    for p, adv in advisories:
        for a in adv:
            if (dev.get("kit") and a.startswith("supports are on")
                    and any(v for k, v in needs.items() if k != p.name)):
                continue
            out.append(f"{p.name}: {a}")
    return out, metrics


def build_device(dev, outdir, previews=None, verbose=True, gap=None, cap=None):
    t0 = time.time()
    gap = gap or dev.get("gap") or GAP
    cap = cap if cap is not None else dev.get("cap")
    margin = dev.get("margin", MARGIN)
    ref, parts = load_parts(dev)
    cfg, info = device_settings(dev, ref)
    advisories, metrics = device_advisories(dev, cfg, parts)
    if not dev.get("stl"):
        # a pause or colour change on the designer's plate would have to be carried too
        for p in parts:
            if ref.custom_gcode_layers(p.plate):
                raise RuntimeError(f"{dev['slug']}: plate {p.plate} has custom gcode")
    prepare(parts, cfg)

    def lay_out():
        if dev.get("kit"):
            pls, kits, how = layout.plan_kit_best(parts, dev["kit"], gap=gap,
                                                  margin=margin, verbose=False,
                                                  by_size=dev.get("kit_by_size", False))
        else:
            pls, how = layout.plan_single_best(parts[0], gap=gap, margin=margin,
                                               verbose=False)
            kits = len(pls)
        before = len(pls)
        pls = drop_exclusion_hits(pls)
        if dev.get("kit"):
            pls, kits = trim_to_whole_kits(pls, parts, dev["kit"])
        else:
            kits = len(pls)
        return pls, kits, how, before - len(pls)

    placements, count, how, dropped = lay_out()
    if dropped:
        # a part reached into the excluded corner and had to go; try again with the
        # packer keeping further clear of it, and keep whichever plate holds more
        pack.set_exclusion_clearance(30.0)
        try:
            alt_pl, alt_count, alt_how, _ = lay_out()
        finally:
            pack.set_exclusion_clearance(pack.EXCLUDE_CLEARANCE)
        if alt_count > count:
            placements, count, how = alt_pl, alt_count, alt_how + " (corner kept clear)"
    if dev.get("keep_layout"):
        own = designer_layout(dev, parts)
        own_count = (trim_to_whole_kits(own, parts, dev["kit"])[1] if dev.get("kit")
                     else len(own))
        if own_count > count:
            placements, count, how = own, own_count, "designer's own arrangement, centred"
    capped_from = None
    if cap and count > cap:
        placements = apply_cap(placements, parts, dev.get("kit"), cap)
        capped_from, count = count, cap
        how += f" (capped from {capped_from} for print time)"
    unit = "kits" if dev.get("kit") else "copies"
    rep, issues = verify.layout_report(placements, gap=gap, margin=margin)
    name = f"{dev['id']:02d} {dev['title']} - {dev['material']} x{count}.3mf".replace("/", "-")
    path = os.path.join(outdir, name)
    today = datetime.date.today().isoformat()
    p3mf.write_project(path, placements, cfg, ref,
                       meta_override={"Title": dev["title"],
                                      "Designer": dev.get("designer", ""),
                                      "Application": "BambuStudio-" + settings.STUDIO_VERSION,
                                      "ModificationDate": today, "CreationDate": today},
                       plate_names={1: dev["title"]}, keep_aux=not dev.get("stl"),
                       strip_design_meta=bool(dev.get("stl")))
    if previews:
        os.makedirs(previews, exist_ok=True)
        verify.preview(placements, os.path.join(previews, f"{dev['id']:02d} {dev['slug']}.png"))
    if verbose:
        print(f"  {dev['id']:02d} {dev['title'][:44]:46} {count:3} {unit:6} "
              f"{os.path.getsize(path)/1e6:5.1f} MB {time.time()-t0:5.1f}s  [{how}]"
              + ("  ISSUES" if issues else ""))
    return dict(slug=dev["slug"], id=dev["id"], title=dev["title"], path=path, layout=how,
                file=os.path.basename(path), material=dev["material"], count=count,
                unit=unit, objects=len(placements), issues=issues, bbox=rep,
                gap=gap, info={k: v for k, v in info.items() if k != "filaments"},
                **({"capped_from": capped_from, "margin": margin}
                   if (capped_from or margin != MARGIN) else {}),
                filaments=info["filaments"], advisories=advisories, metrics=metrics,
                parts=[p.name for p in parts],
                profile=profile_summary(cfg, parts, info))


def main():
    out = sys.argv[1]
    only = sys.argv[2:] or None
    outdir = os.path.join(out, "Full Plates")
    previews = os.path.join(out, "Validation", "plate previews")
    os.makedirs(outdir, exist_ok=True)
    results = [build_device(d, outdir, previews) for d in devices.DEVICES
               if not only or d["slug"] in only]
    js = os.path.join(out, "Validation", "data", "build_data.json")
    if only and os.path.exists(js):
        old = {r["slug"]: r for r in json.load(open(js))}
        old.update({r["slug"]: r for r in results})
        results = [old[k] for k in sorted(old, key=lambda s: old[s]["id"])]
    json.dump(results, open(js, "w"), indent=2)
    print(f"\n{len(results)} devices -> {outdir}")


if __name__ == "__main__":
    main()
