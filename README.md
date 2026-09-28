# MakeAble assistive devices - print files for the Bambu Lab P1S

Every file here is set up for a **Bambu Lab P1S, 0.4 nozzle, textured PEI plate**, saved in Bambu Studio 2.2.2 format. Open one, check the plate, hit slice. Nothing needs to be re-arranged or re-configured.

## Printer this is for

| | |
|---|---|
| Printer | Bambu Lab **P1S** (256 x 256 x 256 mm build volume) |
| Nozzle | 0.4 mm hardened/stainless (stock) |
| Build plate | Textured PEI |
| Slicer | Bambu Studio 2.2.2 or newer (OrcaSlicer 2.4.2 also opens them) |
| Filaments | PLA (`Bambu PLA Basic @BBL X1C`) and PETG (`PETG P1S Tuned`) - one per plate |

These files are **not** for the A1, A1 mini, X1C, P2S or H2 series without re-checking: the machine settings, bed shape and the P1S's front-left bed exclusion area are baked into every plate. On another printer, re-select the machine preset in Studio and re-check part placement before slicing.

## Repository layout

- `Full Plates/` - one file per device, filled with as many copies as fit.
- `Catalogue - one device per plate.3mf` - devices 01-30, each on its own plate, one copy each, same settings.
- `Catalogue 2 - one device per plate.3mf` - devices 31-48, each on its own plate, one copy each, same settings.
- `Validation/` - what was checked, per file, plus plate previews. `Validation/tools/` holds the Python scripts that built and checked the plates.

## Full plates

| # | file | material | per plate | print time | filament | layer | walls | infill | supports | vs designer's file |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | 01 Bag Carrier (Medium) - PLA x4.3mf | PLA | 4 copies | 3h 0m 37s | 125.0 g | 0.2 mm | 2 | 15% | no | 100% |
| 02 | 02 Bag Carrier (Small) - PLA x4.3mf | PLA | 4 copies | 2h 41m 50s | 112.0 g | 0.2 mm | 2 | 15% | no | - |
| 03 | 03 Bag Carrier (Large) - PLA x2.3mf | PLA | 2 copies | 1h 49m 24s | 79.0 g | 0.2 mm | 2 | 15% | no | - |
| 04 | 04 Bottle Cap Opener - PETG x8.3mf | PETG | 8 copies | 7h 1m 48s | 166.0 g | 0.2 mm | 5 | 50% | no | 99% |
| 05 | 05 Bottle Opener (three sizes, wide handle) - PETG x4.3mf | PETG | 4 copies | 6h 46m 6s | 141.0 g | 0.2 mm | 5 | 15% | yes | 96% |
| 06 | 06 Assistive Can Tab Opener - PLA x30.3mf | PLA | 30 copies | 11h 8m 48s | 359.0 g | 0.2 mm | 2 | 50% | yes | 99% |
| 07 | 07 OPENSESAME3000 Jar Tool - PETG x2.3mf | PETG | 2 copies | 5h 57m 26s | 147.0 g | 0.12 mm | 3 | 15% | no | 100% |
| 08 | 08 KeyWings - PETG x76.3mf | PETG | 76 copies | 13h 56m 36s | 237.0 g | 0.2 mm | 3 | 20% | no | 95% |
| 09 | 09 DRAG Assistive Writer (kit of 3) - PLA x2.3mf | PLA | 2 kits | 3h 39m 32s | 146.0 g | 0.2 mm | 2 | 15% | no | 100% |
| 10 | 10 Blister Pack Opener - PETG x8.3mf | PETG | 8 copies | 10h 27m 58s | 251.0 g | 0.2 mm | 5 | 17% | yes | 96% |
| 11 | 11 Pill Popper - PETG x21.3mf | PETG | 21 copies | 8h 22m 50s | 166.0 g | 0.2 mm | 6 | 25% | no | 100% |
| 12 | 12 Clothes Button & Zipper Hook (hook, PETG) - PETG x9.3mf | PETG | 9 copies | 1h 43m 51s | 38.0 g | 0.2 mm | 6 | 25% | no | 96% |
| 13 | 13 Clothes Button & Zipper Hook (handle kit, PLA) - PLA x8.3mf | PLA | 8 kits | 4h 3m 50s | 99.0 g | 0.2 mm | 3/6 | 25% | no | 100% |
| 14 | 14 Flipper Nail Clipper (large clippers) - PLA x3.3mf | PLA | 3 copies | 2h 21m 17s | 91.0 g | 0.2 mm | 2 | 15% | no | 100% |
| 15 | 15 Flipper the Clipper v2 (Thingiverse) - PLA x4.3mf | PLA | 4 copies | 4h 19m 31s | 184.0 g | 0.2 mm | 2 | 80% | no | - |
| 16 | 16 Eating Utensil Aid (kit) - PLA x5.3mf | PLA | 5 kits | 9h 49m 52s | 231.0 g | 0.2 mm | 2 | 60% | no | 100% |
| 17 | 17 Quick-Slip Shoe Horn - PETG x12.3mf | PETG | 12 copies | 11h 46m 18s | 296.0 g | 0.2 mm | 2 | 15% | no | - |
| 18 | 18 Tuber Opener - PLA x12.3mf | PLA | 12 copies | 6h 51m 19s | 203.0 g | 0.16 mm | 4 | 15% | no | 100% |
| 19 | 19 Arthritis Toothbrush Grip - PLA x19.3mf | PLA | 19 copies | 13h 23m 17s | 599.0 g | 0.2 mm | 2 | 15% | no | - |
| 20 | 20 One-Handed Page Holder - PLA x23.3mf | PLA | 23 copies | 8h 10m 32s | 228.0 g | 0.16 mm | 3 | 15% | no | 100% |
| 21 | 21 Smartphone Magnification Stand - PLA x12.3mf | PLA | 12 copies | 10h 10m 51s | 312.0 g | 0.16 mm | 2 | 15% | no | 100% |
| 22 | 22 Eye Drop Assist pliers (bottle 20 mm) - PLA x2.3mf | PLA | 2 copies | 59m 33s | 29.0 g | 0.2 mm | 2 | 15% | no | - |
| 23 | 23 Eye Drop Assist pliers (bottle 22 mm) - PLA x2.3mf | PLA | 2 copies | 59m 19s | 29.0 g | 0.2 mm | 2 | 15% | no | - |
| 24 | 24 Eye Drop Assist pliers (bottle 24 mm) - PLA x2.3mf | PLA | 2 copies | 58m 59s | 29.0 g | 0.2 mm | 2 | 15% | no | - |
| 25 | 25 Eye Drop Assist pliers (bottle 25 mm) - PLA x2.3mf | PLA | 2 copies | 57m 5s | 28.0 g | 0.2 mm | 2 | 15% | no | - |
| 26 | 26 Eye Drop Assist eyepiece 03 A - PLA x35.3mf | PLA | 35 copies | 5h 5m 14s | 118.0 g | 0.2 mm | 2 | 15% | no | - |
| 27 | 27 Eye Drop Assist eyepiece 03 B - PLA x35.3mf | PLA | 35 copies | 4h 42m 50s | 113.0 g | 0.2 mm | 2 | 15% | no | - |
| 28 | 28 Eye Drop Assist eyepiece 03 C - PLA x35.3mf | PLA | 35 copies | 5h 1m 57s | 122.0 g | 0.2 mm | 2 | 15% | no | - |
| 29 | 29 Eye Drop Assist eyepiece 04 D - PLA x35.3mf | PLA | 35 copies | 5h 41m 16s | 137.0 g | 0.2 mm | 2 | 15% | no | - |
| 30 | 30 Eye Drop Assist eyepiece 04 E - PLA x35.3mf | PLA | 35 copies | 5h 21m 16s | 131.0 g | 0.2 mm | 2 | 15% | no | - |
| 31 | 31 Bedside Hook-On Storage Box (kit) - PLA x1.3mf | PLA | 1 kit | 4h 12m 24s | 229.0 g | 0.2 mm | 2 | 15% | no | 100% |
| 32 | 32 Toothpaste Squeezer, external gear (kit) - PLA x8.3mf | PLA | 8 kits | 13h 55m 52s | 323.0 g | 0.2 mm | 3 | 15%/25% | no | 100% |
| 33 | 33 Chopstick Helper (small) - PLA x48.3mf | PLA | 48 copies | 6h 18m 45s | 149.0 g | 0.2 mm | 6 | 100% | no | 99% |
| 34 | 34 Soup Can Opener (no magnets) - PETG x12.3mf | PETG | 12 copies | 6h 12m 36s | 144.0 g | 0.2 mm | 4 | 30% | no | 98% |
| 35 | 35 Jar Opener - Vacuum Releaser - PLA x8.3mf | PLA | 8 copies | 6h 20m 5s | 161.0 g | 0.24 mm | 2 | 10% | no | - |
| 36 | 36 Younger Grip Lid Wrench (glue-in magnets) - PLA x8.3mf | PLA | 8 copies | 9h 25m 5s | 258.0 g | 0.2 mm | 3 | 10% | no | 99% |
| 37 | 37 Plug Puller (WATAP) - PLA x9.3mf | PLA | 9 copies | 2h 59m 51s | 84.0 g | 0.2 mm | 3 | 25% | no | 98% |
| 38 | 38 Pinky Saver 3 & Phone Stand - PLA x18.3mf | PLA | 18 copies | 5h 8m 33s | 159.0 g | 0.2 mm | 2 | 15% | no | - |
| 39 | 39 Universal Cup Holder (kit) - PLA x1.3mf | PLA | 1 kit | 5h 7m 16s | 202.0 g | 0.2 mm | 6 | 15% | yes | 98% |
| 40 | 40 Adjustable Cane Holder (kit) - PLA x6.3mf | PLA | 6 kits | 12h 45m 2s | 413.0 g | 0.2 mm | 2 | 60% | yes | - |
| 41 | 41 Hand Press - Grip Strengthener (Light) - PETG x5.3mf | PETG | 5 copies | 6h 43m 9s | 194.0 g | 0.2 mm | 4 | 15% | no | 100% |
| 42 | 42 Hand Press - Grip Strengthener (Medium) - PETG x5.3mf | PETG | 5 copies | 7h 33m 56s | 221.0 g | 0.2 mm | 5 | 15% | no | 100% |
| 43 | 43 Hand Press - Grip Strengthener (Hard) - PETG x5.3mf | PETG | 5 copies | 8h 13m 43s | 244.0 g | 0.2 mm | 6 | 15% | no | 100% |
| 44 | 44 Universal Travel Coffee Gimbal (kit) - PETG x2.3mf | PETG | 2 kits | 10h 37m 33s | 287.0 g | 0.2 mm | 4 | 15% | some parts | - |
| 45 | 45 Pen Ball (kit) - PETG x4.3mf | PETG | 4 kits | 11h 36m 55s | 261.0 g | 0.2 mm | 2 | 50% | yes | - |
| 46 | 46 Playing Card Holder (4 rows) - PLA x4.3mf | PLA | 4 copies | 7h 25m 17s | 302.0 g | 0.2 mm | 2 | 15% | no | - |
| 47 | 47 Shoe Lifter - Boot Jack - PLA x2.3mf | PLA | 2 copies | 7h 34m 35s | 282.0 g | 0.2 mm | 2 | 15% | no | 100% |
| 48 | 48 Adaptive Pencil Grip - PLA x7.3mf | PLA | 7 copies | 3h 53m 14s | 143.0 g | 0.2 mm | 2 | 15% | no | - |

All 48 plates together: about 9.0 kg of filament.

The last column is the check that matters: filament per copy on your plate against a slice of the designer's own untouched file. 100% means the part comes out exactly as they set it up. The few at 95-96% are the P1S's elephant-foot compensation shaving the first layer, which their printer profile did not apply. A dash means there is nothing to compare against (loose STLs, or a size variant that shares another file's profile, or a supplied plate, which is its own reference).

## Print-time cap

No plate runs longer than 14 hours (the slicer's estimate). Where a full plate would take longer, it holds fewer copies - the ones in the middle of the plate, kept together:

- **KeyWings**: 76 of the 88 copies that fit (13h 56m 36s)
- **Arthritis Toothbrush Grip**: 19 of the 25 copies that fit (13h 23m 17s)
- **Toothpaste Squeezer, external gear (kit)**: 8 of the 10 kits that fit (13h 55m 52s)
- **Adjustable Cane Holder (kit)**: 6 of the 10 kits that fit (12h 45m 2s)
- **Pen Ball (kit)**: 4 of the 6 kits that fit (11h 36m 55s)

## Catalogue files

A Bambu Studio project holds at most 36 plates, so the one-per-plate catalogue comes in two files.

`Catalogue - one device per plate.3mf` holds 30 plates, one device each, in the same order as the table above. Each plate keeps its own layer height, wall count, infill and support settings - those are baked onto the objects, so switching the process preset in Studio will not silently wipe them.

Filament slot 1 is PLA, slot 2 is PETG, and every plate uses one or the other, so you only ever load one spool per plate.

Three settings cannot vary per plate in Bambu Studio, so the file uses the most conservative value any device asked for:

| setting | catalogue | who wanted something else |
|---|---|---|
| first layer height | 0.2 mm | Bottle Cap Opener's profile uses 0.15 mm |
| first layer speed | 15 mm/s | the slowest any designer asked for (DRAG); others use 20-50 mm/s |
| first layer infill speed | 50 mm/s | slowest of the set |

`Catalogue 2 - one device per plate.3mf` holds 18 plates, one device each, in the same order as the table above. Each plate keeps its own layer height, wall count, infill and support settings - those are baked onto the objects, so switching the process preset in Studio will not silently wipe them.

Three settings cannot vary per plate in Bambu Studio, so the file uses the most conservative value any device asked for:

| setting | catalogue | who wanted something else |
|---|---|---|
| first layer height | 0.2 mm | Jar Opener / Vacuum Releaser's profile uses 0.24 mm |
| first layer speed | 35 mm/s | the slowest any designer asked for (Soup Can Opener); the others use 50 mm/s |
| first layer infill speed | 35 mm/s | slowest of the set |

If you want a device exactly as its designer set it up, use its file in `Full Plates/` - those keep every value.

## Spacing, and the corner the printer cannot use

Parts sit at least 5 mm apart, measured on their real outlines rather than bounding boxes, which is what lets the C-shaped ones nest into each other. Where a profile adds a brim or supports, those reach past the part itself, so the plate is sliced and the spacing widened until the slicer stops reporting conflicting toolpaths:

- **Assistive Can Tab Opener**: 8 mm apart - its tree supports flare out well past the part.
- **Universal Cup Holder (kit)**: 8 mm apart - its tree supports flare out well past the part.
- **Universal Travel Coffee Gimbal (kit)**: 8 mm apart - its tree supports flare out well past the part.

**Pinky Saver 3 & Phone Stand** is a supplied plate, arranged by hand in Bambu Studio and kept exactly as it is: its parts are 3.25 mm apart, 3 mm from the plate edge and 3 mm from the excluded corner. It slices with no conflicting toolpaths.

The P1S cannot print in an 18 x 28 mm patch at the front-left corner (Bambu calls it the bed exclusion area). Parts are kept 8 mm clear of it, and any part whose convex hull would still reach into it is dropped - the slicer refuses the whole plate over a single one.

## How the settings were decided

For each device, in order:

1. **Machine settings** always come from the P1S system preset. Nothing from the designer's printer (A1 mini, H2S, X1, X1 Carbon) is carried over - no start/end gcode, no bed shape, no kinematics.
2. **Filament** is your own preset: `PETG P1S Tuned` for PETG, `Bambu PLA Basic @BBL X1C` for PLA.
3. **Speeds, accelerations and elephant-foot compensation** follow the P1S preset, *unless* the designer had deliberately changed that value on their own printer - then their number wins.
4. **Everything else** - walls, infill, shells, supports, brim, seams, line widths, variable layer heights - is the designer's own value from their 3mf.
5. **Loose STLs** have no designer profile: they get the P1S 0.20 mm Standard profile plus only the settings the designer states on the model page.
6. Anything changed on purpose beyond that is listed per file in `Validation/per file/`.
7. **Supplied plates**, arranged by hand in Bambu Studio (Pinky Saver 3 & Phone Stand), are delivered exactly as saved, settings included.

## How they were checked

Bambu Studio's command-line slicer crashes on macOS (a known upstream bug), so slicing checks were run with OrcaSlicer 2.4.2, which reads the same project format. Per file:

- the plate slices with no errors, and the time and filament are recorded;
- the plate finishes inside 14 hours;
- filament per copy is compared against a slice of the designer's untouched file, and against the weight quoted on the model page;
- every part is inside the plate, clear of the P1S's excluded front-left corner, with at least 5 mm between parts (checked on the real outlines, not bounding boxes); a supplied plate keeps its own spacing;
- meshes are byte-identical to the designer's, so painted seams survive;
- each object carries its settings, and every object is on a plate; a supplied plate is instead checked byte for byte against the file it came from.

Structural checks: 50 files, 0 problems. All clean.

## Also needed (not printed)

- **Younger Grip Lid Wrench (glue-in magnets)**: optional: 2 x 8x2 mm (or 8x3 mm) round magnets per grip, glued in after printing
- **Plug Puller (WATAP)**: 2 small zip ties (about 15 cm / 6 in) per puller
- **Pen Ball (kit)**: 5 x #6-32 x 3/4 in round-head screws + 5 x #6-32 hex nuts per ball

## Changed on purpose

- **Jar Opener / Vacuum Releaser**: four mesh vertices forming a 0.36 mm spike under the flat base were moved up onto the base; the part stood on the spike, its first layer was empty and the slicer refused it (the designer's own file fails the same way in OrcaSlicer).

## Worth knowing (nothing was changed)

- **KeyWings**: Body_05*: tall and narrow (21 mm on a 6 mm footprint) with brim off in the designer's profile
- **DRAG Assistive Writer (kit of 3)**: DRAG left plate: 98 mm2 of steep overhang with air under it (max drop 6.1 mm at z=9 mm) while supports are off in the designer's profile - worth a look at the preview
- **DRAG Assistive Writer (kit of 3)**: DRAG right plate: 93 mm2 of steep overhang with air under it (max drop 12.9 mm at z=13 mm) while supports are off in the designer's profile - worth a look at the preview
- **Pill Popper**: Body_08*2: 247 mm2 of steep overhang with air under it (max drop 3.6 mm at z=4 mm) while supports are off in the designer's profile - worth a look at the preview
- **Clothes Button & Zipper Hook (handle kit, PLA)**: Handle+scales.stl: 1157 mm2 of steep overhang with air under it (max drop 5.0 mm at z=5 mm) while supports are off in the designer's profile - worth a look at the preview
- **Flipper Nail Clipper (large clippers)**: Flipper Clipper mod for large size nailcutter.stl: 522 mm2 of steep overhang with air under it (max drop 6.0 mm at z=8 mm) while supports are off in the designer's profile - worth a look at the preview
- **Flipper the Clipper v2 (Thingiverse)**: Flipper the Clipper v2 (Thingiverse): 452 mm2 of steep overhang with air under it (max drop 6.0 mm at z=8 mm) while supports are off in the designer's profile - worth a look at the preview
- **Eating Utensil Aid (kit)**: Spoon Holder.stl: 610 mm2 of steep overhang with air under it (max drop 21.0 mm at z=23 mm) while supports are off in the designer's profile - worth a look at the preview
- **Smartphone Magnification Stand**: Smartphone Magnification Stand.stl: 72 mm2 of steep overhang with air under it (max drop 5.0 mm at z=13 mm) while supports are off in the designer's profile - worth a look at the preview
- **Eye Drop Assist eyepiece 03 A**: Eye Drop Assist eyepiece 03 A: 130 mm2 of steep overhang with air under it (max drop 25.2 mm at z=25 mm) while supports are off in the designer's profile - worth a look at the preview
- **Eye Drop Assist eyepiece 03 C**: Eye Drop Assist eyepiece 03 C: 158 mm2 of steep overhang with air under it (max drop 25.2 mm at z=25 mm) while supports are off in the designer's profile - worth a look at the preview
- **Eye Drop Assist eyepiece 04 D**: Eye Drop Assist eyepiece 04 D: 168 mm2 of steep overhang with air under it (max drop 25.2 mm at z=25 mm) while supports are off in the designer's profile - worth a look at the preview
- **Toothpaste Squeezer, external gear (kit)**: Squeezer base (Seigaiha pattern): 186 mm2 of steep overhang with air under it (max drop 57.0 mm at z=60 mm) while supports are off in the designer's profile - worth a look at the preview
- **Toothpaste Squeezer, external gear (kit)**: Key shaft 0.7 mm (standard): 100 mm2 of steep overhang with air under it (max drop 3.9 mm at z=6 mm) while supports are off in the designer's profile - worth a look at the preview
- **Chopstick Helper (small)**: chopstick_helper_smooth.stl: 115 mm2 of steep overhang with air under it (max drop 6.1 mm at z=8 mm) while supports are off in the designer's profile - worth a look at the preview
- **Soup Can Opener (no magnets)**: Soup Can Opener v5.stl: 235 mm2 of steep overhang with air under it (max drop 3.7 mm at z=5 mm) while supports are off in the designer's profile - worth a look at the preview
- **Jar Opener / Vacuum Releaser**: Body_03: 359 mm2 of steep overhang with air under it (max drop 14.3 mm at z=20 mm) while supports are off in the designer's profile - worth a look at the preview
- **Younger Grip Lid Wrench (glue-in magnets)**: YOUNGER__GRIP_Glue In Magnets_.stl: 346 mm2 of steep overhang with air under it (max drop 15.4 mm at z=15 mm) while supports are off in the designer's profile - worth a look at the preview
- **Plug Puller (WATAP)**: Plug Puller WATAP.stl: 156 mm2 of steep overhang with air under it (max drop 0.8 mm at z=1 mm) while supports are off in the designer's profile - worth a look at the preview
- **Hand Press / Grip Strengthener (Light)**: Fingergrip Press Light.stl: 67 mm2 of steep overhang with air under it (max drop 4.0 mm at z=10 mm) while supports are off in the designer's profile - worth a look at the preview
- **Hand Press / Grip Strengthener (Medium)**: Fingergrip Press Medium.stl: 67 mm2 of steep overhang with air under it (max drop 4.0 mm at z=10 mm) while supports are off in the designer's profile - worth a look at the preview
- **Hand Press / Grip Strengthener (Hard)**: Fingergrip Press Hard.stl: 67 mm2 of steep overhang with air under it (max drop 4.0 mm at z=10 mm) while supports are off in the designer's profile - worth a look at the preview
- **Universal Travel Coffee Gimbal (kit)**: Gimbal: 327 mm2 of steep overhang with air under it (max drop 2.0 mm at z=14 mm) while supports are off in the designer's profile - worth a look at the preview
- **Universal Travel Coffee Gimbal (kit)**: Bolt: 86 mm2 of steep overhang with air under it (max drop 3.7 mm at z=4 mm) while supports are off in the designer's profile - worth a look at the preview
- **Shoe Lifter / Boot Jack**: SchuhauszieherV2.stl_A_A: 11300 mm2 of steep overhang with air under it (max drop 92.0 mm at z=92 mm) while supports are off in the designer's profile - worth a look at the preview

## Where each file came from

| # | device | designer source file (kept locally, not in this repo) | model page |
|---|---|---|---|
| 01 | Bag Carrier (Medium) | `Bag Carrier (PLA)/Bag+Carrier+Medium.3mf` | [page](https://makerworld.com/en/models/1715311-bag-carrier#profileId-1820526) |
| 02 | Bag Carrier (Small) | `Bag Carrier (PLA)/Bag+Carrier+Medium.3mf` | [page](https://makerworld.com/en/models/1715311-bag-carrier) |
| 03 | Bag Carrier (Large) | `Bag Carrier (PLA)/Bag+Carrier+Medium.3mf` | [page](https://makerworld.com/en/models/1715311-bag-carrier) |
| 04 | Bottle Cap Opener | `Bottle Opener (PETG)/Bottle+Cap+Opener.3mf` | [page](https://makerworld.com/en/models/1093642-bottle-cap-opener#profileId-1087614) |
| 05 | Bottle Opener (three sizes, wide handle) | `Bottle Opener (PETG)/Bottle+Opener+remix+without+support+material.3mf` | [page](https://makerworld.com/en/models/712423-bottle-opener-three-sizes-wider-handle#profileId-642822) |
| 06 | Assistive Can Tab Opener | `Can Opener (PLA)/Base_Can_Opener.3mf` | [page](https://makerworld.com/en/models/1797256-assistive-can-tab-opener#profileId-1916191) |
| 07 | OPENSESAME3000 Jar Tool | `Jar Opener (PETG)/opensesame.3mf` | [page](https://makerworld.com/en/models/90424-opensesame3000-jar-tool#profileId-96804) |
| 08 | KeyWings | `Key Holder (PETG)/KeyWings+v6+Bambu.3mf` | [page](https://makerworld.com/en/models/1688156-keywings-for-mobility-needs#profileId-1789186) |
| 09 | DRAG Assistive Writer (kit of 3) | `DRAG Assistive Writer (PLA)/DRAG+v2 (1).3mf` | [page](https://makerworld.com/en/models/869468-drag-assistive-writing-and-drawing-device#profileId-821115) |
| 10 | Blister Pack Opener | `Pill Popper (PETG)/Pill+Opener.3mf` | [page](https://makerworld.com/en/models/1791626-blister-pack-opener#profileId-1909450) |
| 11 | Pill Popper | `Pill Popper (PETG)/Pill+Popper+Bambu+Studio.3mf` | [page](https://makerworld.com/en/models/1440419-pill-popper#profileId-1499190) |
| 12 | Clothes Button & Zipper Hook (hook, PETG) | `Clothes Button and Zipper Aid (PETG + PLA)/central-loop-and-hook-button-and-zipper-hook.3mf` | [page](https://makerworld.com/en/models/423231-clothes-button-and-zipper-hook-helper) |
| 13 | Clothes Button & Zipper Hook (handle kit, PLA) | `Clothes Button and Zipper Aid (PETG + PLA)/central-loop-and-hook-button-and-zipper-hook.3mf` | [page](https://makerworld.com/en/models/423231-clothes-button-and-zipper-hook-helper) |
| 14 | Flipper Nail Clipper (large clippers) | `Nail Clipper Holder (PLA)/Flipper+Clipper+mod+for+large+size+nailcutter_a1mini.3mf` | [page](https://makerworld.com/en/models/47915-flipper-the-one-handed-nail-clipper-adjusted-for-l) |
| 15 | Flipper the Clipper v2 (Thingiverse) | `Nail Clipper Holder (PLA)/Nailcutter_v2.stl` | [page](https://www.thingiverse.com/thing:5637570) |
| 16 | Eating Utensil Aid (kit) | `Eating Utensil Aid (PLA)/Eating+Utensil+Aid.3mf` | [page](https://makerworld.com/en/models/192317-eating-utensil-aid-no-supports-updated-v2-files-in#profileId-212499) |
| 17 | Quick-Slip Shoe Horn | `Shoe Horn (PETG)/Shoe+Horn+3MF.3mf` | [page](https://makerworld.com/en/models/1024414-quick-slip-shoe-horn#profileId-1006338) |
| 18 | Tuber Opener | `Tube Opener/Tube_Opener.3mf` | [page](https://makerworld.com/en/models/1737344-tuber-opener#profileId-1845987) |
| 19 | Arthritis Toothbrush Grip | `Toothbrush Grip (PLA)/6066726cbda58_arthritis-toothbrush-grip/toofbrushgrip.stl` | [page](https://www.myminifactory.com/object/3d-print-arthritis-toothbrush-grip-77601) |
| 20 | One-Handed Page Holder | `Other/One_Handed_Book_Holder.3mf` | [page](https://makerworld.com/en/models/1740474-one-handed-page-holder#profileId-1849552) |
| 21 | Smartphone Magnification Stand | `Other/Smartphone+Magnification+Stand.3mf` | [page](https://makerworld.com/en/models/1737380-smartphone-magnification-stand#profileId-1846025) |
| 22 | Eye Drop Assist pliers (bottle 20 mm) | `Eye Drop Assist (PLA)/edab_pliers_07_bd20.stl` | [page](https://www.printables.com/model/1031668-eye-drop-assist-for-bottles) |
| 23 | Eye Drop Assist pliers (bottle 22 mm) | `Eye Drop Assist (PLA)/edab_pliers_07_bd22.stl` | [page](https://www.printables.com/model/1031668-eye-drop-assist-for-bottles) |
| 24 | Eye Drop Assist pliers (bottle 24 mm) | `Eye Drop Assist (PLA)/edab_pliers_07_bd24.stl` | [page](https://www.printables.com/model/1031668-eye-drop-assist-for-bottles) |
| 25 | Eye Drop Assist pliers (bottle 25 mm) | `Eye Drop Assist (PLA)/EDA_Pliers_Bottle_06Bc_BD25.stl` | [page](https://www.printables.com/model/1031668-eye-drop-assist-for-bottles) |
| 26 | Eye Drop Assist eyepiece 03 A | `Eye Drop Assist (PLA)/EDA_EyePiece_03_A.stl` | [page](https://www.printables.com/model/1031668-eye-drop-assist-for-bottles) |
| 27 | Eye Drop Assist eyepiece 03 B | `Eye Drop Assist (PLA)/EDA_EyePiece_03_B.stl` | [page](https://www.printables.com/model/1031668-eye-drop-assist-for-bottles) |
| 28 | Eye Drop Assist eyepiece 03 C | `Eye Drop Assist (PLA)/EDA_EyePiece_03_C.stl` | [page](https://www.printables.com/model/1031668-eye-drop-assist-for-bottles) |
| 29 | Eye Drop Assist eyepiece 04 D | `Eye Drop Assist (PLA)/eda_eyepiece_04_d.stl` | [page](https://www.printables.com/model/1031668-eye-drop-assist-for-bottles) |
| 30 | Eye Drop Assist eyepiece 04 E | `Eye Drop Assist (PLA)/eda_eyepiece_04_e.stl` | [page](https://www.printables.com/model/1031668-eye-drop-assist-for-bottles) |
| 31 | Bedside Hook-On Storage Box (kit) | `New Devices/Bedside+Holder+v3.3mf` | [page](https://makerworld.com/en/models/1051323-bedside-hook-on-storage-box-organizer#profileId-1038131) |
| 32 | Toothpaste Squeezer, external gear (kit) | `New Devices/ToothSqeez_ExterGear_SeigaihaPattern.3mf` | [page](https://makerworld.com/en/models/2423006-toothpaste-squeezer-external-gear#profileId-2657457) |
| 33 | Chopstick Helper (small) | `New Devices/chopstick_helper_new_design_PLA_Small.3mf` | [page](https://makerworld.com/en/models/1088273-chopstick-helper-refreshed-design#profileId-1082781) |
| 34 | Soup Can Opener (no magnets) | `New Devices/Soup+Can+Opener+-+no+pause+for+magnets.3mf` | [page](https://makerworld.com/en/models/1030162-soup-can-opener-for-poor-grip-strength#profileId-1012846) |
| 35 | Jar Opener / Vacuum Releaser | `New Devices/Jar+Opener+Bambu+ULTRA+FAST.3mf` | [page](https://makerworld.com/en/models/1642031-jar-opener-tuned-for-all-bambu-printers#profileId-1735123) |
| 36 | Younger Grip Lid Wrench (glue-in magnets) | `New Devices/PRJ___YOUNGER+GRIP_Glue-in+Magnets_.3mf` | [page](https://makerworld.com/en/models/1493731-younger-grip-lid-wrench-arthritis-aid#profileId-1572541) |
| 37 | Plug Puller (WATAP) | `New Devices/Plug+Puller+by+WATAP.3mf` | [page](https://makerworld.com/en/models/421822-plug-puller-assistive-technology-by-watap#profileId-324742) |
| 38 | Pinky Saver 3 & Phone Stand | `New Devices/PinkySaver3_x19.3mf` | [page](https://makerworld.com/en/models/1842862-pinky-saver-3#profileId-1969044) |
| 39 | Universal Cup Holder (kit) | `New Devices/STOLLER_CUP_HOLDER_v2.0.3mf` | [page](https://makerworld.com/en/models/1969980-universal-cup-holder#profileId-2118034) |
| 40 | Adjustable Cane Holder (kit) | `New Devices/adjustable-cane-holder-model_files/Recommended Print Files/texture_on_cane_holder_v3.stl (+2 more)` | [page](https://www.printables.com/model/203631-adjustable-cane-holder) |
| 41 | Hand Press / Grip Strengthener (Light) | `New Devices/Fingergrip+Press (1).3mf` | [page](https://makerworld.com/en/models/531052-hand-press-grip-strengthening#profileId-447870) |
| 42 | Hand Press / Grip Strengthener (Medium) | `New Devices/Fingergrip+Press (1).3mf` | [page](https://makerworld.com/en/models/531052-hand-press-grip-strengthening#profileId-447870) |
| 43 | Hand Press / Grip Strengthener (Hard) | `New Devices/Fingergrip+Press (1).3mf` | [page](https://makerworld.com/en/models/531052-hand-press-grip-strengthening#profileId-447870) |
| 44 | Universal Travel Coffee Gimbal (kit) | `New Devices/universal-travel-coffee-gimbal-model_files/Gimbal.stl (+3 more)` | [page](https://www.printables.com/model/129329-universal-travel-coffee-gimbal) |
| 45 | Pen Ball (kit) | `New Devices/Pen Ball - 2810069/files/Pen_Ball_Top_v.1.0.0.STL (+1 more)` | [page](https://www.thingiverse.com/thing:2810069) |
| 46 | Playing Card Holder (4 rows) | `New Devices/Full Size Playing Card Holder - 2863434/files/holder-4row.stl` | [page](https://www.thingiverse.com/thing:2863434) |
| 47 | Shoe Lifter / Boot Jack | `New Devices/SchuhauszieherV2 (1).3mf` | [page](https://makerworld.com/en/models/1040127-shoe-lifter-boot-jack#profileId-1024783) |
| 48 | Adaptive Pencil Grip | `New Devices/adaptive-pencil-grip-model_files/Adaptive writer.stl` | [page](https://www.printables.com/model/520212-adaptive-pencil-grip) |

Each MakerWorld link's profile id was matched against the `DesignProfileId` stored inside the local 3mf, so these are the exact profiles that were linked. The links for 19-21 (Arthritis Toothbrush Grip, One-Handed Page Holder, Smartphone Magnification Stand) were added afterwards from the model pages themselves.

## Look-alikes that were left out

- `Other/EyeDropperAid.3mf` - MakeAble 'Eye Dropper Squeezer Aid' - a different model from the Printables Eye Drop Assist on the list
- `Other/jar-opener+(1).3mf` - MakeAble 'Jar/Pop Bottle and Can Assist' - not the OPENSESAME3000 jar tool
- `Other/4+in+1+button+aid,+key+turner,+zipper+aid,+handle.3mf` - MakeAble 4-in-1 aid - not the Clothes Button & Zipper Hook helper
- `Other/Bottle_Opener_30.stl + .gcode` - a third bottle opener, sliced for a Prusa MK3S
- `Toothbrush Grip (PLA)/toothbrush.STL` - the flat MyMiniFactory toothbrush, not the round arthritis grip you picked
- `Walking Stick Holder/` - not on the catalogue list
- `Other/DRAG+v2.3mf` - byte-identical copy of the DRAG folder's 3mf
- `Other/Tube_Opener.3mf` - plain mesh export with no settings in it
- `Aug*.3mf, Combined*.3mf, Bag_Carrier_x4.3mf` - earlier working files, not designer sources
- `Clothes Button .../*.stl (loose)` - the loose STLs differ from the 3mf: its pins are scaled to 95% and its hook carries painted seams

From the second batch (`New Devices/`):

- `adjustable-cane-holder-model_files/Design History Files/, Alternative Files/` - the designer's earlier versions and work-in-progress latch; their 'Recommended Print Files' are used
- `universal-travel-coffee-gimbal-model_files/Optional *.stl` - optional extras (long bolt, nut, cup and flat-surface adapters, vertical gimbal, TPU bar wrap); the kit is gimbal + clamp + bolt + washer
- `universal-travel-coffee-gimbal-model_files/MPC Washer.3mf, *.step, *.f3d` - a plain mesh of the washer STL that is used, and the CAD sources
- `Full Size Playing Card Holder - 2863434/files/holder.stl, case-*.stl` - the original 3-row holder and the storage cases; the 4-row holder is the one on the list
- `Full Size Playing Card Holder - 2863434/files/holder-4rows.stl` - same shape as holder-4row.stl
- `adaptive-pencil-grip-model_files/Test print.stl` - a small pencil-fit test piece
- `PRJ___YOUNGER+GRIP_Glue-in+Magnets_.3mf, plate 1` - the painted four-colour version; the single-colour plate is used
- `ToothSqeez_ExterGear_SeigaihaPattern.3mf, plates 4-6` - the 1.0, 1.3 and 1.6 mm key shafts for thicker tube ends; the kit uses the 0.7 mm standard shaft
- `Fingergrip+Press (1).3mf` - one file, three devices: each strength gets its own plate

## Still open

- **Eye Drop Assist (files 22-30)**: the three Printables pages sit behind a bot check, so the designer's own print settings could not be read. Those files use the P1S 0.20 mm Standard profile in PLA. They also need a decision: whether a pliers and an eyepiece pair up into one device (in which case they should be kit plates) or are alternatives.
- **Universal Cup Holder**: the designer's painted brim ears are carried over, but OrcaSlicer (used for these checks) does not read painted ears. Worth a glance at the first layer in Bambu Studio's preview before the first print.

