# 33 Chopstick Helper (small)

- file: `Full Plates/33 Chopstick Helper (small) - PLA x48.3mf`
- source: https://makerworld.com/en/models/1088273-chopstick-helper-refreshed-design#profileId-1082781
- reference 3mf: `New Devices/chopstick_helper_new_design_PLA_Small.3mf`
- designer: Daranto
- license: MakerWorld Standard Digital File License
- material: PLA (Bambu PLA Basic @BBL X1C)
- on the plate: 48 copies (48 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL X1C | 0.2 mm | 0.2 mm | 6 | 100% zig-zag | off | auto_brim | 1/1 |

### Taken from the designer's file
| setting | P1S preset | designer |
|---|---|---|
| `bottom_shell_layers` | 3 | **1** |
| `bottom_surface_pattern` | monotonic | **concentric** |
| `overhang_totally_speed` | 10 | **50** |
| `seam_position` | aligned | **back** |
| `sparse_infill_density` | 15% | **100%** |
| `sparse_infill_pattern` | grid | **zig-zag** |
| `support_type` | tree(auto) | **normal(auto)** |
| `top_shell_layers` | 5 | **1** |
| `top_surface_pattern` | monotonicline | **concentric** |
| `tree_support_wall_count` | -1 | **0** |
| `wall_loops` | 2 | **6** |

### Left at the P1S value (designer never changed it on their printer)
| setting | their file | P1S |
|---|---|---|
| `flush_multiplier` | 1 | **0.75** |
| `raft_first_layer_expansion` | 2 | **-1** |
| `top_area_threshold` | 100% | **200%** |

## Validation
- Orca slice: passed - 6h 18m 45s, 149.2 g, 118.4 cm3
- per copie: 2.47 cm3
- the designer's own file slices at 2.48 cm3 per copy (99% of that here)
- the model page quotes 4 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): raft_first_layer_expansion

## Advisories (nothing changed)
- chopstick_helper_smooth.stl: 115 mm2 of steep overhang with air under it (max drop 6.1 mm at z=8 mm) while supports are off in the designer's profile - worth a look at the preview

## Notes
- Small size: 6.12 mm holes. Medium (6.80 mm) and large (7.75 mm) exist on the page.
- Designer's profile: 6 walls, 100% infill.

