# 04 Bottle Cap Opener

- file: `Full Plates/04 Bottle Cap Opener - PETG x8.3mf`
- source: https://makerworld.com/en/models/1093642-bottle-cap-opener#profileId-1087614
- reference 3mf: `Bottle Opener (PETG)/Bottle+Cap+Opener.3mf`
- designer: TuTu
- material: PETG (PETG P1S Tuned)
- on the plate: 8 copies (8 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL X1C | 0.2 mm | 0.15 mm | 5 | 50% grid | off | auto_brim | 3/5 |

### Taken from the designer's file
| setting | P1S preset | designer |
|---|---|---|
| `bottom_shell_layers` | 3 | **5** |
| `initial_layer_infill_speed` | 105 | **50** |
| `initial_layer_print_height` | 0.2 | **0.15** |
| `inner_wall_speed` | 300 | **250** |
| `outer_wall_speed` | 200 | **150** |
| `overhang_totally_speed` | 10 | **19** |
| `sparse_infill_density` | 15% | **50%** |
| `sparse_infill_speed` | 270 | **250** |
| `support_type` | tree(auto) | **normal(auto)** |
| `top_shell_layers` | 5 | **3** |
| `top_shell_thickness` | 1.0 | **0.6** |
| `tree_support_wall_count` | -1 | **1** |
| `wall_loops` | 2 | **5** |

### Left at the P1S value (designer never changed it on their printer)
| setting | their file | P1S |
|---|---|---|
| `default_acceleration` | 6000 | **10000** |
| `flush_multiplier` | 1 | **0.75** |
| `raft_first_layer_expansion` | 2 | **-1** |
| `smooth_coefficient` | 80 | **150** |
| `top_area_threshold` | 100% | **200%** |
| `travel_speed` | 700 | **500** |

## Validation
- Orca slice: passed - 7h 1m 48s, 166.0 g, 132.8 cm3
- per copie: 16.60 cm3
- the designer's own file slices at 16.68 cm3 per copy (99% of that here)
- the model page quotes 22 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): raft_first_layer_expansion

## Notes
- Designer's profile: 0.15 mm first layer, 5 walls, 50% infill, slower walls (was an A1 mini profile, rebased onto the P1S).

