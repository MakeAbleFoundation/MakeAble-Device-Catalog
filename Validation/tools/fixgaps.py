#!/usr/bin/env python3
"""Widen part spacing on any plate whose gcode paths conflict.

5 mm between silhouettes is plenty for bare parts, but a brim or tree supports reach
further than the part does, and then neighbouring toolpaths collide - which the slicer
reports as a gcode path conflict. Rather than pad every plate for the worst case (and
throw away parts that fit fine), each plate is sliced, and only the ones that conflict are
rebuilt with more room until they come out clean.
"""
import json, os, sys, tempfile
import build, devices, report, validate


def conflicts(log):
    return "conflict" in (log or "").lower()


def main(out, ladder=(8.0, 10.0, 12.0, 16.0, 22.0)):
    data = {r["slug"]: r for r in json.load(open(f"{out}/Validation/data/build_data.json"))}
    slices = json.load(open(f"{out}/Validation/data/slices_devices.json"))
    outdir = os.path.join(out, "Full Plates")
    previews = os.path.join(out, "Validation", "plate previews")
    by_slug = {d["slug"]: d for d in devices.DEVICES}
    fixed = {}
    for slug, s in slices.items():
        if s.get("ok"):
            continue
        dev = by_slug[slug]
        print(f"  {data[slug]['title']}: slice failed"
              f"{' (gcode path conflict)' if conflicts(s.get('log')) else ''}")
        old_file = report.plate_path(out, data[slug])
        for gap in ladder:
            r = build.build_device(dev, outdir, previews, verbose=False, gap=gap)
            with tempfile.TemporaryDirectory() as d:
                s2 = validate.slice_project(r["path"], d)
            p1 = (s2.get("plates") or {}).get(1, {})
            state = "slices clean" if s2["ok"] else "still conflicts"
            extra = f", {p1.get('total_time', '')} {p1.get('used_g', 0):.0f} g" if s2["ok"] else ""
            print(f"     {gap:.0f} mm spacing -> {r['count']} {r['unit']}, {state}{extra}")
            if s2["ok"]:
                if os.path.exists(old_file) and old_file != r["path"]:
                    os.remove(old_file)
                data[slug] = r
                slices[slug] = s2
                fixed[slug] = gap
                break
            if os.path.exists(r["path"]) and r["path"] != old_file:
                os.remove(r["path"])
    rows = [data[k] for k in sorted(data, key=lambda s: data[s]["id"])]
    json.dump(rows, open(f"{out}/Validation/data/build_data.json", "w"), indent=2)
    json.dump(slices, open(f"{out}/Validation/data/slices_devices.json", "w"), indent=2)
    print(f"\nwidened spacing on {len(fixed)} plate(s): "
          + ", ".join(f"{k} -> {v:.0f} mm" for k, v in fixed.items()))


if __name__ == "__main__":
    main(sys.argv[1])
