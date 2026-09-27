# 22 Ratcheted Toothpaste Squeezer (kit)

- file: `Full Plates/22 Ratcheted Toothpaste Squeezer (kit) - PLA x15.3mf`
- reference 3mf: `Other/Toothpaste+Squeezer+4.0.3mf`
- designer: Andrew3d
- material: PLA (Bambu PLA Basic @BBL X1C)
- on the plate: 15 kits (30 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL X1C | 0.2 mm | 0.2 mm | 2 | 15% grid | off | auto_brim | 5/3 |

### Taken from the designer's file
| setting | P1S preset | designer |
|---|---|---|
| `flush_multiplier` | 0.75 | **1** |
| `overhang_threshold_participating_cooling` | ['95%', '95%'] | **95%** |
| `pressure_advance` | ['0.02', '0.02'] | **0.02** |
| `top_solid_infill_flow_ratio` | 1 | **1** |

### Left at the P1S value (designer never changed it on their printer)
| setting | their file | P1S |
|---|---|---|
| `outer_wall_acceleration` | 6000 | **5000** |
| `smooth_coefficient` | 4 | **150** |
| `travel_speed` | 600 | **500** |

## Validation
- Orca slice: passed - 21h 46m 24s, 606.2 g, 481.1 cm3
- per kit: 32.08 cm3
- the designer's own file slices at 31.90 cm3 per copy (101% of that here)
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): tree_support_wall_count, raft_first_layer_expansion

## Advisories (nothing changed)
- Toothpaste Squeezer 4.0.stl: 427 mm2 of steep overhang with air under it (max drop 51.0 mm at z=80 mm) while supports are off in the designer's profile - worth a look at the preview

## Notes
- One kit = body + handle/shaft; the ratchet prints in place inside the body.
- Profile was saved for a P2S, which this Studio doesn't ship; process values kept, machine speeds and accelerations rebased to the P1S.

