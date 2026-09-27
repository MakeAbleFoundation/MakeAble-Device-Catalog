# 34 Soup Can Opener (no magnets)

- file: `Full Plates/34 Soup Can Opener (no magnets) - PETG x12.3mf`
- source: https://makerworld.com/en/models/1030162-soup-can-opener-for-poor-grip-strength#profileId-1012846
- reference 3mf: `New Devices/Soup+Can+Opener+-+no+pause+for+magnets.3mf`
- designer: Makerneer
- license: CC0
- material: PETG (PETG P1S Tuned)
- on the plate: 12 copies (12 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Strength @BBL X1C | 0.2 mm | 0.2 mm | 4 | 30% adaptivecubic | off | auto_brim | 5/5 |

### Taken from the designer's file
| setting | P1S preset | designer |
|---|---|---|
| `bottom_shell_layers` | 3 | **5** |
| `fuzzy_skin_point_distance` | 0.8 | **0.6** |
| `infill_wall_overlap` | 15% | **33%** |
| `initial_layer_infill_speed` | 105 | **35** |
| `initial_layer_speed` | 50 | **35** |
| `line_width` | 0.42 | **0.48** |
| `outer_wall_line_width` | 0.42 | **0.48** |
| `overhang_totally_speed` | 10 | **50** |
| `sparse_infill_density` | 25% | **30%** |
| `sparse_infill_pattern` | grid | **adaptivecubic** |
| `support_type` | tree(auto) | **normal(auto)** |
| `top_surface_line_width` | 0.42 | **0.48** |
| `tree_support_wall_count` | -1 | **0** |
| `wall_generator` | classic | **arachne** |
| `wall_loops` | 6 | **4** |

### Left at the P1S value (designer never changed it on their printer)
| setting | their file | P1S |
|---|---|---|
| `flush_multiplier` | 1 | **0.75** |
| `raft_first_layer_expansion` | 2 | **-1** |
| `top_area_threshold` | 100% | **200%** |

## Validation
- Orca slice: passed - 6h 12m 36s, 143.7 g, 115.0 cm3
- per copie: 9.58 cm3
- the designer's own file slices at 9.82 cm3 per copy (98% of that here)
- the model page quotes 13 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): raft_first_layer_expansion

## Advisories (nothing changed)
- Soup Can Opener v5.stl: 235 mm2 of steep overhang with air under it (max drop 3.7 mm at z=5 mm) while supports are off in the designer's profile - worth a look at the preview

## Notes
- The designer printed it in Bambu PETG HF, so PETG it is.
- The 'no magnets' profile: no pause, the magnet holes stay empty.

