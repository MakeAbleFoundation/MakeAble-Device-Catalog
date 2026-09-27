#!/usr/bin/env python3
"""Turn parts into plate layouts: pick the orientation, then fill the plate."""
import math
import numpy as np
import pack
from pack import RES, px


HEAVY_MESH = 20000      # above this, rotate the raster instead of re-rasterising


def masks_for(part, thetas, gap, fast=None):
    """Raw + dilated silhouette rasters at each angle.

    Small meshes are rasterised from the rotated geometry (exact). Big ones are
    rasterised once and the raster is rotated, which is within a pixel and turns a
    40-second sweep into a one-second one; the extra 2 px of dilation covers the
    rounding either way.
    """
    out = {}
    r = max(1, int(round(gap / RES)) + 2)   # +2 px so raster rounding can't eat the gap
    pts = part.verts[:, :2]
    if fast is None:
        fast = len(part.tris) > HEAVY_MESH
    base = pack.rasterize(pts, part.tris) if fast else None
    for th in thetas:
        if fast:
            m, o = pack.rotate_mask(base[0], base[1], th)
        else:
            t = math.radians(th)
            R = np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])
            m, o = pack.rasterize(pts @ R.T, part.tris)
        out[th] = dict(rpad=r, dil=pack.dilate(m, r),
                       dil_org=(o[0] - r * RES, o[1] - r * RES), raw=m, org=o)
    return out


def fits_at(bed, mask, iy, ix):
    h, w = mask.shape
    if iy < 0 or ix < 0 or iy + h > bed.n or ix + w > bed.n:
        return False
    return not np.any(bed.occ[iy:iy + h, ix:ix + w] & mask)


def bl_positions(bed, mask, limit=1):
    """Bottom-left feasible offsets for a raw mask."""
    ok = bed.feasible(mask)
    if ok is None or not ok.any():
        return []
    ys, xs = np.nonzero(ok)
    order = np.lexsort((xs, ys))
    return [(int(ys[i]), int(xs[i])) for i in order[:limit]]


def place(bed, part, th, mi, iy, ix, plate=1):
    """iy/ix are offsets of the RAW mask; the dilated mask is what gets stamped."""
    import p3mf
    d = int(round((mi["org"][0] - mi["dil_org"][0]) / RES))
    bed.stamp(mi["dil"], iy - d, ix - d)
    return p3mf.Placement(part=part, theta=th, plate=plate,
                          x=ix * RES - mi["org"][0], y=iy * RES - mi["org"][1])


def realize_lattice(part, th, m, v1, v2, gap, margin, cap, steps=8, target=None):
    """Lay the lattice down for real, trying a grid of anchor offsets inside one cell.
    Every position is collision-checked against the bed (margins and the excluded corner
    included), so an over-optimistic estimate simply places fewer."""
    mask = m["raw"]
    h, w = mask.shape
    m0 = px(margin)
    best = ([], None)
    px_x, (sx, px_y) = v1[0], v2
    if target and target > 30:
        steps = 4          # dense plates of small parts barely care where the grid starts
    for ax in range(steps):
        ox = m0 + int(px_x * ax / steps)
        for ay in range(steps):
            oy = m0 + int(px_y * ay / steps)
            b = pack.Bed(margin=margin, gap=gap)
            out = []
            rows = int((pack.BED / RES) // max(1, px_y)) + 2
            cols = int((pack.BED / RES) // max(1, px_x)) + 2
            for j in range(rows):
                iy = oy + j * px_y
                if iy + h > b.n:
                    break
                for i in range(-cols, 2 * cols):
                    ix = ox + i * px_x + j * sx
                    if ix < 0 or ix + w > b.n:
                        continue
                    if fits_at(b, mask, iy, ix):
                        out.append(place(b, part, th, m, iy, ix))
                        if len(out) >= cap:
                            break
                if len(out) >= cap:
                    break
            if len(out) > len(best[0]):
                best = (out, b)
            if target and len(best[0]) >= target:
                return best          # the estimate is the ceiling; stop hunting anchors
    return best if best[1] is not None else ([], pack.Bed(margin=margin, gap=gap))


def greedy_extra(part, thetas, mi, state, gap, margin, cap, tries=12):
    """Mop up leftover space after the lattice pass."""
    placements, bed = state
    if bed is None:
        bed = pack.Bed(margin=margin, gap=gap)
    added = 0
    while len(placements) < cap and added < tries:
        best = None
        for th in thetas:
            m = mi.get(th % 360)
            if m is None:
                continue
            pos = bl_positions(bed, m["raw"], limit=1)
            if pos and (best is None or pos[0] < best[1]):
                best = (th % 360, pos[0], m)
        if not best:
            break
        th, (iy, ix), m = best
        placements.append(place(bed, part, th, m, iy, ix))
        added += 1
    return placements, bed


def plan_single(part, gap=5.0, margin=5.0, thetas=None, cap=400, verbose=True):
    """Fill one plate with copies of a single part."""
    thetas = thetas if thetas is not None else list(range(0, 180, 5))
    mi = masks_for(part, thetas, gap)
    usable = px(pack.BED - 2 * margin)
    scored = []
    for th, d in mi.items():
        cnt, v1, v2 = pack.lattice_count(d["raw"], d["dil"], (usable, usable), d["rpad"])
        scored.append((cnt, th, v1, v2))
    scored.sort(reverse=True, key=lambda s: (s[0], -s[1]))
    best = None
    for cnt, th, v1, v2 in scored[:4]:
        if v1:
            got = realize_lattice(part, th, mi[th], v1, v2, gap, margin, cap, target=cnt)
        else:
            got = ([], pack.Bed(margin=margin, gap=gap))
        got = greedy_extra(part, [th, (th + 180) % 360], mi, got, gap, margin, cap,
                           tries=12 if v1 else cap)
        if verbose:
            print(f"    theta={th:3}  lattice estimate {cnt:3}  ->  placed {len(got[0])}")
        if best is None or len(got[0]) > len(best[0]):
            best = got
    return best


def plan_kit(parts, counts, gap=5.0, margin=5.0, thetas=None, max_kits=60, verbose=True):
    """Fill one plate with complete kits: parts[i] appears counts[i] times per kit."""
    thetas = thetas if thetas is not None else list(range(0, 180, 15))
    mi = [masks_for(p, thetas, gap) for p in parts]
    order = sorted(range(len(parts)), key=lambda i: -mi[i][thetas[0]]["raw"].sum())
    bed = pack.Bed(margin=margin, gap=gap)
    placements, kits = [], 0
    while kits < max_kits:
        snapshot = bed.occ.copy()
        trial, ok = [], True
        for i in order:
            for _ in range(counts[i]):
                best = None
                for th in thetas:
                    m = mi[i][th]
                    pos = bl_positions(bed, m["raw"], limit=1)
                    if pos and (best is None or pos[0] < best[1]):
                        best = (th, pos[0], m)
                if not best:
                    ok = False
                    break
                th, (iy, ix), m = best
                trial.append(place(bed, parts[i], th, m, iy, ix))
            if not ok:
                break
        if not ok:
            bed.occ = snapshot
            bed._fft = None
            break
        placements += trial
        kits += 1
        if verbose:
            print(f"    kit {kits} placed ({len(placements)} parts)")
    return placements, kits


# --------------------------------------------------------------------------- pairs
# C- and L-shaped parts (bottle openers, shoe horns, pliers) nest far better when every
# second copy is turned 180 degrees. A pair is packed as one unit: two copies at the
# tightest relative offset that still respects the gap.

class Unit:
    """Two copies of a part, welded into one thing the packer can lay out."""

    def __init__(self, members):
        import numpy as np
        self.members = members                     # [(part, theta, dx, dy), ...]
        vs, ts, off = [], [], 0
        for part, th, dx, dy in members:
            t = math.radians(th)
            R = np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])
            v = part.verts.copy()
            v[:, :2] = v[:, :2] @ R.T + np.array([dx, dy])
            vs.append(v)
            ts.append(np.asarray(part.tris) + off)
            off += len(v)
        self.verts = np.vstack(vs)
        self.tris = np.vstack(ts)
        self.name = members[0][0].name
        self.key = members[0][0].key + "#pair"


def emit(unit, phi, x, y, plate=1):
    """Placements for every member of a unit placed at (x, y) turned by phi."""
    import p3mf
    t = math.radians(phi)
    c, s = math.cos(t), math.sin(t)
    out = []
    for part, th, dx, dy in unit.members:
        out.append(p3mf.Placement(part=part, theta=th + phi, plate=plate,
                                  x=x + c * dx - s * dy, y=y + s * dx + c * dy))
    return out


def best_pair(part, th, gap, mi=None):
    """Tightest 180-degree pairing of `part` at angle `th`, or None."""
    mi = mi or masks_for(part, [th, (th + 180) % 360], gap)
    if th not in mi or (th + 180) % 360 not in mi:
        mi = dict(mi)
        mi.update(masks_for(part, [th, (th + 180) % 360], gap))
    A, B = mi[th], mi[(th + 180) % 360]
    a_dil, b_raw = A["dil"], B["raw"]
    ah, aw = a_dil.shape
    bh, bw = b_raw.shape
    n = 1 << (max(ah + bh, aw + bw) + 2 - 1).bit_length()
    F = np.fft.rfft2(a_dil.astype(float), s=(n, n))
    G = np.fft.rfft2(b_raw[::-1, ::-1].astype(float), s=(n, n))
    corr = np.fft.irfft2(F * G, s=(n, n))[bh - 1:, bw - 1:]
    ok = corr < 0.5
    # offsets are B's raw origin relative to A's dilated origin; convert to raw-to-raw
    rp = A["rpad"]
    ys, xs = np.nonzero(ok)
    if not len(ys):
        return None
    dx = xs - rp
    dy = ys - rp
    arh, arw = A["raw"].shape
    x0 = np.minimum(0, dx)
    x1 = np.maximum(arw, dx + bw)
    y0 = np.minimum(0, dy)
    y1 = np.maximum(arh, dy + bh)
    area = (x1 - x0).astype(np.int64) * (y1 - y0).astype(np.int64)
    i = int(np.argmin(area))
    # only worth it if the pair is denser than two parts side by side
    if area[i] >= 2 * arh * arw:
        return None
    return Unit([(part, th, 0.0, 0.0),
                 (part, (th + 180) % 360,
                  float(dx[i] * RES + A["org"][0] - B["org"][0]),
                  float(dy[i] * RES + A["org"][1] - B["org"][1]))])


def plan_single_best(part, gap=5.0, margin=5.0, thetas=None, cap=400, verbose=True):
    """Plain lattice vs. 180-degree pairs: whichever puts more parts on the plate."""
    thetas = thetas if thetas is not None else list(range(0, 180, 5))
    plain, _bed = plan_single(part, gap=gap, margin=margin, thetas=thetas, cap=cap,
                              verbose=verbose)
    best, how = plain, "single"
    mi = masks_for(part, thetas, gap)
    usable = px(pack.BED - 2 * margin)
    scored = sorted(((pack.lattice_count(d["raw"], d["dil"], (usable, usable), d["rpad"])[0],
                      th) for th, d in mi.items()), reverse=True)
    # the angle that packs best on its own is often not the angle that pairs best (the
    # eye-drop pliers only pair inside the plate at 60 and 150 degrees), so sweep widely
    # sweep pair angles as finely as the single sweep: which angle lets two copies
    # interlock is not obvious, and 175 deg beat everything for the bottle cap opener.
    # Rasters here come from rotating one raster (a pixel of slop, covered by the extra
    # dilation) so 36 angles stay cheap.
    pair_angles = sorted(set(thetas) | {th for _c, th in scored[:2]})
    mi_pair = masks_for(part, sorted({a for th in pair_angles
                                      for a in (th, (th + 180) % 360)}), gap, fast=True)
    for th in pair_angles:
        unit = best_pair(part, th, gap, mi_pair)
        if unit is None:
            continue
        umi = masks_for(unit, [0, 90], gap)
        if all(min(d["raw"].shape) * RES > pack.BED - 2 * margin for d in umi.values()):
            continue
        for uth, d in umi.items():
            cnt, v1, v2 = pack.lattice_count(d["raw"], d["dil"], (usable, usable), d["rpad"])
            if not v1 or 2 * cnt <= len(best):
                continue        # cheap estimate first: only lay it out if it could win
            spots, bed = realize_lattice(unit, uth, d, v1, v2, gap, margin, cap // 2,
                                         target=cnt)
            spots, bed = greedy_extra(unit, [uth], umi, (spots, bed), gap, margin,
                                      cap // 2, tries=2)
            placed = [p for sp in spots for p in emit(unit, sp.theta, sp.x, sp.y)]
            if verbose:
                print(f"    pair theta={th:3}+{uth:3}  {len(spots)} pairs -> {len(placed)} parts")
            if len(placed) > len(best):
                best, how = placed, f"pairs at {th}deg"
    if verbose:
        print(f"    best: {len(best)} parts ({how})")
    return best, how


def kit_cluster(parts, counts, gap, margin, thetas):
    """Pack one kit into a tight cluster, then hand it back as a single Unit so the
    lattice packer can tile whole kits instead of placing them one at a time."""
    mi = [masks_for(p, thetas, gap) for p in parts]
    order = sorted(range(len(parts)), key=lambda i: -mi[i][thetas[0]]["raw"].sum())
    bed = pack.Bed(margin=margin, gap=gap)
    members = []
    for i in order:
        for _ in range(counts[i]):
            best = None
            for th in thetas:
                pos = bl_positions(bed, mi[i][th]["raw"], limit=1)
                if pos and (best is None or pos[0] < best[1]):
                    best = (th, pos[0], mi[i][th])
            if not best:
                return None
            th, (iy, ix), m = best
            pl = place(bed, parts[i], th, m, iy, ix)
            members.append([parts[i], th, pl.x, pl.y])
    xs = [m[2] for m in members]
    ys = [m[3] for m in members]
    for m in members:
        m[2] -= min(xs)
        m[3] -= min(ys)
    return Unit([tuple(m) for m in members])


def plan_kit_best(parts, counts, gap=5.0, margin=5.0, cap=400, verbose=True):
    """Kit by kit vs. tiling a whole-kit cluster: whichever fits more complete kits."""
    best, how = [], "none"
    for step in (15, 10):
        thetas = list(range(0, 180, step))
        pls, kits = plan_kit(parts, counts, gap=gap, margin=margin, thetas=thetas,
                             verbose=False)
        if verbose:
            print(f"    kit-by-kit ({step} deg steps): {kits} kits")
        if kits > len(best) / max(1, sum(counts)):
            best, how, best_kits = pls, f"kit by kit ({step} deg)", kits
    best_kits = len(best) // max(1, sum(counts))
    unit = kit_cluster(parts, counts, gap, margin, list(range(0, 180, 15)))
    if unit is not None:
        umi = masks_for(unit, [0, 90], gap)
        usable = px(pack.BED - 2 * margin)
        for uth, d in umi.items():
            cnt, v1, v2 = pack.lattice_count(d["raw"], d["dil"], (usable, usable), d["rpad"])
            if not v1:
                continue
            spots, bed = realize_lattice(unit, uth, d, v1, v2, gap, margin, cap, target=cnt)
            spots, bed = greedy_extra(unit, [uth], umi, (spots, bed), gap, margin, cap,
                                      tries=4)
            placed = [p for sp in spots for p in emit(unit, sp.theta, sp.x, sp.y)]
            if verbose:
                print(f"    kit cluster at {uth} deg: {len(spots)} kits")
            if len(spots) > best_kits:
                best, how, best_kits = placed, f"kit cluster ({uth} deg)", len(spots)
    if verbose:
        print(f"    best: {best_kits} kits ({how})")
    return best, best_kits, how
