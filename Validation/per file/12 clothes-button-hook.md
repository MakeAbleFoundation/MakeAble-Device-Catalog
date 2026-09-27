# 12 Clothes Button & Zipper Hook (hook, PETG)

- file: `Full Plates/12 Clothes Button & Zipper Hook (hook, PETG) - PETG x9.3mf`
- source: https://makerworld.com/en/models/423231-clothes-button-and-zipper-hook-helper
- reference 3mf: `Clothes Button and Zipper Aid (PETG + PLA)/central-loop-and-hook-button-and-zipper-hook.3mf`
- designer: Adapt3D_OT
- material: PETG (PETG P1S Tuned)
- on the plate: 9 copies (9 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Strength @BBL X1C | 0.2 mm | 0.2 mm | 6 | 25% gyroid | off | auto_brim | 5/3 |

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
- Orca slice: passed - 1h 43m 51s, 37.9 g, 30.3 cm3
- per copie: 3.37 cm3
- the designer's own file slices at 3.50 cm3 per copy (96% of that here)
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): raft_first_layer_expansion

## Notes
- Designer: print the central piece in PETG so it keeps its shape.
- This mesh carries the designer's painted seams, which are preserved.

