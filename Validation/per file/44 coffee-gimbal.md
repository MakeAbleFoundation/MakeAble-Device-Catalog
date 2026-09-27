# 44 Universal Travel Coffee Gimbal (kit)

- file: `Full Plates/44 Universal Travel Coffee Gimbal (kit) - PETG x2.3mf`
- source: https://www.printables.com/model/129329-universal-travel-coffee-gimbal
- source files: `New Devices/universal-travel-coffee-gimbal-model_files/Gimbal.stl`, `New Devices/universal-travel-coffee-gimbal-model_files/Clamp.stl`, `New Devices/universal-travel-coffee-gimbal-model_files/Bolt.stl`, `New Devices/universal-travel-coffee-gimbal-model_files/MPC Washer.stl`
- designer: mobiobi (Printables)
- license: CC BY-NC 4.0
- material: PETG (PETG P1S Tuned)
- on the plate: 2 kits (8 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL X1C | 0.2 mm | 0.2 mm | 4 | 15% grid | some parts, tree(auto) | auto_brim | 5/3 |

### Deliberate changes
- `wall_loops`: 2 -> **4**

### Per-part settings
- Clamp: `enable_support` = **1**, `support_type` = **tree(auto)**, `support_on_build_plate_only` = **1**

## Validation
- Orca slice: passed - 10h 37m 33s, 287.1 g, 229.7 cm3
- per kit: 114.84 cm3
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): tree_support_wall_count, raft_first_layer_expansion

## Advisories (nothing changed)
- Gimbal: 327 mm2 of steep overhang with air under it (max drop 2.0 mm at z=14 mm) while supports are off in the designer's profile - worth a look at the preview
- Bolt: 86 mm2 of steep overhang with air under it (max drop 3.7 mm at z=4 mm) while supports are off in the designer's profile - worth a look at the preview

## Notes
- One kit = gimbal + clamp + bolt + washer. The optional long bolt, nut, cup and flat-surface adapters, vertical gimbal and TPU bar wrap are left out.
- Designer: 4 perimeters, no supports on the gimbal. The clamp has a large overhang in its print orientation, so it alone gets tree supports.
- PETG rather than PLA: it holds hot cups and may sit on a car dashboard.

