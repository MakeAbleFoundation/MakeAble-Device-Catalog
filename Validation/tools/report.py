#!/usr/bin/env python3
"""Validate the built files and write the reports.

Stages (run as `report.py <stage> <out-dir>`):
  slice-devices    slice every full-plate file with Orca
  slice-refs       slice each untouched designer reference, for the per-part comparison
  slice-catalogue  slice every plate of the catalogue file
  write            write the per-file markdown, summary.csv and README.md
"""
import csv, json, os, subprocess, sys, tempfile, zipfile
import validate, devices, build

# what the designer's MakerWorld profile says one copy weighs, for a free cross-check
PAGE_WEIGHT = {
    "bag-carrier-medium": 32, "bottle-cap-opener": 22, "bottle-opener-wide-handle": 35,
    "can-opener": 12, "jar-opener": 74, "keywings": 4, "drag-writer": 76,
    "blister-pack-opener": 33, "pill-popper": 9, "flipper-nail-clipper-large": 30,
    "eating-utensil-aid": 45, "shoe-horn": 25, "tube-opener": 17,
}


def data_path(out, name):
    return os.path.join(out, "Validation", "data", name)


def slice_devices(out):
    rows = json.load(open(data_path(out, "build_data.json")))
    res = {}
    for r in rows:
        with tempfile.TemporaryDirectory() as d:
            s = validate.slice_project(r["path"], d)
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
    if dev.get("split"):                     # one object holding the whole kit
        want = Counter({parts[0].name: 1}) if parts else Counter()
        per_unit = {parts[0].name: 1} if parts else {}
    elif dev.get("kit"):
        per_unit = dict(zip(dev["names"], dev["kit"]))
    elif dev.get("names"):
        per_unit = {n: 1 for n in dev["names"]}
    else:                                    # selected by index: all objects are the part
        per_unit = {parts[0].name: 1} if parts else {}
    out = {}
    by_plate = {}
    for p in parts:
        by_plate.setdefault(p.plate, []).append(p.name)
    for plate, names in by_plate.items():
        c = Counter(names)
        if set(c) != set(per_unit):
            continue
        units = min(c[n] // per_unit[n] for n in per_unit)
        leftover = any(c[n] != units * per_unit[n] for n in per_unit)
        if units and not leftover:
            out[plate] = units
    return out


def slice_refs(out):
    res = {}
    for dev in devices.DEVICES:
        if dev.get("stl"):
            continue
        units = ref_units(dev)
        with tempfile.TemporaryDirectory() as d:
            s = validate.slice_project(dev["ref"], d)
        cm3 = {}
        for plate, n in units.items():
            p = (s["plates"] or {}).get(plate) or (s["plates"] or {}).get(str(plate)) or {}
            if p.get("used_cm3") and n:
                cm3[plate] = p["used_cm3"] / n
        res[dev["slug"]] = dict(ref=dev["ref"], units=units, per_unit_cm3=cm3,
                                ok=s["ok"], plates={k: v for k, v in s["plates"].items()})
        best = min(cm3.values()) if cm3 else None
        print(f"  {dev['id']:02d} {dev['title'][:40]:42} ref {'OK ' if s['ok'] else 'FAIL'} "
              f"units {units} -> {best if best is None else round(best, 2)} cm3 per unit")
        json.dump(res, open(data_path(out, "slices_refs.json"), "w"), indent=2)


def slice_catalogue(out):
    """One Orca run per plate: slicing all 31 at once segfaults the slicer, and this way
    a problem on one plate doesn't hide the other thirty."""
    path = os.path.join(out, "Catalogue - one device per plate.3mf")
    rows = _try(data_path(out, "catalogue_data.json"), {}).get("rows", [])
    n_plates = len(rows) or len(devices.DEVICES)
    res = {"plates": {}, "per_plate": {}, "clamped": {}, "ok": True}
    for plate in range(1, n_plates + 1):
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
        json.dump(res, open(data_path(out, "slices_catalogue.json"), "w"), indent=2)


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
            per_plate=f"{r['count']} {r['unit']}", objects=r["objects"],
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
    L.append(f"- reference 3mf: `{os.path.relpath(dev.get('ref', dev.get('stl', ['-'])[0]), '/Users/justinrui/Desktop/M')}`")
    L.append(f"- designer: {dev.get('designer', '-')}")
    L.append(f"- material: {r['material']} ({', '.join(r['filaments'])})")
    L.append(f"- on the plate: {r['count']} {r['unit']} ({r['objects']} objects)")
    L.append("")
    L.append("## Profile")
    pr = r["profile"]
    L.append(f"| preset | layer | first layer | walls | infill | supports | brim | top/bottom |")
    L.append("|---|---|---|---|---|---|---|---|")
    L.append(f"| {pr['preset']} | {pr['layer']} mm | {pr['first_layer']} mm | {pr['walls']} | "
             f"{pr['infill']} {pr['pattern']} | {'on ' + pr['support_type'] if pr['support'] == '1' else 'off'} | "
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
    if info.get("overrides"):
        L.append("### Deliberate changes")
        for k, (a, b) in sorted(info["overrides"].items()):
            L.append(f"- `{k}`: {a} -> **{b}**")
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
    if s.get("warnings"):
        L.append(f"- slicer warnings: {'; '.join(s['warnings'][:4])}")
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
    stage, out = sys.argv[1], sys.argv[2]
    {"slice-devices": slice_devices, "slice-refs": slice_refs,
     "slice-catalogue": slice_catalogue, "write": write}[stage](out)
