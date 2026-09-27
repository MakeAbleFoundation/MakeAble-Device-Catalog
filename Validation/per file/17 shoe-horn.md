# 17 Quick-Slip Shoe Horn

- file: `Full Plates/17 Quick-Slip Shoe Horn - PETG x12.3mf`
- source: https://makerworld.com/en/models/1024414-quick-slip-shoe-horn#profileId-1006338
- reference 3mf: `Shoe Horn (PETG)/Shoe+Horn+3MF.3mf`
- designer: Stag 3D
- material: PETG (PETG P1S Tuned)
- on the plate: 12 copies (12 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL X1C | 0.2 mm | 0.2 mm | 2 | 15% grid | off | auto_brim | 5/3 |

### Taken from the designer's file
| setting | P1S preset | designer |
|---|---|---|
| `ironing_flow` | 10% | **15%** |

### Left at the P1S value (designer never changed it on their printer)
| setting | their file | P1S |
|---|---|---|
| `flush_multiplier` | 1 | **0.75** |
| `smooth_coefficient` | 4 | **150** |
| `sparse_infill_speed` | 350 | **270** |
| `travel_speed` | 1000 | **500** |

## Validation
- Orca slice: passed - 11h 46m 18s, 296.5 g, 237.2 cm3
- per copie: 19.76 cm3
- the model page quotes 25 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): tree_support_wall_count, raft_first_layer_expansion

## Notes
- Designer: PETG or stronger is required.
- Profile came from an H2S; speeds and accelerations rebased to the P1S.

