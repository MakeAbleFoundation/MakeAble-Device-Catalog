# 38 Pinky Saver 3 & Phone Stand

- file: `Full Plates/38 Pinky Saver 3 & Phone Stand - PLA x18.3mf`
- source: https://makerworld.com/en/models/1842862-pinky-saver-3#profileId-1969044
- reference 3mf: `New Devices/PinkySaver3_x19.3mf` (the delivered file, byte for byte)
- designer: aqua3D
- license: Standard Digital File License
- material: PLA (Bambu PLA Basic @BBL X1C)
- on the plate: 18 copies (9 interlocked pairs)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL X1C | 0.2 mm | 0.2 mm | 2 | 15% grid | off | auto_brim | 5/3 |

The designer's profile ("0.2mm layer, 2 walls, 15% infill") on the P1S system presets
(`Bambu Lab P1S 0.4 nozzle`, `0.20mm Standard @BBL X1C`, `Bambu PLA Basic @BBL X1C`).

## How this file was made

Supplied as a finished plate, arranged and saved in Bambu Studio 2.2.2, and committed
unchanged. It was not rebuilt by `Validation/tools`, so the settings are not baked per object
and the packer's spacing rules were not applied.

## Validation
- Orca slice: passed - 5h 8m 33s, 159.0 g, 126.2 cm3, no warnings, no toolpath conflicts
- per copy: 7.01 cm3, 8.8 g
- the model page quotes 9 g per copy
- geometry check: tighter than the house rules, which it does not follow - the closest pairs
  are about 3.3 mm apart (rule: 5 mm), and the front row sits 3 mm from the plate edge
  (rule: 5 mm) and 3 mm right of the 18 x 28 mm excluded corner (rule: 8 mm). Every part is
  on the plate and its convex hull is clear of the corner.
- clamped for Orca only (the delivered file keeps Bambu's values): tree_support_wall_count,
  raft_first_layer_expansion

## Notes
- Replaces the earlier Pinky Saver & Phone Stand (standard holes, model 941286) with the
  designer's newer Pinky Saver 3.
- The source file was named `x19`, but it holds 18 copies (Orca and Bambu's own plate
  thumbnail agree).
- Catalogue 2 plate 38 still holds the earlier Pinky Saver.
