#!/usr/bin/env python3
"""Slice a project with OrcaSlicer and report what came out.

Bambu Studio's own CLI segfaults on macOS (upstream bug #8569), so the independent check
is Orca, which reads the same project format.
"""
import json, os, re, subprocess, sys, tempfile
from orca_fix import fix

ORCA = "/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer"
TIME_RE = re.compile(r"model printing time: ([^;]+); total estimated time: (.+)")


def parse_gcode(path):
    out, head = {}, []
    with open(path, "r", errors="replace") as f:
        for i, line in enumerate(f):
            head.append(line)
            if i > 60:
                break
    for line in head:
        m = TIME_RE.search(line)
        if m:
            out["model_time"], out["total_time"] = m.group(1).strip(), m.group(2).strip()
        for key, tag in (("layers", "total layer number:"), ("max_z", "max_z_height:"),
                         ("density", "filament_density:")):
            if tag in line:
                out[key] = line.split(":", 1)[1].strip()
    tail = subprocess.run(["tail", "-c", "300000", path], capture_output=True,
                          text=True).stdout
    for key, tag in (("used_mm", "filament used [mm]"), ("used_cm3", "filament used [cm3]"),
                     ("used_g", "filament used [g]")):
        # multi-filament projects report one value per slot: "0,0,9.53,0"
        m = re.search(re.escape(tag) + r"\s*=\s*([\d.,\s]+)", tail)
        if m:
            vals = [float(x) for x in m.group(1).replace(" ", "").split(",") if x not in ("", ".")]
            out[key] = round(sum(vals), 3)
    return out


def slice_project(path, workdir, plate=0, timeout=3600):
    os.makedirs(workdir, exist_ok=True)
    fixed = os.path.join(workdir, "fixed.3mf")
    clamped = fix(path, fixed)
    # designer files saved by a newer Studio than Orca 2.4.2 are gated unless allowed
    cmd = [ORCA, "--slice", str(plate), "--allow-newer-file",
           "--outputdir", workdir, fixed]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    log = (p.stdout or "") + (p.stderr or "")
    plates = {}
    for g in sorted(f for f in os.listdir(workdir) if f.endswith(".gcode")):
        n = int(re.search(r"plate_(\d+)", g).group(1)) if "plate_" in g else 1
        plates[n] = parse_gcode(os.path.join(workdir, g))
    warn = [l.strip() for l in log.splitlines()
            if re.search(r"error|invalid|not in range|failed|exceed|conflict|outside", l, re.I)
            and "no error" not in l.lower()]
    return dict(ok=p.returncode == 0 and bool(plates), returncode=p.returncode,
                clamped=clamped, plates=plates, warnings=warn[:12], log=log[-4000:])


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as d:
        r = slice_project(sys.argv[1], d, int(sys.argv[2]) if len(sys.argv) > 2 else 0)
    print(json.dumps({k: v for k, v in r.items() if k != "log"}, indent=2)[:4000])
