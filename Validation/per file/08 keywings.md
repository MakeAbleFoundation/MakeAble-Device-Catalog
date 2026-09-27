# 08 KeyWings

- file: `Full Plates/08 KeyWings - PETG x76.3mf`
- source: https://makerworld.com/en/models/1688156-keywings-for-mobility-needs#profileId-1789186
- reference 3mf: `Key Holder (PETG)/KeyWings+v6+Bambu.3mf`
- designer: AlbertMakes
- material: PETG (PETG P1S Tuned)
- on the plate: 76 copies (76 objects)
- print-time cap: 88 copies fit on the plate; trimmed to 76 to stay under 14 h

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL X1C | 0.2 mm | 0.2 mm | 3 | 20% grid | off | no_brim | 5/3 |

### Taken from the designer's file
| setting | P1S preset | designer |
|---|---|---|
| `bridge_speed` | 50 | **30** |
| `brim_type` | auto_brim | **no_brim** |
| `enable_arc_fitting` | 1 | **0** |
| `enable_prime_tower` | 1 | **0** |
| `inner_wall_line_width` | 0.45 | **0.5** |
| `max_travel_detour_distance` | 0 | **50** |
| `outer_wall_line_width` | 0.42 | **0.5** |
| `outer_wall_speed` | 200 | **100** |
| `overhang_2_4_speed` | 50 | **100** |
| `overhang_3_4_speed` | 30 | **100** |
| `overhang_4_4_speed` | 10 | **100** |
| `overhang_totally_speed` | 10 | **100** |
| `reduce_crossing_wall` | 0 | **1** |
| `skeleton_infill_density` | 15% | **20%** |
| `skin_infill_density` | 15% | **20%** |
| `sparse_infill_density` | 15% | **20%** |
| `tree_support_wall_count` | -1 | **0** |
| `wall_generator` | classic | **arachne** |
| `wall_loops` | 2 | **3** |
| `wall_sequence` | inner wall/outer wall | **outer wall/inner wall** |

### Left at the P1S value (designer never changed it on their printer)
| setting | their file | P1S |
|---|---|---|
| `default_acceleration` | 6000 | **10000** |
| `elefant_foot_compensation` | 0 | **0.15** |
| `flush_multiplier` | 1 | **0.75** |
| `raft_first_layer_expansion` | 2 | **-1** |
| `smooth_coefficient` | 80 | **150** |
| `travel_speed` | 700 | **500** |

## Validation
- Orca slice: passed - 13h 56m 36s, 237.0 g, 189.6 cm3
- per copie: 2.49 cm3
- the designer's own file slices at 2.63 cm3 per copy (95% of that here)
- the model page quotes 4 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): raft_first_layer_expansion

## Advisories (nothing changed)
- Body_05*: tall and narrow (21 mm on a 6 mm footprint) with brim off in the designer's profile

## Notes
- Designer recommends PETG or nylon; brim is deliberately off in their profile.

