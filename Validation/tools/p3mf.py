#!/usr/bin/env python3
"""Read Bambu/Orca 3mf projects and write new ones with parts re-laid-out.

Mesh payloads are copied byte-for-byte (so painted seams survive); only the object
wrappers, build items, plate assignment and the settings blocks are rewritten.

Transform convention: 3mf stores 12 numbers and a point maps as
    x' = m0*x + m3*y + m6*z + m9  (etc), i.e. row-vector p' = p*M + t.
"""
import json, math, os, re, zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass

CORE = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
PROD = "http://schemas.microsoft.com/3dmanufacturing/production/2015/06"
NS = {"m": CORE, "p": PROD}

PROJECT_SETTINGS = "Metadata/project_settings.config"
MODEL_SETTINGS = "Metadata/model_settings.config"
MODEL_3D = "3D/3dmodel.model"

IDENT = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]


def parse_tf(s):
    if not s:
        return list(IDENT)
    v = [float(x) for x in s.split()]
    return v if len(v) == 12 else list(IDENT)


def fmt_tf(v):
    return " ".join("%.9g" % (0.0 if abs(x) < 1e-12 else x) for x in v)


def mat_mul(a, b):
    """Row-vector composition of two 3x3 blocks: p*(A then B)."""
    A = [a[0:3], a[3:6], a[6:9]]
    B = [b[0:3], b[3:6], b[6:9]]
    C = [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return C[0] + C[1] + C[2]


def rot_z(deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [c, s, 0, -s, c, 0, 0, 0, 1]


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


@dataclass
class SrcPart:
    """One printable object taken from a reference project, ready to be re-placed."""
    key: str
    name: str
    mesh_bytes: bytes
    mesh_objid: int
    comp_tf: list
    base_lin: list
    base_z: float
    ms_meta: list
    part_xml: str
    face_count: str
    extruder: str = "1"
    plate: int = 1
    verts: object = None
    tris: object = None


@dataclass
class Placement:
    part: SrcPart
    theta: float
    x: float
    y: float
    plate: int = 1


class Ref:
    """A reference project: the designer's 3mf."""

    def __init__(self, path):
        self.path = path
        self.zf = zipfile.ZipFile(path)
        self.names = self.zf.namelist()
        self.settings = (json.loads(self.zf.read(PROJECT_SETTINGS))
                         if PROJECT_SETTINGS in self.names else {})
        self.root = ET.fromstring(self.zf.read(MODEL_3D).decode("utf-8"))
        self.ms_root = ET.fromstring(self.zf.read(MODEL_SETTINGS).decode("utf-8")
                                     if MODEL_SETTINGS in self.names else "<config/>")

    def meta(self):
        out = {}
        for md in self.root.findall("m:metadata", NS):
            if md.get("name"):
                out[md.get("name")] = md.text or ""
        return out

    def auxiliaries(self):
        return [n for n in self.names if n.startswith("Auxiliaries/")]

    def object_plates(self):
        """object id -> plate number, from model_settings.config."""
        out = {}
        for i, pl in enumerate(self.ms_root.findall("plate"), start=1):
            num = i
            for md in pl.findall("metadata"):
                if md.get("key") == "plater_id":
                    num = int(md.get("value"))
            for mi in pl.findall("model_instance"):
                for md in mi.findall("metadata"):
                    if md.get("key") == "object_id":
                        out[md.get("value")] = num
        return out

    def parts(self):
        res = self.root.find("m:resources", NS)
        objs = {o.get("id"): o for o in res.findall("m:object", NS)}
        ms_objs = {o.get("id"): o for o in self.ms_root.findall("object")}
        plate_of = self.object_plates()
        out = []
        for item in self.root.find("m:build", NS).findall("m:item", NS):
            oid = item.get("objectid")
            obj = objs[oid]
            tf = parse_tf(item.get("transform"))
            comps = obj.find("m:components", NS)
            if comps is None:
                raise RuntimeError(f"{self.path}: object {oid} has an inline mesh")
            comp = comps.findall("m:component", NS)
            if len(comp) != 1:
                raise RuntimeError(f"{self.path}: object {oid} has {len(comp)} components")
            comp = comp[0]
            path = (comp.get(f"{{{PROD}}}path") or MODEL_3D).lstrip("/")
            objid = comp.get("objectid")
            if path == MODEL_3D:
                # the mesh lives in the main model file: lift out just this object, or the
                # payload would drag in the file's other objects and its <build> section,
                # which the slicer then instantiates on top of ours
                payload = extract_object(self.zf.read(path), objid)
            else:
                payload = self.zf.read(path)
            mo = ms_objs.get(oid)
            meta, part_xml, face_count, extruder, name = [], "", "", "1", f"object_{oid}"
            if mo is not None:
                for md in mo.findall("metadata"):
                    k, v = md.get("key"), md.get("value")
                    if k == "name":
                        name = v
                    elif k == "extruder":
                        extruder = v
                    elif k is None and md.get("face_count"):
                        face_count = md.get("face_count")
                    elif k:
                        meta.append((k, v))
                p = mo.find("part")
                if p is not None:
                    part_xml = ET.tostring(p, encoding="unicode")
            out.append(SrcPart(
                key=f"{os.path.basename(self.path)}::{oid}", name=name,
                mesh_bytes=payload, mesh_objid=int(objid),
                comp_tf=parse_tf(comp.get("transform")), base_lin=tf[0:9], base_z=tf[11],
                ms_meta=meta, part_xml=part_xml, face_count=face_count, extruder=extruder,
                plate=plate_of.get(oid, 1)))
        return out


MESH_WRAP_HEAD = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<model unit="millimeter" xml:lang="en-US" '
    'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
    'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
    'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" '
    'requiredextensions="p">\n'
    ' <metadata name="BambuStudio:3mfVersion">1</metadata>\n'
    ' <resources>\n')
MESH_WRAP_TAIL = " </resources>\n <build/>\n</model>\n"


def extract_object(model_bytes, objid):
    """A standalone mesh payload holding one <object> copied verbatim from a model file."""
    text = model_bytes.decode("utf-8")
    m = re.search(r'<object id="%s"[ >].*?</object>' % re.escape(str(objid)), text, re.S)
    if not m:
        raise KeyError(f"object {objid} not found in model file")
    return (MESH_WRAP_HEAD + "  " + m.group(0) + "\n" + MESH_WRAP_TAIL).encode("utf-8")


def mesh_geometry(mesh_bytes, objid):
    import numpy as np
    root = ET.fromstring(mesh_bytes)
    for o in root.find("m:resources", NS).findall("m:object", NS):
        if int(o.get("id")) != int(objid):
            continue
        mesh = o.find("m:mesh", NS)
        V = np.array([[float(v.get("x")), float(v.get("y")), float(v.get("z"))]
                      for v in mesh.find("m:vertices", NS)], dtype=float)
        T = np.array([[int(t.get("v1")), int(t.get("v2")), int(t.get("v3"))]
                      for t in mesh.find("m:triangles", NS)], dtype=int)
        return V, T
    raise KeyError(objid)


def load_geometry(part):
    """Bed-space vertices: component + item orientation applied, translation dropped."""
    import numpy as np
    V, T = mesh_geometry(part.mesh_bytes, part.mesh_objid)
    lin = mat_mul(part.comp_tf[0:9], part.base_lin)
    M = np.array([lin[0:3], lin[3:6], lin[6:9]], dtype=float)
    part.verts = V @ M + np.array(part.comp_tf[9:12], dtype=float) @ M
    part.tris = T
    return part


HEAD = '<?xml version="1.0" encoding="UTF-8"?>\n'
SLICE_INFO = (HEAD + '<config>\n  <header>\n'
              '    <header_item key="X-BBL-Client-Type" value="slicer"/>\n'
              '    <header_item key="X-BBL-Client-Version" value="02.02.02.56"/>\n'
              '  </header>\n</config>\n')


# provenance that belongs to the file a shell was borrowed from, not to this model
DESIGN_META = ("DesignModelId", "DesignProfileId", "DesignRegion", "ProfileTitle",
               "ProfileUserId", "ProfileUserName", "ProfileCover", "ProfileDescription",
               "DesignerUserId", "DesignerCover", "License", "CopyRight", "Copyright",
               "Origin", "Description")


def write_project(out_path, placements, settings, ref_for_shell, meta_override=None,
                  plate_names=None, keep_aux=True, strip_design_meta=False):
    """Write a Bambu project: one <object> per placement, meshes shared by path."""
    meshes, mesh_files = {}, []
    for pl in placements:
        if pl.part.key in meshes:
            continue
        idx = len(meshes) + 1
        path = f"3D/Objects/object_{idx}.model"
        new_id = 1000 + idx
        body = re.sub(rb'(<object id=")(\d+)(")',
                      lambda m, n=new_id: m.group(1) + str(n).encode() + m.group(3),
                      pl.part.mesh_bytes, count=1)
        meshes[pl.part.key] = (path, new_id)
        mesh_files.append((path, body))

    res, build, ms_objs, plates = [], [], [], {}
    oid, ident = 2, 100
    for pl in placements:
        path, mid = meshes[pl.part.key]
        lin = mat_mul(pl.part.base_lin, rot_z(pl.theta))
        tf = lin + [pl.x, pl.y, pl.part.base_z]
        res.append(
            f'  <object id="{oid}" p:UUID="{oid:08d}-61cb-4c03-9d28-80fed5dfa1dc" type="model">\n'
            f'   <components>\n'
            f'    <component p:path="/{path}" objectid="{mid}" '
            f'p:UUID="{oid:04d}0000-b206-40ff-9872-83e8017abed1" '
            f'transform="{fmt_tf(pl.part.comp_tf[0:9] + [0, 0, 0])}"/>\n'
            f'   </components>\n  </object>\n')
        build.append(f'  <item objectid="{oid}" p:UUID="{oid:08d}-b1ec-4553-aec9-835e5b724bb4" '
                     f'transform="{fmt_tf(tf)}" printable="1"/>\n')
        mo = [f'  <object id="{oid}">\n',
              f'    <metadata key="name" value="{esc(pl.part.name)}"/>\n',
              f'    <metadata key="extruder" value="{pl.part.extruder}"/>\n']
        for k, v in pl.part.ms_meta:
            mo.append(f'    <metadata key="{esc(k)}" value="{esc(v)}"/>\n')
        if pl.part.face_count:
            mo.append(f'    <metadata face_count="{pl.part.face_count}"/>\n')
        if pl.part.part_xml:
            px = re.sub(r'<part id="\d+"', f'<part id="{mid}"', pl.part.part_xml, count=1)
            mo.append("    " + px.strip() + "\n")
        mo.append("  </object>\n")
        ms_objs.append("".join(mo))
        plates.setdefault(pl.plate, []).append((oid, ident))
        oid += 1
        ident += 1

    ms = [HEAD, "<config>\n"] + ms_objs
    for pid in sorted(plates):
        ms.append("  <plate>\n")
        ms.append(f'    <metadata key="plater_id" value="{pid}"/>\n')
        ms.append(f'    <metadata key="plater_name" value="{esc((plate_names or {}).get(pid, ""))}"/>\n')
        ms.append('    <metadata key="locked" value="false"/>\n')
        for o, idn in plates[pid]:
            ms.append('    <model_instance>\n'
                      f'      <metadata key="object_id" value="{o}"/>\n'
                      '      <metadata key="instance_id" value="0"/>\n'
                      f'      <metadata key="identify_id" value="{idn}"/>\n'
                      '    </model_instance>\n')
        ms.append("  </plate>\n")
    ms.append("</config>\n")

    meta = ref_for_shell.meta()
    if strip_design_meta:
        for k in DESIGN_META:
            meta.pop(k, None)
    meta.update(meta_override or {})
    meta.pop("Thumbnail_Middle", None)
    meta.pop("Thumbnail_Small", None)
    mm = [HEAD,
          '<model unit="millimeter" xml:lang="en-US" '
          f'xmlns="{CORE}" xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
          f'xmlns:p="{PROD}" requiredextensions="p">\n']
    for k, v in meta.items():
        mm.append(f' <metadata name="{esc(k)}">{esc(v)}</metadata>\n')
    mm.append(" <resources>\n")
    mm += res
    mm.append(" </resources>\n")
    mm.append(' <build p:UUID="2c7c17d8-22b5-4d84-8835-1976022ea369">\n')
    mm += build
    mm.append(" </build>\n</model>\n")

    rels_3d = [HEAD, '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n']
    for i, (path, _) in enumerate(mesh_files, 1):
        rels_3d.append(f' <Relationship Target="/{path}" Id="rel-{i}" '
                       'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>\n')
    rels_3d.append("</Relationships>\n")

    aux = ref_for_shell.auxiliaries() if keep_aux else []
    rels = [HEAD, '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n',
            ' <Relationship Target="/3D/3dmodel.model" Id="rel-1" '
            'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>\n']
    thumbs = {"Auxiliaries/.thumbnails/thumbnail_3mf.png":
              ("rel-2", "http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail"),
              "Auxiliaries/.thumbnails/thumbnail_middle.png":
              ("rel-4", "http://schemas.bambulab.com/package/2021/cover-thumbnail-middle"),
              "Auxiliaries/.thumbnails/thumbnail_small.png":
              ("rel-5", "http://schemas.bambulab.com/package/2021/cover-thumbnail-small")}
    for t, (rid, typ) in thumbs.items():
        if t in aux:
            rels.append(f' <Relationship Target="/{t}" Id="{rid}" Type="{typ}"/>\n')
    rels.append("</Relationships>\n")

    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED, compresslevel=8) as z:
        z.writestr("[Content_Types].xml", ref_for_shell.zf.read("[Content_Types].xml"))
        z.writestr("_rels/.rels", "".join(rels))
        z.writestr(MODEL_3D, "".join(mm))
        z.writestr("3D/_rels/3dmodel.model.rels", "".join(rels_3d))
        for path, body in mesh_files:
            z.writestr(path, body)
        z.writestr(PROJECT_SETTINGS, json.dumps(settings, indent=4, ensure_ascii=False))
        z.writestr(MODEL_SETTINGS, "".join(ms))
        z.writestr("Metadata/slice_info.config", SLICE_INFO)
        for a in aux:
            z.writestr(a, ref_for_shell.zf.read(a))
    return out_path
