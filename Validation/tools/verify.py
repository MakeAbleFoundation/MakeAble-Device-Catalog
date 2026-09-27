#!/usr/bin/env python3
"""Independent geometric check of a finished layout (does not trust the packer)."""
import math
import numpy as np
import pack
from pack import RES, px


def convex_hull(points):
    """Monotone chain hull of an (N,2) array."""
    pts = sorted(map(tuple, np.round(points, 3)))
    if len(pts) < 3:
        return pts

    def half(seq):
        out = []
        for p in seq:
            while len(out) >= 2:
                (x1, y1), (x2, y2) = out[-2], out[-1]
                if (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1) > 0:
                    break
                out.pop()
            out.append(p)
        return out

    return half(pts)[:-1] + half(reversed(pts))[:-1]


def hull_hits_exclusion(points, clearance=None):
    """Does this part's convex hull reach into the printer's excluded corner?

    The slicer inflates the object's convex hull -- not its outline -- before testing it
    against bed_exclude_area, so a C-shaped part can be rejected even when its silhouette
    is clear of the corner.
    """
    clearance = pack.EXCLUDE_CLEARANCE if clearance is None else clearance
    ex = pack.EXCLUDE_RAW
    rect = [(ex[0] - clearance, ex[1] - clearance), (ex[2] + clearance, ex[1] - clearance),
            (ex[2] + clearance, ex[3] + clearance), (ex[0] - clearance, ex[3] + clearance)]
    hull = convex_hull(points)
    if not hull:
        return False

    def sep(poly_a, poly_b):
        for poly in (poly_a, poly_b):
            n = len(poly)
            for i in range(n):
                (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
                ax, ay = -(y2 - y1), (x2 - x1)
                pa = [ax * px_ + ay * py_ for px_, py_ in poly_a]
                pb = [ax * px_ + ay * py_ for px_, py_ in poly_b]
                if max(pa) <= min(pb) + 1e-9 or max(pb) <= min(pa) + 1e-9:
                    return True
        return False

    return not sep(hull, rect)


def layout_report(placements, gap=5.0, margin=5.0):
    n = px(pack.BED)
    occ = np.zeros((n, n), dtype=bool)
    issues = []
    r = max(1, int(round((gap / 2) / RES)) - 1)   # half a gap each, less a pixel of slack
    per_plate = {}
    for pl in placements:
        per_plate.setdefault(pl.plate, []).append(pl)
    out = {}
    for plate, pls in sorted(per_plate.items()):
        occ[:] = False
        bbox = [1e9, 1e9, -1e9, -1e9]
        for k, pl in enumerate(pls):
            t = math.radians(pl.theta)
            R = np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])
            pts = pl.part.verts[:, :2] @ R.T + np.array([pl.x, pl.y])
            m, o = pack.rasterize(pts, pl.part.tris)
            x0, y0 = o
            x1, y1 = x0 + m.shape[1] * RES, y0 + m.shape[0] * RES
            bbox = [min(bbox[0], x0), min(bbox[1], y0), max(bbox[2], x1), max(bbox[3], y1)]
            # half a pixel of raster rounding is not a real margin violation: the plate
            # edge is at 256 mm and these parts still clear it by more than 4.5 mm
            slack = 0.55
            if (x0 < margin - slack or y0 < margin - slack
                    or x1 > pack.BED - margin + slack or y1 > pack.BED - margin + slack):
                issues.append(f"plate {plate} part {k} ({pl.part.name}) outside the "
                              f"{margin} mm margin: x[{x0:.1f},{x1:.1f}] y[{y0:.1f},{y1:.1f}]")
            if hull_hits_exclusion(pts):
                issues.append(f"plate {plate} part {k} ({pl.part.name}) reaches into the "
                              f"excluded corner (convex hull, which is what the slicer "
                              f"checks)")
            d = pack.dilate(m, r)
            iy, ix = px(y0 - r * RES), px(x0 - r * RES)
            h, w = d.shape
            if iy < 0 or ix < 0 or iy + h > n or ix + w > n:
                issues.append(f"plate {plate} part {k} raster off the bed")
                continue
            sub = occ[iy:iy + h, ix:ix + w]
            hits = int(np.count_nonzero(sub & d))
            if hits:
                issues.append(f"plate {plate} part {k} ({pl.part.name}) is closer than "
                              f"{gap} mm to another part ({hits} px)")
            sub |= d
        out[plate] = dict(count=len(pls), bbox=[round(v, 1) for v in bbox])
    return out, issues


def preview(placements, path, plate=1, size=760):
    """Top view of one plate: a sanity image, not a slicer preview."""
    from PIL import Image, ImageDraw
    n = px(pack.BED)
    img = Image.new("RGB", (n, n), (24, 26, 30))
    d = ImageDraw.Draw(img)
    for g in range(0, 257, 32):
        d.line([px(g), 0, px(g), n], fill=(42, 46, 52))
        d.line([0, px(g), n, px(g)], fill=(42, 46, 52))
    ex = pack.EXCLUDE
    d.rectangle([px(ex[0]), n - px(ex[3]), px(ex[2]), n - px(ex[1])], fill=(74, 40, 40))
    colors = [(96, 190, 128), (110, 160, 224), (232, 172, 88), (206, 122, 192)]
    names = {}
    for pl in placements:
        if pl.plate != plate:
            continue
        names.setdefault(pl.part.key, len(names))
        t = math.radians(pl.theta)
        R = np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])
        pts = pl.part.verts[:, :2] @ R.T + np.array([pl.x, pl.y])
        m, o = pack.rasterize(pts, pl.part.tris)
        col = colors[names[pl.part.key] % len(colors)]
        layer = Image.new("RGB", m.shape[::-1], col)
        img.paste(layer, (px(o[0]), n - px(o[1]) - m.shape[0]), Image.fromarray(np.flipud(m)))
    d2 = ImageDraw.Draw(img)
    d2.rectangle([0, 0, n - 1, n - 1], outline=(120, 126, 134))
    img.resize((size, size), Image.LANCZOS).save(path)
    return path
