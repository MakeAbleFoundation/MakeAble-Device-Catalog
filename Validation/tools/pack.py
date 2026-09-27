#!/usr/bin/env python3
"""Fit as many copies of a part as possible on the P1S plate.

Everything is done on a 0.25 mm raster of the part's true XY silhouette (not its bounding
box or convex hull), so concave parts nest into each other. A staggered lattice search
picks the orientation and pitch; a bottom-left greedy pass mops up the leftovers.
"""
import math
import numpy as np
from PIL import Image, ImageDraw

RES = 0.25                     # mm per pixel
BED = 256.0                    # P1S plate, mm
# Bambu's bed_exclude_area for this machine, grown by 8 mm: the slicer rejects a plate
# whose object merely comes "too close to exclusion area", and a brim reaches 5 mm past
# the part, so the raw rectangle is not enough clearance.
EXCLUDE_RAW = (0.0, 0.0, 18.0, 28.0)
EXCLUDE_CLEARANCE = 8.0
EXCLUDE = (0.0, 0.0, EXCLUDE_RAW[2] + EXCLUDE_CLEARANCE, EXCLUDE_RAW[3] + EXCLUDE_CLEARANCE)


def set_exclusion_clearance(mm):
    """Grow the no-go corner. Used to retry a layout that lost a part to the corner:
    keeping the packer further away is usually cheaper than dropping a whole part."""
    global EXCLUDE
    EXCLUDE = (0.0, 0.0, EXCLUDE_RAW[2] + mm, EXCLUDE_RAW[3] + mm)
    return EXCLUDE


def px(mm):
    return int(round(mm / RES))


def rasterize(pts, tris):
    """Binary silhouette of a mesh projected on XY. Returns (mask, (x0, y0))."""
    x0, y0 = pts[:, 0].min(), pts[:, 1].min()
    x1, y1 = pts[:, 0].max(), pts[:, 1].max()
    w, h = px(x1 - x0) + 3, px(y1 - y0) + 3
    img = Image.new("1", (w, h), 0)
    d = ImageDraw.Draw(img)
    P = np.empty((len(pts), 2), dtype=np.int32)
    P[:, 0] = np.rint((pts[:, 0] - x0) / RES) + 1
    P[:, 1] = np.rint((pts[:, 1] - y0) / RES) + 1
    for a, b, c in tris:
        d.polygon([tuple(P[a]), tuple(P[b]), tuple(P[c])], fill=1)
    return np.array(img, dtype=bool), (x0 - RES, y0 - RES)


def rotate_mask(mask, origin, theta):
    """Rotate a silhouette raster CCW by theta about the geometry origin."""
    if theta % 360 == 0:
        return mask, origin
    img = Image.fromarray(mask)
    out = img.rotate(-theta, resample=Image.NEAREST, expand=True, fillcolor=0)  # PIL is CW here
    m = np.array(out, dtype=bool)
    h, w = mask.shape
    h2, w2 = m.shape
    c_in = np.array([w / 2.0, h / 2.0])
    c_out = np.array([w2 / 2.0, h2 / 2.0])
    t = math.radians(theta)
    R = np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])
    o = R @ np.asarray(origin, dtype=float) + RES * (R @ c_in - c_out)
    return m, (float(o[0]), float(o[1]))


def dilate(mask, r):
    """Chebyshev dilation by r pixels; the array grows by r on every side."""
    if r <= 0:
        return mask
    m = np.zeros((mask.shape[0] + 2 * r, mask.shape[1] + 2 * r), dtype=bool)
    m[r:r + mask.shape[0], r:r + mask.shape[1]] = mask
    for axis in (0, 1):
        acc = m.copy()
        for s in range(1, r + 1):
            acc |= np.roll(m, s, axis=axis)
            acc |= np.roll(m, -s, axis=axis)
        m = acc
    return m


class Bed:
    """Occupancy raster of the plate plus FFT-based placement search."""

    def __init__(self, margin=5.0, gap=5.0):
        self.n = px(BED)
        self.gap = gap
        self.occ = np.ones((self.n, self.n), dtype=bool)
        m = px(margin)
        self.occ[m:self.n - m, m:self.n - m] = False
        ex = (px(EXCLUDE[0]), px(EXCLUDE[1]), px(EXCLUDE[2]), px(EXCLUDE[3]))
        self.occ[ex[1]:ex[3], ex[0]:ex[2]] = True
        self._fft = None

    def free_fft(self):
        if self._fft is None:
            self._fft = np.fft.rfft2(self.occ.astype(float), s=(self.n, self.n))
        return self._fft

    def feasible(self, mask):
        """Offsets where `mask` does not collide with anything already on the bed."""
        mh, mw = mask.shape
        if mh > self.n or mw > self.n:
            return None
        F = np.fft.rfft2(mask[::-1, ::-1].astype(float), s=(self.n, self.n))
        corr = np.fft.irfft2(self.free_fft() * F, s=(self.n, self.n))
        ok = corr[mh - 1:, mw - 1:] < 0.5
        ok[self.n - mh + 1:, :] = False
        ok[:, self.n - mw + 1:] = False
        return ok

    def place(self, mask):
        self.occ |= mask
        self._fft = None

    def stamp(self, mask, iy, ix):
        """Mark a dilated mask as occupied, clipping whatever falls off the bed."""
        h, w = mask.shape
        y0, x0 = max(0, iy), max(0, ix)
        y1, x1 = min(self.n, iy + h), min(self.n, ix + w)
        if y0 >= y1 or x0 >= x1:
            return
        self.occ[y0:y1, x0:x1] |= mask[y0 - iy:y1 - iy, x0 - ix:x1 - ix]
        self._fft = None


def lattice_count(raw, dil, usable_px, rpad, stagger_steps=24):
    """Best staggered lattice for one part. `dil` is `raw` grown by the required gap, so a
    raw copy that avoids `dil` is automatically at least one gap away.

    Returns (count, v1, v2) with lattice vectors in pixels.
    """
    n = max(dil.shape[0] + raw.shape[0], dil.shape[1] + raw.shape[1]) + 2
    n = 1 << (n - 1).bit_length()
    A = np.fft.rfft2(dil.astype(float), s=(n, n))
    B = np.fft.rfft2(raw[::-1, ::-1].astype(float), s=(n, n))
    corr = np.fft.irfft2(A * B, s=(n, n))
    rh, rw = raw.shape
    dh, dw = dil.shape

    def ok(dx, dy):
        """True when a raw copy shifted by (dx, dy) -- origin to origin between raw copies
        -- stays clear of the dilated original. The +rpad corrects for the dilated array
        starting rpad pixels earlier; the early exit avoids circular-correlation aliasing."""
        if abs(dx) > rw + rpad or abs(dy) > rh + rpad:
            return True
        return bool(corr[(dy + rpad + rh - 1) % n, (dx + rpad + rw - 1) % n] < 0.5)

    lim_x, lim_y = rw + rpad, rh + rpad
    best = (0, None, None)

    dxs = np.arange(1, dw + rw)
    row0 = (rpad + rh - 1) % n
    vals = np.where(dxs > lim_x, 0.0, corr[row0, (dxs + rpad + rw - 1) % n])
    hit = np.nonzero(vals < 0.5)[0]
    if not len(hit):
        return best
    pitch_x = int(dxs[hit[0]])

    # every lattice difference vector within +-3 steps has to clear the gap, otherwise the
    # count is a fantasy the realisation pass can never hit. Vectorised over dy: the same
    # check as a loop, minus a million Python calls on big parts.
    combos = [(k1, k2) for k1 in range(-3, 4) for k2 in range(-3, 4) if (k1, k2) != (0, 0)]
    dys = np.arange(1, dh + rh)
    for s_i in range(stagger_steps):
        st = int(round(pitch_x * s_i / stagger_steps))
        ok_all = np.ones(len(dys), dtype=bool)
        for k1, k2 in combos:
            dx = k2 * st + k1 * pitch_x
            dy = k2 * dys
            far = (abs(dx) > lim_x) | (np.abs(dy) > lim_y)
            v = corr[(dy + rpad + rh - 1) % n, (dx + rpad + rw - 1) % n]
            ok_all &= far | (v < 0.5)
            if not ok_all.any():
                break
        cand = np.nonzero(ok_all)[0]
        if not len(cand):
            continue
        pitch_y = int(dys[cand[0]])
        rows = int((usable_px[1] - rh) // pitch_y) + 1
        cnt = 0
        for r in range(max(0, rows)):
            off = (st * r) % pitch_x
            c = int((usable_px[0] - rw - off) // pitch_x) + 1
            cnt += max(0, c)
        if cnt > best[0]:
            best = (cnt, (pitch_x, 0), (st, pitch_y))
    return best
