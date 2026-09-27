# 14 Flipper Nail Clipper (large clippers)

- file: `Full Plates/14 Flipper Nail Clipper (large clippers) - PLA x3.3mf`
- source: https://makerworld.com/en/models/47915-flipper-the-one-handed-nail-clipper-adjusted-for-l
- reference 3mf: `Nail Clipper Holder (PLA)/Flipper+Clipper+mod+for+large+size+nailcutter_a1mini.3mf`
- designer: saad.caffeine
- material: PLA (Bambu PLA Basic @BBL X1C)
- on the plate: 3 copies (3 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL X1C | 0.2 mm | 0.2 mm | 2 | 15% grid | off | auto_brim | 5/3 |

### Taken from the designer's file
| setting | P1S preset | designer |
|---|---|---|
| `overhang_totally_speed` | 10 | **19** |
| `support_type` | tree(auto) | **normal(auto)** |
| `tree_support_wall_count` | -1 | **0** |

### Left at the P1S value (designer never changed it on their printer)
| setting | their file | P1S |
|---|---|---|
| `default_acceleration` | 6000 | **10000** |
| `elefant_foot_compensation` | 0 | **0.15** |
| `flush_multiplier` | 1 | **0.75** |
| `raft_first_layer_expansion` | 2 | **-1** |
| `smooth_coefficient` | 80 | **150** |
| `top_area_threshold` | 100% | **200%** |
| `travel_speed` | 700 | **500** |

## Validation
- Orca slice: passed - 2h 21m 17s, 90.8 g, 72.1 cm3
- per copie: 24.02 cm3
- the designer's own file slices at 23.96 cm3 per copy (100% of that here)
- the model page quotes 30 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): raft_first_layer_expansion

## Advisories (nothing changed)
- Flipper Clipper mod for large size nailcutter.stl: 522 mm2 of steep overhang with air under it (max drop 6.0 mm at z=8 mm) while supports are off in the designer's profile - worth a look at the preview

## Notes
- Print-in-place hinge: the two bodies stay in one object, as the designer had it.
- Designer notes PETG works better than PLA; folder says PLA, so PLA it is.

