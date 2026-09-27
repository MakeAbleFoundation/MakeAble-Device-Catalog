# 15 Flipper the Clipper v2 (Thingiverse)

- file: `Full Plates/15 Flipper the Clipper v2 (Thingiverse) - PLA x4.3mf`
- source: https://www.thingiverse.com/thing:5637570
- reference 3mf: `Nail Clipper Holder (PLA)/Nailcutter_v2.stl`
- designer: kafei
- material: PLA (Bambu PLA Basic @BBL X1C)
- on the plate: 4 copies (4 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL X1C | 0.2 mm | 0.2 mm | 2 | 80% grid | off | auto_brim | 5/3 |

### Deliberate changes
- `skeleton_infill_density`: 15% -> **80%**
- `skin_infill_density`: 15% -> **80%**
- `sparse_infill_density`: 15% -> **80%**

## Validation
- Orca slice: passed - 4h 19m 31s, 184.0 g, 146.0 cm3
- per copie: 36.50 cm3
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): tree_support_wall_count, raft_first_layer_expansion

## Advisories (nothing changed)
- Flipper the Clipper v2 (Thingiverse): 452 mm2 of steep overhang with air under it (max drop 6.0 mm at z=8 mm) while supports are off in the designer's profile - worth a look at the preview

## Notes
- No designer 3mf exists, so this is the P1S 0.20 mm Standard profile plus the designer's one stated requirement: 80% infill.

