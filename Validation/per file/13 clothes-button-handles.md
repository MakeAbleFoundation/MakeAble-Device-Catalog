# 13 Clothes Button & Zipper Hook (handle kit, PLA)

- file: `Full Plates/13 Clothes Button & Zipper Hook (handle kit, PLA) - PLA x8.3mf`
- source: https://makerworld.com/en/models/423231-clothes-button-and-zipper-hook-helper
- reference 3mf: `Clothes Button and Zipper Aid (PETG + PLA)/central-loop-and-hook-button-and-zipper-hook.3mf`
- designer: Adapt3D_OT
- material: PLA (Bambu PLA Basic @BBL X1C)
- on the plate: 8 kits (32 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Strength @BBL X1C | 0.2 mm | 0.2 mm | 3/6 | 25% gyroid | off | auto_brim | 5/3 |

### Taken from the designer's file
| setting | P1S preset | designer |
|---|---|---|
| `overhang_totally_speed` | 10 | **50** |
| `sparse_infill_pattern` | grid | **gyroid** |
| `support_type` | tree(auto) | **normal(auto)** |
| `tree_support_wall_count` | -1 | **0** |

### Left at the P1S value (designer never changed it on their printer)
| setting | their file | P1S |
|---|---|---|
| `flush_multiplier` | 1 | **0.75** |
| `raft_first_layer_expansion` | 2 | **-1** |
| `top_area_threshold` | 100% | **200%** |

## Validation
- Orca slice: passed - 4h 3m 50s, 98.6 g, 78.3 cm3
- per kit: 9.79 cm3
- the designer's own file slices at 9.81 cm3 per copy (100% of that here)
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): raft_first_layer_expansion

## Advisories (nothing changed)
- Handle+scales.stl: 1157 mm2 of steep overhang with air under it (max drop 5.0 mm at z=5 mm) while supports are off in the designer's profile - worth a look at the preview

## Notes
- One kit = 2 handle scales + 2 connector pins, which is what one hook needs.
- Pins are the designer's 95%-scaled version from the 3mf, not the loose STL.

