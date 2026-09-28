#!/usr/bin/env python3
"""Make each plate slice clean and finish inside the print-time cap.

One loop per device: slice the plate; if neighbouring toolpaths conflict (a brim or supports
reach further than the part does), widen the spacing; if the plate runs longer than
devices.MAX_HOURS, keep fewer copies - the ones nearest the middle of the plate - and slice
again. The spacing and cap that come out are printed so they can be written into
devices.py, which is what makes a later rebuild reproduce the delivered file.
"""
import json, math, os, re, sys, tempfile
import build, devices, report, validate

LADDER = (8.0, 10.0, 12.0, 16.0, 22.0)


def hours(t):
    """Orca's '16h 7m 18s' (or '1d 2h 3m 4s') in hours."""
    unit = {"d": 24.0, "h": 1.0, "m": 1 / 60, "s": 1 / 3600}
    return sum(int(v) * unit[u] for v, u in re.findall(r"(\d+)\s*([dhms])", t or ""))


def save(js, sjs, r, s):
    """Merge one device's result into the shared data files. Several fitplate runs may
    work through different devices at once, so re-read under a lock and touch only this
    device's entries."""
    import fcntl
    with open(js + ".lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        data = {x["slug"]: x for x in json.load(open(js))}
        data[r["slug"]] = r
        rows = [data[k] for k in sorted(data, key=lambda k: data[k]["id"])]
        json.dump(rows, open(js, "w"), indent=2)
        slices = report._load(sjs)
        slices[r["slug"]] = s
        json.dump(slices, open(sjs, "w"), indent=2)


def fit(out, slugs):
    js = report.data_path(out, "build_data.json")
    sjs = report.data_path(out, "slices_devices.json")
    data = {r["slug"]: r for r in json.load(open(js))}
    slices = report._load(sjs)
    by_slug = {d["slug"]: d for d in devices.DEVICES}
    outdir = os.path.join(out, "Full Plates")
    previews = os.path.join(out, "Validation", "plate previews")
    summary = {}
    for slug in slugs:
        dev = by_slug[slug]
        r = data.get(slug)
        gap = (r or {}).get("gap") or dev.get("gap") or build.GAP
        cap = dev.get("cap")
        if r is None:
            r = build.build_device(dev, outdir, previews, verbose=False, gap=gap, cap=cap)
        print(f"  {dev['id']:02d} {dev['title']}", flush=True)
        while True:
            with tempfile.TemporaryDirectory() as d:
                s = validate.slice_project(report.plate_path(out, r), d)
            p1 = s["plates"].get(1, {})
            t = hours(p1.get("total_time"))
            print(f"     {r['count']:3} {r['unit']:6} "
                  + ("as supplied" if dev.get("supplied") else f"gap {gap:4.1f} mm") + " -> "
                  + (f"{p1.get('total_time')}, {p1.get('used_g', 0):.0f} g" if s["ok"]
                     else "FAILED" + (" (gcode path conflict)" if s.get("conflict")
                                      else f": {s['warnings'][:2]}")), flush=True)
            if dev.get("supplied"):
                # delivered as arranged: report a problem, never re-space or trim it
                if not s["ok"]:
                    print("     supplied plate does not slice - fix it in Bambu Studio",
                          flush=True)
                elif t > devices.MAX_HOURS:
                    print(f"     supplied plate runs over {devices.MAX_HOURS:.0f} h - fix it in "
                          "Bambu Studio", flush=True)
                break
            if not s["ok"]:
                wider = [g for g in LADDER if g > gap]
                if not s.get("conflict") or not wider:
                    break
                gap = wider[0]
            elif t > devices.MAX_HOURS:
                cap = max(1, min(r["count"] - 1, math.floor(r["count"] * devices.MAX_HOURS / t)))
            else:
                break
            new = build.build_device(dev, outdir, previews, verbose=False, gap=gap, cap=cap)
            if new["file"] != r["file"] and os.path.exists(report.plate_path(out, r)):
                os.remove(report.plate_path(out, r))
            r = new
        save(js, sjs, r, s)
        summary[slug] = dict(ok=s["ok"] and t <= devices.MAX_HOURS, count=r["count"], gap=gap,
                             cap=r["count"] if r.get("capped_from") else None,
                             time=(s["plates"].get(1) or {}).get("total_time"))
    print("\nfor devices.py:")
    for slug, v in summary.items():
        extra = []
        if v["gap"] != build.GAP:
            extra.append(f"gap={v['gap']}")
        if v["cap"]:
            extra.append(f"cap={v['cap']}")
        print(f"  {slug:28} {'OK  ' if v['ok'] else 'FAIL'} {v['count']:3}  {v['time']}  "
              + (", ".join(extra) or "-"))
    return summary


if __name__ == "__main__":
    fit(sys.argv[1], sys.argv[2:])
