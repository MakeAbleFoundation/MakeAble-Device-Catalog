#!/usr/bin/env python3
"""Checks of my own, on top of whatever the designer's profile says.

Nothing here changes a file: it produces advisories for the report, so a support setting
or a missing brim stays the user's decision, with numbers in front of them.
"""
import numpy as np


def _normals(V, T):
    a, b, c = V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]
    n = np.cross(b - a, c - a)
    length = np.linalg.norm(n, axis=1)
    area = length / 2
    unit = np.zeros_like(n)
    nz = length > 1e-12
    unit[nz] = n[nz] / length[nz][:, None]
    return unit, area, (a + b + c) / 3


def overhangs(part, threshold=30.0, bed_eps=0.4, gap_eps=0.4, cell=4.0):
    """Area of downward faces whose slope is below `threshold` degrees from horizontal
    and that have air underneath."""
    V, T = np.asarray(part.verts), np.asarray(part.tris)
    unit, area, cen = _normals(V, T)
    nz = unit[:, 2]
    slope = np.degrees(np.arccos(np.clip(-nz, -1, 1)))
    zmin = V[:, 2].min()
    cand = (nz < -1e-6) & (slope < threshold) & (cen[:, 2] > zmin + bed_eps) & (area > 0.05)
    if not cand.any():
        return dict(area=0.0, max_gap=0.0, faces=0, worst_z=0.0)
    lo = V[:, :2].min(0)
    tri_lo = np.minimum(np.minimum(V[T[:, 0], :2], V[T[:, 1], :2]), V[T[:, 2], :2])
    tri_hi = np.maximum(np.maximum(V[T[:, 0], :2], V[T[:, 1], :2]), V[T[:, 2], :2])
    grid = {}
    for i in range(len(T)):
        x0, y0 = ((tri_lo[i] - lo) // cell).astype(int)
        x1, y1 = ((tri_hi[i] - lo) // cell).astype(int)
        for gx in range(x0, x1 + 1):
            for gy in range(y0, y1 + 1):
                grid.setdefault((gx, gy), []).append(i)
    A, B, C = V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]
    unsupported, max_gap, worst_z, faces = 0.0, 0.0, 0.0, 0
    for i in np.nonzero(cand)[0]:
        p = cen[i]
        gx, gy = ((p[:2] - lo) // cell).astype(int)
        idx = grid.get((int(gx), int(gy)))
        if not idx:
            continue
        j = np.array([k for k in idx if k != i])
        if not len(j):
            continue
        # barycentric test of this face's centre against every triangle in the cell at
        # once; one numpy call per candidate instead of one per triangle
        a, b, c = A[j], B[j], C[j]
        v0 = c[:, :2] - a[:, :2]
        v1 = b[:, :2] - a[:, :2]
        v2 = p[:2] - a[:, :2]
        d00 = np.einsum("ij,ij->i", v0, v0)
        d01 = np.einsum("ij,ij->i", v0, v1)
        d02 = np.einsum("ij,ij->i", v0, v2)
        d11 = np.einsum("ij,ij->i", v1, v1)
        d12 = np.einsum("ij,ij->i", v1, v2)
        den = d00 * d11 - d01 * d01
        good = np.abs(den) > 1e-12
        with np.errstate(invalid="ignore", divide="ignore"):
            u = np.where(good, (d11 * d02 - d01 * d12) / den, -1)
            v = np.where(good, (d00 * d12 - d01 * d02) / den, -1)
        inside = good & (u >= -1e-6) & (v >= -1e-6) & (u + v <= 1 + 1e-6)
        if not inside.any():
            below = np.array([zmin])
        else:
            z = a[inside, 2] + u[inside] * (c[inside, 2] - a[inside, 2]) \
                + v[inside] * (b[inside, 2] - a[inside, 2])
            z = z[z < p[2] - 1e-6]
            below = z if len(z) else np.array([zmin])
        gap = float(p[2] - below.max())
        if gap > gap_eps:
            unsupported += float(area[i])
            faces += 1
            if gap > max_gap:
                max_gap, worst_z = gap, float(p[2])
    return dict(area=round(unsupported, 1), max_gap=round(max_gap, 1), faces=faces,
                worst_z=round(worst_z, 1))


def footprint(part, layer=0.3):
    """First-layer contact area and how tall the part is relative to it."""
    V, T = np.asarray(part.verts), np.asarray(part.tris)
    zmin = V[:, 2].min()
    flat = np.all(np.abs(V[T][:, :, 2] - zmin) < layer, axis=1)
    _, area, _ = _normals(V, T)
    h = float(V[:, 2].max() - zmin)
    w = float(min(V[:, 0].max() - V[:, 0].min(), V[:, 1].max() - V[:, 1].min()))
    return dict(contact_mm2=round(float(area[flat].sum()), 1), height=round(h, 1),
                min_width=round(w, 1), slenderness=round(h / w, 2) if w else 0)


def advise(part, cfg, z_offset=0.0):
    """Turn the numbers into plain advisories about this device's profile."""
    out = []
    try:
        th = float(str(cfg.get("support_threshold_angle", 30)).rstrip("%") or 30)
    except ValueError:
        th = 30.0
    o = overhangs(part, threshold=th)
    o["worst_z"] = round(o["worst_z"] + z_offset, 1)     # report height above the plate
    f = footprint(part)
    sup = str(cfg.get("enable_support", "0")).strip("[]'\"") in ("1",)
    if o["area"] > 60 and not sup:
        out.append(f"{o['area']:.0f} mm2 of steep overhang with air under it (max drop "
                   f"{o['max_gap']:.1f} mm at z={o['worst_z']:.0f} mm) while supports are off "
                   f"in the designer's profile - worth a look at the preview")
    if sup and o["area"] < 5:
        out.append("supports are on in the designer's profile but the mesh has almost no "
                   "unsupported overhang; they may be there for a different orientation")
    brim = str(cfg.get("brim_type", "auto_brim"))
    if f["slenderness"] > 3 and brim == "no_brim":
        out.append(f"tall and narrow ({f['height']:.0f} mm on a {f['min_width']:.0f} mm "
                   f"footprint) with brim off in the designer's profile")
    if f["contact_mm2"] < 120 and brim == "no_brim":
        out.append(f"only {f['contact_mm2']:.0f} mm2 touches the plate and brim is off")
    return out, dict(overhang=o, footprint=f)
