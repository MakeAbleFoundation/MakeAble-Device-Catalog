# 11 Pill Popper

- file: `Full Plates/11 Pill Popper - PETG x21.3mf`
- source: https://makerworld.com/en/models/1440419-pill-popper#profileId-1499190
- reference 3mf: `Pill Popper (PETG)/Pill+Popper+Bambu+Studio.3mf`
- designer: AlbertMakes
- material: PETG (PETG P1S Tuned)
- on the plate: 21 copies (21 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Strength @BBL X1C | 0.2 mm | 0.2 mm | 6 | 25% grid | off | auto_brim | 5/3 |

### Taken from the designer's file
| setting | P1S preset | designer |
|---|---|---|
| `bridge_speed` | 50 | **30** |
| `initial_layer_speed` | 50 | **20** |
| `tree_support_wall_count` | -1 | **0** |

### Left at the P1S value (designer never changed it on their printer)
| setting | their file | P1S |
|---|---|---|
| `curr_bed_type` | High Temp Plate | **Textured PEI Plate** |
| `default_acceleration` | 6000 | **10000** |
| `elefant_foot_compensation` | 0 | **0.15** |
| `flush_multiplier` | 1 | **0.75** |
| `raft_first_layer_expansion` | 2 | **-1** |
| `smooth_coefficient` | 80 | **150** |
| `travel_speed` | 700 | **500** |

## Validation
- Orca slice: passed - 8h 22m 50s, 165.8 g, 132.6 cm3
- per copie: 6.32 cm3
- the designer's own file slices at 6.29 cm3 per copy (100% of that here)
- the model page quotes 9 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): raft_first_layer_expansion

## Advisories (nothing changed)
- Body_08*2: 247 mm2 of steep overhang with air under it (max drop 3.6 mm at z=4 mm) while supports are off in the designer's profile - worth a look at the preview

## Notes
- Model page asks for a very slow first layer: the profile's 20 mm/s is kept.
- Page says 10-15% infill, the profile says 25%; the profile wins, as agreed.

