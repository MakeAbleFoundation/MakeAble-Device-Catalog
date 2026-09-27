#!/usr/bin/env python3
"""One project, one device per plate - each plate keeping its own settings.

Print-level settings can't vary per plate, so the shared profile takes the most
conservative value any device asked for; everything that can be object-scoped (layer
height, walls, infill, supports, brim, line widths, region speeds) is baked onto the
objects themselves.
"""
import datetime, json, math, os, sys
from collections import Counter
import numpy as np
import p3mf, settings, layout, pack, verify, objectcfg, devices, build

GAP, MARGIN = 5.0, 5.0

# Studio lays plates out on a grid: stride = plate size * 1.2, columns = ~sqrt(count)
# (PartPlate.cpp: LOGICAL_PART_PLATE_GAP = 1/5, compute_colum_count). Objects have to sit
# at their plate's origin in that grid, or they all pile onto plate 1 in the 3D view.
STRIDE = pack.BED * 1.2


def grid_columns(count):
    v = math.sqrt(count)
    r = round(v)
    return int(r + 1) if v > r else int(r)

# the slowest first layer any designer in the catalogue asked for (DRAG: 15 mm/s); the
# first-layer height stays at the 0.2 mm everything but the Bottle Cap Opener uses
SHARED = {
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": ["15"],
    "initial_layer_infill_speed": ["50"],
}


def num(v):
    return f"{v:g}"


def shared_for(cfgs):
    """The same three print-level values, worked out for another set of devices: the
    first-layer height most of them use, and the slowest first layer any of them asked for."""
    heights = Counter(objectcfg.one(c["initial_layer_print_height"]) for c in cfgs)
    return {
        "initial_layer_print_height": heights.most_common(1)[0][0],
        "initial_layer_speed": [num(min(float(objectcfg.one(c["initial_layer_speed"]))
                                        for c in cfgs))],
        "initial_layer_infill_speed": [num(min(float(objectcfg.one(c["initial_layer_infill_speed"]))
                                               for c in cfgs))],
    }


def center(placements):
    """Shift a group of placements so it sits in the middle of the plate."""
    xs, ys = [], []
    for pl in placements:
        t = math.radians(pl.theta)
        R = np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])
        pts = pl.part.verts[:, :2] @ R.T + np.array([pl.x, pl.y])
        xs += [pts[:, 0].min(), pts[:, 0].max()]
        ys += [pts[:, 1].min(), pts[:, 1].max()]
    dx = pack.BED / 2 - (min(xs) + max(xs)) / 2
    dy = pack.BED / 2 - (min(ys) + max(ys)) / 2
    for pl in placements:
        pl.x += dx
        pl.y += dy
    return placements


def main(out_path, n=1, previews=None):
    fil = [devices.FILAMENT["PLA"], devices.FILAMENT["PETG"]]
    base_ref = p3mf.Ref(settings.SKELETON_3MF)
    devs = [d for d in devices.DEVICES if d["id"] in devices.CATALOGUES[n]["ids"]]

    placements, plate_names, rows, by_plate, cfgs = [], {}, [], {}, []
    for plate, dev in enumerate(devs, start=1):
        ref, parts = build.load_parts(dev)
        dcfg, info = build.device_settings(dev, ref)
        cfgs.append(dcfg)
        build.prepare(parts, dcfg, extruder="1" if dev["material"] == "PLA" else "2")
        margin = dev.get("margin", MARGIN)
        gap = dev.get("gap") or GAP       # brims and supports need what the full plate got
        if dev.get("keep_layout"):
            pls = build.designer_layout(dev, parts)
        elif dev.get("kit"):
            pls, _kits = layout.plan_kit(parts, dev["kit"], gap=gap, margin=margin,
                                         max_kits=1, verbose=False)
        else:
            mi = layout.masks_for(parts[0], [0], gap)
            bed = pack.Bed(margin=margin, gap=gap)
            pos = layout.bl_positions(bed, mi[0]["raw"], limit=1)
            pls = [layout.place(bed, parts[0], 0, mi[0], *pos[0])] if pos else []
        if not pls:
            # an empty plate would otherwise go out without a word
            raise RuntimeError(f"plate {plate}: {dev['title']} does not fit on the plate")
        for pl in pls:
            pl.plate = plate
        center(pls)
        placements += pls
        by_plate[plate] = pls
        plate_names[plate] = f"{dev['id']:02d} {dev['title']}"
        rows.append(dict(plate=plate, slug=dev["slug"], title=dev["title"],
                         material=dev["material"], objects=len(pls),
                         layer=objectcfg.one(dcfg["layer_height"]),
                         walls=objectcfg.one(dcfg["wall_loops"]),
                         infill=objectcfg.one(dcfg["sparse_infill_density"]),
                         support=objectcfg.one(dcfg["enable_support"]),
                         device_first_layer=objectcfg.one(dcfg["initial_layer_print_height"]),
                         device_first_layer_speed=objectcfg.one(dcfg["initial_layer_speed"]),
                         device_first_layer_infill_speed=objectcfg.one(
                             dcfg["initial_layer_infill_speed"])))
        print(f"  plate {plate:2}  {dev['title'][:46]:48} {len(pls)} object(s)")

    shared = SHARED if n == 1 else shared_for(cfgs)
    cfg, _ = settings.build({}, "0.20mm Standard @BBL X1C", None, fil, overrides=shared)
    cols = grid_columns(len(rows))
    for plate, pls in by_plate.items():
        col, row = (plate - 1) % cols, (plate - 1) // cols
        for pl in pls:
            pl.x += col * STRIDE
            pl.y -= row * STRIDE

    today = datetime.date.today().isoformat()
    p3mf.write_project(out_path, placements, cfg, base_ref,
                       meta_override={"Title": "MakeAble assistive devices - one per plate"
                                      + ("" if n == 1 else f" ({n})"),
                                      "Designer": "MakeAble",
                                      "Application": "BambuStudio-" + settings.STUDIO_VERSION,
                                      "ModificationDate": today, "CreationDate": today},
                       plate_names=plate_names, keep_aux=False, strip_design_meta=True)
    # check each plate in its own coordinates
    local = []
    for plate, pls in by_plate.items():
        col, row = (plate - 1) % cols, (plate - 1) // cols
        for pl in pls:
            local.append(p3mf.Placement(part=pl.part, theta=pl.theta, plate=plate,
                                        x=pl.x - col * STRIDE, y=pl.y + row * STRIDE))
    issues = []
    for plate, pls in by_plate.items():
        dev = devs[plate - 1]
        mine = [pl for pl in local if pl.plate == plate]
        _rep, iss = verify.layout_report(mine, gap=(dev.get("gap") or GAP)
                                         if not dev.get("keep_layout") else 0.5,
                                         margin=dev.get("margin", MARGIN))
        issues += iss
    print(f"\nwrote {out_path} ({os.path.getsize(out_path)/1e6:.1f} MB), "
          f"{len(rows)} plates, issues: {issues or 'none'}")
    return rows, issues, shared


if __name__ == "__main__":
    out = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    cat = devices.CATALOGUES[n]
    rows, issues, shared = main(os.path.join(out, cat["file"]), n)
    json.dump(dict(rows=rows, issues=issues, shared=shared),
              open(os.path.join(out, "Validation", "data", cat["data"]), "w"), indent=2)
