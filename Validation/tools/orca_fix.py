#!/usr/bin/env python3
"""Copy a Bambu 3mf, clamping the few values OrcaSlicer's validator rejects.

Only used to make validation slices possible; the delivered files keep Bambu's values.
Each clamp is recorded so the report can say what differed from the real profile.
"""
import json, os, sys, zipfile

CLAMPS = {
    "tree_support_wall_count": lambda v: "0" if str(v) == "-1" else v,   # -1 = auto in Bambu
    "raft_first_layer_expansion": lambda v: "2" if float(v) < 0 else v,  # no raft anywhere
}


def fix(src, dst):
    changed = {}
    zin = zipfile.ZipFile(src)
    cfg = json.loads(zin.read("Metadata/project_settings.config"))
    for k, f in CLAMPS.items():
        if k not in cfg:
            continue
        old = cfg[k]
        new = [f(v) for v in old] if isinstance(old, list) else f(old)
        if new != old:
            cfg[k] = new
            changed[k] = (old, new)
    os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zout:
        for n in zin.namelist():
            data = zin.read(n)
            if n == "Metadata/project_settings.config":
                data = json.dumps(cfg, indent=4, ensure_ascii=False).encode()
            zout.writestr(n, data)
    return changed


if __name__ == "__main__":
    print(fix(sys.argv[1], sys.argv[2]))
