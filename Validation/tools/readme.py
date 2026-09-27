#!/usr/bin/env python3
"""Write the folder's README.md from the build + validation data."""
import json, os, sys
import devices

EXCLUDED = [
    ("Other/EyeDropperAid.3mf", "MakeAble 'Eye Dropper Squeezer Aid' - a different model "
     "from the Printables Eye Drop Assist on the list"),
    ("Other/jar-opener+(1).3mf", "MakeAble 'Jar/Pop Bottle and Can Assist' - not the "
     "OPENSESAME3000 jar tool"),
    ("Other/4+in+1+button+aid,+key+turner,+zipper+aid,+handle.3mf",
     "MakeAble 4-in-1 aid - not the Clothes Button & Zipper Hook helper"),
    ("Other/Bottle_Opener_30.stl + .gcode", "a third bottle opener, sliced for a Prusa MK3S"),
    ("Toothbrush Grip (PLA)/toothbrush.STL", "the flat MyMiniFactory toothbrush, not the "
     "round arthritis grip you picked"),
    ("Walking Stick Holder/", "not on the catalogue list"),
    ("Other/DRAG+v2.3mf", "byte-identical copy of the DRAG folder's 3mf"),
    ("Other/Tube_Opener.3mf", "plain mesh export with no settings in it"),
    ("Aug*.3mf, Combined*.3mf, Bag_Carrier_x4.3mf", "earlier working files, not designer sources"),
    ("Clothes Button .../*.stl (loose)", "the loose STLs differ from the 3mf: its pins are "
     "scaled to 95% and its hook carries painted seams"),
]


def fmt(v, dash="-"):
    return dash if v in (None, "", 0) else v


def main(out):
    rows = json.load(open(f"{out}/Validation/data/build_data.json"))
    refs = json.load(open(f"{out}/Validation/data/slices_refs.json"))
    sl = json.load(open(f"{out}/Validation/data/slices_devices.json"))
    cat = json.load(open(f"{out}/Validation/data/catalogue_data.json"))
    csl = json.load(open(f"{out}/Validation/data/slices_catalogue.json"))
    chk = json.load(open(f"{out}/Validation/data/selfcheck.json"))
    by_slug = {d["slug"]: d for d in devices.DEVICES}

    L = ["# MakeAble assistive devices - print files for the Bambu Lab P1S", ""]
    L.append("Every file here is set up for a **Bambu Lab P1S, 0.4 nozzle, textured PEI "
             "plate**, saved in Bambu Studio 2.2.2 format. Open one, check the plate, hit "
             "slice. Nothing needs to be re-arranged or re-configured.")
    L.append("")
    L.append("- `Full Plates/` - one file per device, filled with as many copies as fit.")
    L.append("- `Catalogue - one device per plate.3mf` - every device on its own plate, "
             "one copy each, same settings.")
    L.append("- `Validation/` - what was checked, per file, plus plate previews.")
    L.append("")
    L.append("## Full plates")
    L.append("")
    L.append("| # | file | material | per plate | print time | filament | layer | walls | infill | supports | vs designer's file |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        s = sl.get(r["slug"], {})
        p1 = (s.get("plates") or {}).get("1") or (s.get("plates") or {}).get(1) or {}
        pr = r["profile"]
        rs = refs.get(r["slug"]) or {}
        per_unit = (p1.get("used_cm3", 0) / r["count"]) if r["count"] else 0
        ref_per = min((rs.get("per_unit_cm3") or {}).values(), default=None)
        match = f"{100 * per_unit / ref_per:.0f}%" if (ref_per and per_unit) else "-"
        L.append(f"| {r['id']:02d} | {r['file']} | {r['material']} | {r['count']} "
                 f"{r['unit']} | {fmt(p1.get('total_time'))} | "
                 f"{fmt(round(p1.get('used_g', 0), 0))} g | {pr['layer']} mm | "
                 f"{pr['walls']} | {pr['infill']} | "
                 f"{'yes' if pr['support'] == '1' else 'no'} | {match} |")
    L.append("")
    tot_g = sum((((sl.get(r['slug'], {}).get('plates') or {}).get('1')
                   or (sl.get(r['slug'], {}).get('plates') or {}).get(1) or {})).get('used_g', 0)
                for r in rows)
    L.append(f"All {len(rows)} plates together: about {tot_g/1000:.1f} kg of filament.")
    L.append("")
    L.append("The last column is the check that matters: filament per copy on your plate "
             "against a slice of the designer's own untouched file. 100% means the part "
             "comes out exactly as they set it up. The few at 95-96% are the P1S's "
             "elephant-foot compensation shaving the first layer, which their printer "
             "profile did not apply. A dash means there is nothing to compare against "
             "(loose STLs, or a size variant that shares another file's profile).")
    L.append("")
    L.append("## Catalogue file")
    L.append("")
    L.append("`Catalogue - one device per plate.3mf` holds "
             f"{len(cat['rows'])} plates, one device each, in the same order as the table "
             "above. Each plate keeps its own layer height, wall count, infill and support "
             "settings - those are baked onto the objects, so switching the process preset "
             "in Studio will not silently wipe them.")
    L.append("")
    L.append("Filament slot 1 is PLA, slot 2 is PETG, and every plate uses one or the "
             "other, so you only ever load one spool per plate.")
    L.append("")
    L.append("Three settings cannot vary per plate in Bambu Studio, so the file uses the "
             "most conservative value any device asked for:")
    L.append("")
    L.append("| setting | catalogue | who wanted something else |")
    L.append("|---|---|---|")
    L.append("| first layer height | 0.2 mm | Bottle Cap Opener's profile uses 0.15 mm |")
    L.append("| first layer speed | 15 mm/s | the slowest any designer asked for (DRAG); "
             "others use 20-50 mm/s |")
    L.append("| first layer infill speed | 50 mm/s | slowest of the set |")
    L.append("")
    L.append("If you want a device exactly as its designer set it up, use its file in "
             "`Full Plates/` - those keep every value.")
    L.append("")
    L.append("## Spacing, and the corner the printer cannot use")
    L.append("")
    L.append("Parts sit at least 5 mm apart, measured on their real outlines rather than "
             "bounding boxes, which is what lets the C-shaped ones nest into each other. "
             "Where a profile adds a brim or supports, those reach past the part itself, "
             "so the plate is sliced and the spacing widened until the slicer stops "
             "reporting conflicting toolpaths:")
    L.append("")
    for r in rows:
        if r.get("gap", 5) != 5:
            L.append(f"- **{r['title']}**: {r['gap']:.0f} mm apart - its tree supports "
                     f"flare out well past the part.")
    L.append("")
    L.append("The P1S cannot print in an 18 x 28 mm patch at the front-left corner "
             "(Bambu calls it the bed exclusion area). Parts are kept 8 mm clear of it, "
             "and any part whose convex hull would still reach into it is dropped - the "
             "slicer refuses the whole plate over a single one.")
    L.append("")
    L.append("## How the settings were decided")
    L.append("")
    L.append("For each device, in order:")
    L.append("")
    L.append("1. **Machine settings** always come from the P1S system preset. Nothing from "
             "the designer's printer (A1 mini, H2S, P2S) is carried over - no start/end "
             "gcode, no bed shape, no kinematics.")
    L.append("2. **Filament** is your own preset: `PETG P1S Tuned` for PETG, "
             "`Bambu PLA Basic @BBL X1C` for PLA.")
    L.append("3. **Speeds, accelerations and elephant-foot compensation** follow the P1S "
             "preset, *unless* the designer had deliberately changed that value on their "
             "own printer - then their number wins.")
    L.append("4. **Everything else** - walls, infill, shells, supports, brim, seams, line "
             "widths - is the designer's own value from their 3mf.")
    L.append("5. Anything changed on purpose beyond that is listed per file in "
             "`Validation/per file/`.")
    L.append("")
    L.append("## How they were checked")
    L.append("")
    L.append("Bambu Studio's command-line slicer crashes on macOS (a known upstream bug), "
             "so slicing checks were run with OrcaSlicer 2.4.2, which reads the same "
             "project format. Per file:")
    L.append("")
    L.append("- the plate slices with no errors, and the time and filament are recorded;")
    L.append("- filament per copy is compared against a slice of the designer's untouched "
             "file, and against the weight quoted on the model page;")
    L.append("- every part is inside the plate, clear of the P1S's excluded front-left "
             "corner, with at least 5 mm between parts (checked on the real outlines, not "
             "bounding boxes);")
    L.append("- meshes are byte-identical to the designer's, so painted seams survive;")
    L.append("- each object carries its settings, and every object is on a plate.")
    L.append("")
    probs = sum(len(v["problems"]) for v in chk.values())
    L.append(f"Structural checks: {len(chk)} files, {probs} problems. "
             + ("All clean." if not probs else "See Validation/selfcheck.json."))
    L.append("")
    adv = [(r, a) for r in rows for a in r["advisories"]]
    if adv:
        L.append("## Worth knowing (nothing was changed)")
        L.append("")
        for r, a in adv:
            L.append(f"- **{r['title']}**: {a}")
        L.append("")
    L.append("## Where each file came from")
    L.append("")
    L.append("| # | device | source file in this folder | model page |")
    L.append("|---|---|---|---|")
    for r in rows:
        d = by_slug[r["slug"]]
        src = d.get("ref") or (d.get("stl") or ["-"])[0]
        src = os.path.relpath(src, "/Users/justinrui/Desktop/M")
        link = f"[page]({d['link']})" if d.get("link") else "-"
        L.append(f"| {r['id']:02d} | {r['title']} | `{src}` | {link} |")
    L.append("")
    L.append("Each MakerWorld link's profile id was matched against the `DesignProfileId` "
             "stored inside the local 3mf, so these are the exact profiles that were linked.")
    L.append("")
    L.append("## Look-alikes that were left out")
    L.append("")
    for f, why in EXCLUDED:
        L.append(f"- `{f}` - {why}")
    L.append("")
    L.append("## Still open")
    L.append("")
    L.append("- **Eye Drop Assist (files 23-31)**: the three Printables pages sit behind a "
             "bot check, so the designer's own print settings could not be read. Those "
             "files use the P1S 0.20 mm Standard profile in PLA. They also need a decision: "
             "whether a pliers and an eyepiece pair up into one device (in which case they "
             "should be kit plates) or are alternatives.")
    L.append("")
    open(f"{out}/README.md", "w").write("\n".join(L) + "\n")
    print(f"wrote {out}/README.md")


if __name__ == "__main__":
    main(sys.argv[1])
