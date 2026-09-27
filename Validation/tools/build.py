#!/usr/bin/env python3
"""Build one full-plate 3mf per device (and the per-device data the report needs)."""
import datetime, json, os, sys, time
import p3mf, sources, settings, layout, pack, verify, objectcfg, quality, devices

GAP, MARGIN = 5.0, 5.0


def load_parts(dev):
    """Source parts + the reference project used for settings and provenance."""
    if dev.get("stl"):
        ref = p3mf.Ref(settings.SKELETON_3MF)
        return ref, [sources.from_stl(p, dev["title"]) for p in dev["stl"]]
    ref = p3mf.Ref(dev["ref"])
    _mref, parts = sources.from_ref(dev.get("mesh_ref", dev["ref"]),
                                    names=dev.get("names"), indices=dev.get("indices"))
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
    return ref, parts


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


def build_device(dev, outdir, previews=None, verbose=True, gap=None):
    t0 = time.time()
    gap = gap or dev.get("gap") or GAP
    ref, parts = load_parts(dev)
    cfg, info = device_settings(dev, ref)
    advisories, metrics = [], {}
    for p in parts:
        adv, met = quality.advise(p, cfg, z_offset=p.base_z)
        advisories += [f"{p.name}: {a}" for a in adv]
        metrics[p.name] = met
    prepare(parts, cfg)

    def lay_out():
        if dev.get("kit"):
            pls, kits, how = layout.plan_kit_best(parts, dev["kit"], gap=gap,
                                                  margin=MARGIN, verbose=False)
        else:
            pls, how = layout.plan_single_best(parts[0], gap=gap, margin=MARGIN,
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
    unit = "kits" if dev.get("kit") else "copies"
    rep, issues = verify.layout_report(placements, gap=gap, margin=MARGIN)
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
                filaments=info["filaments"], advisories=advisories, metrics=metrics,
                parts=[p.name for p in parts],
                profile=dict(preset=info["target_preset"],
                             layer=objectcfg.one(cfg["layer_height"]),
                             first_layer=objectcfg.one(cfg["initial_layer_print_height"]),
                             walls=objectcfg.one(cfg["wall_loops"]),
                             infill=objectcfg.one(cfg["sparse_infill_density"]),
                             pattern=objectcfg.one(cfg["sparse_infill_pattern"]),
                             support=objectcfg.one(cfg["enable_support"]),
                             support_type=objectcfg.one(cfg["support_type"]),
                             brim=objectcfg.one(cfg["brim_type"]),
                             top=objectcfg.one(cfg["top_shell_layers"]),
                             bottom=objectcfg.one(cfg["bottom_shell_layers"])))


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
