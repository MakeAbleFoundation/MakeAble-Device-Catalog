# 32 Toothpaste Squeezer, external gear (kit)

- file: `Full Plates/32 Toothpaste Squeezer, external gear (kit) - PLA x8.3mf`
- source: https://makerworld.com/en/models/2423006-toothpaste-squeezer-external-gear#profileId-2657457
- reference 3mf: `New Devices/ToothSqeez_ExterGear_SeigaihaPattern.3mf`
- designer: Tazio design
- license: MakerWorld Standard Digital File License
- material: PLA (Bambu PLA Basic @BBL X1C)
- on the plate: 8 kits (24 objects)
- print-time cap: 10 kits fit on the plate; trimmed to 8 to stay under 14 h

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL X1C | 0.2 mm | 0.2 mm | 3 | 15%/25% grid/gyroid | off | auto_brim | 5/3 |

### Taken from the designer's file
| setting | P1S preset | designer |
|---|---|---|
| `bottom_shell_thickness` | 0 | **1** |
| `skeleton_infill_density` | 15% | **25%** |
| `skin_infill_density` | 15% | **25%** |
| `sparse_infill_density` | 15% | **25%** |
| `wall_loops` | 2 | **3** |

### Left at the P1S value (designer never changed it on their printer)
| setting | their file | P1S |
|---|---|---|
| `curr_bed_type` | Supertack Plate | **Textured PEI Plate** |
| `flush_multiplier` | 1 | **0.75** |

## Validation
- Orca slice: passed - 13h 55m 52s, 323.4 g, 256.6 cm3
- per kit: 32.08 cm3
- the designer's own file slices at 32.17 cm3 per copy (100% of that here)
- the model page quotes 42 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): tree_support_wall_count, raft_first_layer_expansion

## Advisories (nothing changed)
- Squeezer base (Seigaiha pattern): 186 mm2 of steep overhang with air under it (max drop 57.0 mm at z=60 mm) while supports are off in the designer's profile - worth a look at the preview
- Key shaft 0.7 mm (standard): 100 mm2 of steep overhang with air under it (max drop 3.9 mm at z=6 mm) while supports are off in the designer's profile - worth a look at the preview

## Notes
- One kit = base + key head + the 0.7 mm 'Standard' key shaft. The designer also offers 1.0, 1.3 and 1.6 mm shafts for thicker tube ends (left out).
- The key parts keep the designer's own 15% gyroid; the base uses their 3 walls, 25% grid.
- Designer: PLA, PLA+, PETG or ASA - not silk PLA, which cracks at the key.

