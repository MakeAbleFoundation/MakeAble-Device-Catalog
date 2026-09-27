# 10 Blister Pack Opener

- file: `Full Plates/10 Blister Pack Opener - PETG x8.3mf`
- source: https://makerworld.com/en/models/1791626-blister-pack-opener#profileId-1909450
- reference 3mf: `Pill Popper (PETG)/Pill+Opener.3mf`
- designer: MakeAble
- material: PETG (PETG P1S Tuned)
- on the plate: 8 copies (8 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL X1C | 0.2 mm | 0.2 mm | 5 | 17% crosshatch | on tree(auto) | outer_only | 6/6 |

### Taken from the designer's file
| setting | P1S preset | designer |
|---|---|---|
| `bottom_shell_layers` | 3 | **6** |
| `brim_type` | auto_brim | **outer_only** |
| `enable_support` | 0 | **1** |
| `sparse_infill_density` | 15% | **17%** |
| `sparse_infill_pattern` | grid | **crosshatch** |
| `support_remove_small_overhang` | 1 | **0** |
| `top_shell_layers` | 5 | **6** |
| `wall_loops` | 2 | **5** |

### Left at the P1S value (designer never changed it on their printer)
| setting | their file | P1S |
|---|---|---|
| `flush_multiplier` | 1 | **0.75** |

## Validation
- Orca slice: passed - 10h 27m 58s, 251.1 g, 200.9 cm3
- per copie: 25.11 cm3
- the designer's own file slices at 26.09 cm3 per copy (96% of that here)
- the model page quotes 33 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): tree_support_wall_count, raft_first_layer_expansion

## Notes
- Tree supports and an outer brim are part of the designer's profile.

