# 06 Assistive Can Tab Opener

- file: `Full Plates/06 Assistive Can Tab Opener - PLA x30.3mf`
- source: https://makerworld.com/en/models/1797256-assistive-can-tab-opener#profileId-1916191
- reference 3mf: `Can Opener (PLA)/Base_Can_Opener.3mf`
- designer: MakeAble
- material: PLA (Bambu PLA Basic @BBL X1C)
- on the plate: 30 copies (30 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL X1C | 0.2 mm | 0.2 mm | 2 | 50% grid | on tree(auto) | auto_brim | 5/3 |

### Taken from the designer's file
| setting | P1S preset | designer |
|---|---|---|
| `enable_support` | 0 | **1** |
| `skeleton_infill_density` | 15% | **50%** |
| `skin_infill_density` | 15% | **50%** |
| `sparse_infill_density` | 15% | **50%** |

### Left at the P1S value (designer never changed it on their printer)
| setting | their file | P1S |
|---|---|---|
| `flush_multiplier` | 0.62 | **0.75** |

## Validation
- Orca slice: passed - 11h 8m 48s, 358.8 g, 284.7 cm3
- per copie: 9.49 cm3
- the designer's own file slices at 9.57 cm3 per copy (99% of that here)
- the model page quotes 12 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): tree_support_wall_count, raft_first_layer_expansion

