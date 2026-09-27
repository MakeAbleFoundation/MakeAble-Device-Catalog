# 36 Younger Grip Lid Wrench (glue-in magnets)

- file: `Full Plates/36 Younger Grip Lid Wrench (glue-in magnets) - PLA x8.3mf`
- source: https://makerworld.com/en/models/1493731-younger-grip-lid-wrench-arthritis-aid#profileId-1572541
- reference 3mf: `New Devices/PRJ___YOUNGER+GRIP_Glue-in+Magnets_.3mf`
- designer: SFYoung
- license: MakerWorld Standard Digital File License
- material: PLA (Bambu PLA Basic @BBL X1C)
- on the plate: 8 copies (8 objects)
- also needed: optional: 2 x 8x2 mm (or 8x3 mm) round magnets per grip, glued in after printing

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL X1C | 0.2 mm | 0.2 mm | 3 | 10% gyroid | off | auto_brim | 5/3 |

### Taken from the designer's file
| setting | P1S preset | designer |
|---|---|---|
| `skeleton_infill_density` | 15% | **10%** |
| `skin_infill_density` | 15% | **10%** |
| `sparse_infill_density` | 15% | **10%** |
| `sparse_infill_pattern` | grid | **gyroid** |
| `top_surface_pattern` | monotonicline | **monotonic** |
| `tree_support_wall_count` | -1 | **0** |
| `wall_generator` | classic | **arachne** |
| `wall_loops` | 2 | **3** |

### Left at the P1S value (designer never changed it on their printer)
| setting | their file | P1S |
|---|---|---|
| `flush_multiplier` | 1 | **0.75** |
| `raft_first_layer_expansion` | 2 | **-1** |

## Validation
- Orca slice: passed - 9h 25m 5s, 258.3 g, 205.0 cm3
- per copie: 25.63 cm3
- the designer's own file slices at 25.87 cm3 per copy (99% of that here)
- the model page quotes 33 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): raft_first_layer_expansion

## Advisories (nothing changed)
- YOUNGER__GRIP_Glue In Magnets_.stl: 346 mm2 of steep overhang with air under it (max drop 15.4 mm at z=15 mm) while supports are off in the designer's profile - worth a look at the preview

## Notes
- The designer's single-colour 'glue-in magnets' plate: no pause, the magnet pockets stay open.
- Their height-range layer settings are kept: 0.12 mm layers over the finger-well overhang, 0.24 mm for the bridge above it, 0.2 mm elsewhere.

