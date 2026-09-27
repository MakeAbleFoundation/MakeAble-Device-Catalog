# 37 Plug Puller (WATAP)

- file: `Full Plates/37 Plug Puller (WATAP) - PLA x9.3mf`
- source: https://makerworld.com/en/models/421822-plug-puller-assistive-technology-by-watap#profileId-324742
- reference 3mf: `New Devices/Plug+Puller+by+WATAP.3mf`
- designer: WATAP_3D
- license: CC BY-NC-SA
- material: PLA (Bambu PLA Basic @BBL X1C)
- on the plate: 9 copies (9 objects)
- also needed: 2 small zip ties (about 15 cm / 6 in) per puller

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Strength @BBL X1C | 0.2 mm | 0.2 mm | 3 | 25% gyroid | off | auto_brim | 5/3 |

### Taken from the designer's file
| setting | P1S preset | designer |
|---|---|---|
| `overhang_totally_speed` | 10 | **50** |
| `sparse_infill_pattern` | grid | **gyroid** |
| `support_type` | tree(auto) | **normal(manual)** |
| `tree_support_wall_count` | -1 | **0** |
| `wall_loops` | 6 | **3** |

### Left at the P1S value (designer never changed it on their printer)
| setting | their file | P1S |
|---|---|---|
| `flush_multiplier` | 1 | **0.75** |
| `raft_first_layer_expansion` | 2 | **-1** |
| `top_area_threshold` | 100% | **200%** |

## Validation
- Orca slice: passed - 2h 59m 51s, 84.2 g, 66.8 cm3
- per copie: 7.42 cm3
- the designer's own file slices at 7.59 cm3 per copy (98% of that here)
- the model page quotes 10 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): raft_first_layer_expansion

## Advisories (nothing changed)
- Plug Puller WATAP.stl: 156 mm2 of steep overhang with air under it (max drop 0.8 mm at z=1 mm) while supports are off in the designer's profile - worth a look at the preview

## Notes
- The designer's variable layer height is kept.

