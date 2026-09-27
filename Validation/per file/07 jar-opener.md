# 07 OPENSESAME3000 Jar Tool

- file: `Full Plates/07 OPENSESAME3000 Jar Tool - PETG x2.3mf`
- source: https://makerworld.com/en/models/90424-opensesame3000-jar-tool#profileId-96804
- reference 3mf: `Jar Opener (PETG)/opensesame.3mf`
- designer: cartyski
- material: PETG (PETG P1S Tuned)
- on the plate: 2 copies (2 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.12mm Fine @BBL X1C | 0.12 mm | 0.2 mm | 3 | 15% gyroid | off | auto_brim | 5/5 |

### Taken from the designer's file
| setting | P1S preset | designer |
|---|---|---|
| `infill_combination` | 0 | **1** |
| `initial_layer_speed` | 50 | **40** |
| `overhang_totally_speed` | 10 | **50** |
| `sparse_infill_pattern` | grid | **gyroid** |
| `support_on_build_plate_only` | 0 | **1** |
| `support_type` | tree(auto) | **normal(auto)** |
| `tree_support_wall_count` | -1 | **0** |
| `wall_loops` | 2 | **3** |

### Left at the P1S value (designer never changed it on their printer)
| setting | their file | P1S |
|---|---|---|
| `flush_multiplier` | 1 | **0.75** |
| `raft_first_layer_expansion` | 2 | **-1** |
| `top_area_threshold` | 100% | **200%** |

## Validation
- Orca slice: passed - 5h 57m 26s, 147.1 g, 117.7 cm3
- per copie: 58.83 cm3
- the designer's own file slices at 58.94 cm3 per copy (100% of that here)
- the model page quotes 74 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): raft_first_layer_expansion

## Notes
- Linked profile is the PLA one (0.12 mm, 3 walls, 15% gyroid). The designer publishes the same settings as a PETG profile, which is what this file is set up for since the folder says PETG.

