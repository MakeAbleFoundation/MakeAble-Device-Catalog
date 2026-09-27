# 47 Shoe Lifter / Boot Jack

- file: `Full Plates/47 Shoe Lifter - Boot Jack - PLA x2.3mf`
- source: https://makerworld.com/en/models/1040127-shoe-lifter-boot-jack#profileId-1024783
- reference 3mf: `New Devices/SchuhauszieherV2 (1).3mf`
- designer: Chio97
- license: MakerWorld Standard Digital File License
- material: PLA (Bambu PLA Basic @BBL X1C)
- on the plate: 2 copies (2 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL X1C | 0.2 mm | 0.2 mm | 2 | 15% grid | off | auto_brim | 4/4 |

### Taken from the designer's file
| setting | P1S preset | designer |
|---|---|---|
| `bottom_shell_layers` | 3 | **4** |
| `outer_wall_speed` | 200 | **100** |
| `overhang_totally_speed` | 10 | **50** |
| `support_type` | tree(auto) | **normal(auto)** |
| `top_shell_layers` | 5 | **4** |
| `tree_support_wall_count` | -1 | **0** |

### Left at the P1S value (designer never changed it on their printer)
| setting | their file | P1S |
|---|---|---|
| `flush_multiplier` | 1 | **0.75** |
| `raft_first_layer_expansion` | 2 | **-1** |
| `top_area_threshold` | 100% | **200%** |

## Validation
- Orca slice: passed - 7h 34m 35s, 282.3 g, 224.1 cm3
- per copie: 112.03 cm3
- the designer's own file slices at 111.71 cm3 per copy (100% of that here)
- the model page quotes 141 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): raft_first_layer_expansion

## Advisories (nothing changed)
- SchuhauszieherV2.stl_A_A: 11300 mm2 of steep overhang with air under it (max drop 92.0 mm at z=92 mm) while supports are off in the designer's profile - worth a look at the preview

## Notes
- The designer's 'ohne Support' (no supports) profile; they state it prints without supports. A with-supports profile exists on the page.

