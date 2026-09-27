# 40 Adjustable Cane Holder (kit)

- file: `Full Plates/40 Adjustable Cane Holder (kit) - PLA x6.3mf`
- source: https://www.printables.com/model/203631-adjustable-cane-holder
- source files: `New Devices/adjustable-cane-holder-model_files/Recommended Print Files/texture_on_cane_holder_v3.stl`, `New Devices/adjustable-cane-holder-model_files/Recommended Print Files/alt_screw_updates.stl`, `New Devices/adjustable-cane-holder-model_files/Recommended Print Files/clamp_protector_tri.stl`
- designer: newhouse24 (Printables)
- license: CC BY-NC-SA 4.0
- material: PLA (Bambu PLA Basic @BBL X1C)
- on the plate: 6 kits (18 objects)
- print-time cap: 10 kits fit on the plate; trimmed to 6 to stay under 14 h

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL X1C | 0.2 mm | 0.2 mm | 2 | 60% grid | on tree(auto) | auto_brim/outer_only | 5/3 |

### Deliberate changes
- `enable_support`: 0 -> **1**
- `skeleton_infill_density`: 15% -> **60%**
- `skin_infill_density`: 15% -> **60%**
- `sparse_infill_density`: 15% -> **60%**
- `support_base_pattern_spacing`: 2.5 -> **4**
- `support_on_build_plate_only`: 0 -> **1**

### Per-part settings
- Clamp screw (easy grip): `brim_type` = **outer_only**, `brim_width` = **5**

## Validation
- Orca slice: passed - 12h 45m 2s, 413.3 g, 328.0 cm3
- per kit: 54.66 cm3
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): tree_support_wall_count, raft_first_layer_expansion

## Notes
- The page's 'Recommended Print Files': textured holder, easy-grip screw, textured clamp protector.
- Designer's stated settings: 60% infill, supports touching the build plate at about 10% density (support line spacing 4 mm), a brim for the screw. Everything else is the P1S 0.20 mm Standard.

