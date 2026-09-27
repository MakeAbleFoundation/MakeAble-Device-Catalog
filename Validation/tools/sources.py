#!/usr/bin/env python3
"""Turn references, loose STLs and multi-shell meshes into placeable parts."""
import os, re, struct
import numpy as np
import p3mf

MESH_HEAD = ('<?xml version="1.0" encoding="UTF-8"?>\n'
             '<model unit="millimeter" xml:lang="en-US" '
             'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
             'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
             'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" '
             'requiredextensions="p">\n'
             ' <metadata name="BambuStudio:3mfVersion">1</metadata>\n'
             ' <resources>\n'
             '  <object id="1" p:UUID="00010000-81cb-4c03-9d28-80fed5dfa1dc" type="model">\n'
             '   <mesh>\n')
MESH_TAIL = '   </mesh>\n  </object>\n </resources>\n <build/>\n</model>\n'


def mesh_payload(V, T):
    out = [MESH_HEAD, "    <vertices>\n"]
    for x, y, z in V:
        out.append(f'     <vertex x="{x:.9g}" y="{y:.9g}" z="{z:.9g}"/>\n')
    out.append("    </vertices>\n    <triangles>\n")
    for a, b, c in T:
        out.append(f'     <triangle v1="{a}" v2="{b}" v3="{c}"/>\n')
    out.append("    </triangles>\n")
    out.append(MESH_TAIL)
    return "".join(out).encode("utf-8")


def part_xml(name, face_count):
    return (f'<part id="1" subtype="normal_part">\n'
            f'      <metadata key="name" value="{p3mf.esc(name)}"/>\n'
            f'      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>\n'
            f'      <metadata key="source_object_id" value="0"/>\n'
            f'      <metadata key="source_volume_id" value="0"/>\n'
            f'      <mesh_stat face_count="{face_count}" edges_fixed="0" '
            f'degenerate_facets="0" facets_removed="0" facets_reversed="0" '
            f'backwards_edges="0"/>\n    </part>')


def _normalise(V):
    """Centre in XY and sit on the bed, so a placement is just (x, y)."""
    V = np.asarray(V, dtype=float)
    cx = (V[:, 0].min() + V[:, 0].max()) / 2
    cy = (V[:, 1].min() + V[:, 1].max()) / 2
    return V - np.array([cx, cy, V[:, 2].min()])


def from_stl(path, name=None, key=None):
    b = open(path, "rb").read()
    if b[:5].lower() == b"solid" and b"facet" in b[:400]:
        nums = re.findall(rb"vertex\s+(\S+)\s+(\S+)\s+(\S+)", b)
        pts = np.array([[float(x) for x in t] for t in nums], dtype=float)
    else:
        n = struct.unpack("<I", b[80:84])[0]
        pts = np.empty((n * 3, 3), dtype=float)
        for i in range(n):
            o = 84 + i * 50
            v = struct.unpack("<12f", b[o:o + 48])
            pts[3 * i:3 * i + 3] = np.array(v[3:12]).reshape(3, 3)
    q = np.round(pts, 5)                      # weld identical vertices
    uniq, inv = np.unique(q, axis=0, return_inverse=True)
    V = _normalise(uniq)
    T = inv.reshape(-1, 3)
    nm = name or os.path.basename(path)
    return p3mf.SrcPart(
        key=key or f"stl::{os.path.basename(path)}", name=nm,
        mesh_bytes=mesh_payload(V, T), mesh_objid=1, comp_tf=list(p3mf.IDENT),
        base_lin=[1, 0, 0, 0, 1, 0, 0, 0, 1], base_z=0.0, ms_meta=[],
        part_xml=part_xml(nm, len(T)), face_count=str(len(T)), extruder="1",
        verts=V, tris=T)


def split_shells(part, names=None, min_tris=50):
    """Split a multi-body object into one part per connected shell."""
    V, T = p3mf.mesh_geometry(part.mesh_bytes, part.mesh_objid)
    parent = np.arange(len(V))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for a, b, c in T:
        ra, rb, rc = find(a), find(b), find(c)
        parent[rb] = ra
        parent[rc] = ra
    roots = np.array([find(i) for i in range(len(V))])
    tri_root = roots[T[:, 0]]
    lin = p3mf.mat_mul(part.comp_tf[0:9], part.base_lin)
    M = np.array([lin[0:3], lin[3:6], lin[6:9]], dtype=float)
    out = []
    for i, r in enumerate(sorted(set(tri_root.tolist()),
                                 key=lambda r: -int((tri_root == r).sum()))):
        sel = tri_root == r
        if sel.sum() < min_tris:
            continue
        idx = np.unique(T[sel])
        remap = {int(v): j for j, v in enumerate(idx)}
        sub_T = np.array([[remap[int(v)] for v in tri] for tri in T[sel]])
        world = V[idx] @ M + np.array(part.comp_tf[9:12]) @ M
        cx = (world[:, 0].min() + world[:, 0].max()) / 2
        cy = (world[:, 1].min() + world[:, 1].max()) / 2
        world = world - np.array([cx, cy, 0.0])
        nm = (names[i] if names and i < len(names) else f"{part.name} [{i + 1}]")
        out.append(p3mf.SrcPart(
            key=f"{part.key}#shell{i}", name=nm, mesh_bytes=mesh_payload(world, sub_T),
            mesh_objid=1, comp_tf=list(p3mf.IDENT), base_lin=[1, 0, 0, 0, 1, 0, 0, 0, 1],
            base_z=part.base_z, ms_meta=list(part.ms_meta),
            part_xml=part_xml(nm, len(sub_T)), face_count=str(len(sub_T)),
            extruder=part.extruder, verts=world, tris=sub_T))
    return out


def from_ref(path, names=None, indices=None):
    ref = p3mf.Ref(path)
    parts = [p3mf.load_geometry(p) for p in ref.parts()]
    if names:
        want = list(names)
        parts = [p for p in parts if p.name in want]
        parts.sort(key=lambda p: want.index(p.name))
    if indices is not None:
        parts = [parts[i] for i in indices]
    return ref, parts
