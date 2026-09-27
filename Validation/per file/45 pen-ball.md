# 45 Pen Ball (kit)

- file: `Full Plates/45 Pen Ball (kit) - PETG x4.3mf`
- source: https://www.thingiverse.com/thing:2810069
- source files: `New Devices/Pen Ball - 2810069/files/Pen_Ball_Top_v.1.0.0.STL`, `New Devices/Pen Ball - 2810069/files/Pen_Ball_Bottom_v.1.0.0.stl`
- designer: makersmakingchange (Thingiverse)
- license: CC BY-NC-SA
- material: PETG (PETG P1S Tuned)
- on the plate: 4 kits (8 objects)
- print-time cap: 6 kits fit on the plate; trimmed to 4 to stay under 14 h
- also needed: 5 x #6-32 x 3/4 in round-head screws + 5 x #6-32 hex nuts per ball

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL X1C | 0.2 mm | 0.2 mm | 2 | 50% grid | on tree(auto) | auto_brim | 5/3 |

### Deliberate changes
- `enable_support`: 0 -> **1**
- `skeleton_infill_density`: 15% -> **50%**
- `skin_infill_density`: 15% -> **50%**
- `sparse_infill_density`: 15% -> **50%**
- `support_on_build_plate_only`: 0 -> **1**

## Validation
- Orca slice: passed - 11h 36m 55s, 261.4 g, 209.1 cm3
- per kit: 52.28 cm3
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): tree_support_wall_count, raft_first_layer_expansion

## Notes
- Designer's spec sheet: 0.2 mm layers, 50% infill, supports only in the centre cavity, both halves printed together. Build-plate-only supports reach just that cavity.
- Designer used ABS; PETG is the closest of the two filaments here.

