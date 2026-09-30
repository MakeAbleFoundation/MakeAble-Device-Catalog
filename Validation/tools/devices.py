#!/usr/bin/env python3
"""The MakeAble catalogue: which file is the source of truth for each device.

Every MakerWorld `profileId` in the brief was matched against the `DesignProfileId`
stored inside the local 3mf, so `ref` below is the exact profile that was linked.
"""
import os

M = "/Users/justinrui/Desktop/M/"
# the second batch lives next to the repo, in a folder that is kept out of git
REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
N = os.path.join(REPO, "New Devices") + "/"

MAX_HOURS = 14.0        # no plate may run longer than this (Orca's estimate)

PLA = "Bambu PLA Basic @BBL X1C"
PETG = "PETG P1S Tuned"

DEVICES = [
 dict(id=1, slug="bag-carrier-medium", title="Bag Carrier (Medium)", designer="MakeAble",
      link="https://makerworld.com/en/models/1715311-bag-carrier#profileId-1820526",
      ref=M+"Bag Carrier (PLA)/Bag+Carrier+Medium.3mf", names=["Bag Carrier Medium.stl"],
      material="PLA"),
 dict(id=2, slug="bag-carrier-small", title="Bag Carrier (Small)", designer="MakeAble",
      link="https://makerworld.com/en/models/1715311-bag-carrier",
      ref=M+"Bag Carrier (PLA)/Bag+Carrier+Medium.3mf",
      mesh_ref=M+"Other/All+bag+carriers.3mf", names=["Bag Carrier Small.stl"],
      material="PLA",
      notes=["Mesh from All+bag+carriers.3mf; settings from the linked Medium profile "
             "(the designer uses the same 0.2 mm / 2 walls / 15% profile for all sizes)."]),
 dict(id=3, slug="bag-carrier-large", title="Bag Carrier (Large)", designer="MakeAble",
      link="https://makerworld.com/en/models/1715311-bag-carrier",
      ref=M+"Bag Carrier (PLA)/Bag+Carrier+Medium.3mf",
      mesh_ref=M+"Other/All+bag+carriers.3mf", names=["Bag Carrier Large.stl"],
      material="PLA",
      notes=["Mesh from All+bag+carriers.3mf; settings from the linked Medium profile."]),
 dict(id=4, slug="bottle-cap-opener", title="Bottle Cap Opener", designer="TuTu",
      link="https://makerworld.com/en/models/1093642-bottle-cap-opener#profileId-1087614",
      ref=M+"Bottle Opener (PETG)/Bottle+Cap+Opener.3mf", names=["Bottle Cap Opener"],
      material="PETG",
      notes=["Designer's profile: 0.15 mm first layer, 5 walls, 50% infill, slower walls "
             "(was an A1 mini profile, rebased onto the P1S)."]),
 dict(id=5, slug="bottle-opener-wide-handle",
      title="Bottle Opener (three sizes, wide handle)", designer="val",
      link="https://makerworld.com/en/models/712423-bottle-opener-three-sizes-wider-handle#profileId-642822",
      ref=M+"Bottle Opener (PETG)/Bottle+Opener+remix+without+support+material.3mf",
      names=["bottle opener remix.stl"], material="PETG",
      notes=["The designer's per-object settings (5 walls, 15% honeycomb, supports on, "
             "seam at the back) are carried over per object, as in the original."]),
 dict(id=6, slug="can-opener", title="Assistive Can Tab Opener", designer="MakeAble",
      link="https://makerworld.com/en/models/1797256-assistive-can-tab-opener#profileId-1916191",
      ref=M+"Can Opener (PLA)/Base_Can_Opener.3mf", names=["Base_Can_Opener.stl"],
      material="PLA", gap=8.0),
 dict(id=7, slug="jar-opener", title="OPENSESAME3000 Jar Tool", designer="cartyski",
      link="https://makerworld.com/en/models/90424-opensesame3000-jar-tool#profileId-96804",
      ref=M+"Jar Opener (PETG)/opensesame.3mf", names=["logod.stl"], material="PETG",
      notes=["Linked profile is the PLA one (0.12 mm, 3 walls, 15% gyroid). The designer "
             "publishes the same settings as a PETG profile, which is what this file is "
             "set up for since the folder says PETG."]),
 dict(id=8, slug="keywings", title="KeyWings", designer="AlbertMakes",
      link="https://makerworld.com/en/models/1688156-keywings-for-mobility-needs#profileId-1789186",
      ref=M+"Key Holder (PETG)/KeyWings+v6+Bambu.3mf", names=["Body_05*"], material="PETG",
      cap=76,
      notes=["Designer recommends PETG or nylon; brim is deliberately off in their profile."]),
 dict(id=9, slug="drag-writer", title="DRAG Assistive Writer (kit of 3)", designer="PrintLab",
      link="https://makerworld.com/en/models/869468-drag-assistive-writing-and-drawing-device#profileId-821115",
      ref=M+"DRAG Assistive Writer (PLA)/DRAG+v2 (1).3mf", names=["all parts v2.stl"],
      split=["DRAG left plate", "DRAG right plate", "DRAG centre plate"],
      kit=[1, 1, 1], material="PLA",
      notes=["One kit = left + right + centre plate, as the maker guide specifies "
             "(plus 3x M3x20 screws, not printed)."]),
 # a plate arranged by hand in Bambu Studio: delivered byte for byte (build.supplied_device)
 dict(id=10, slug="blister-pack-opener", title="Blister Pack Opener", designer="MakeAble",
      link="https://makerworld.com/en/models/1791626-blister-pack-opener#profileId-1909450",
      ref=N+"BlisterPackOpener_x8.3mf", names=["Blister Pack Opener.step"], indices=[0],
      supplied=True, material="PETG",
      notes=["Tree supports and an outer brim are part of the designer's profile.",
             "Adjusted by hand in Bambu Studio from the earlier built plate "
             "(designer file `Pill Popper (PETG)/Pill+Opener.3mf`): all eight copies turned "
             "over onto their opposite face; mesh, settings and copy count unchanged."]),
 dict(id=11, slug="pill-popper", title="Pill Popper", designer="AlbertMakes",
      link="https://makerworld.com/en/models/1440419-pill-popper#profileId-1499190",
      ref=M+"Pill Popper (PETG)/Pill+Popper+Bambu+Studio.3mf", names=["Body_08*2"],
      material="PETG",
      notes=["Model page asks for a very slow first layer: the profile's 20 mm/s is kept.",
             "Page says 10-15% infill, the profile says 25%; the profile wins, as agreed."]),
 dict(id=12, slug="clothes-button-hook",
      title="Clothes Button & Zipper Hook (hook, PETG)", designer="Adapt3D_OT",
      link="https://makerworld.com/en/models/423231-clothes-button-and-zipper-hook-helper",
      ref=M+"Clothes Button and Zipper Aid (PETG + PLA)/central-loop-and-hook-button-and-zipper-hook.3mf",
      names=["central-loop-and-hook-button-and-zipper-hook.stl"], material="PETG",
      notes=["Designer: print the central piece in PETG so it keeps its shape.",
             "This mesh carries the designer's painted seams, which are preserved."]),
 dict(id=13, slug="clothes-button-handles",
      title="Clothes Button & Zipper Hook (handle kit, PLA)", designer="Adapt3D_OT",
      link="https://makerworld.com/en/models/423231-clothes-button-and-zipper-hook-helper",
      ref=M+"Clothes Button and Zipper Aid (PETG + PLA)/central-loop-and-hook-button-and-zipper-hook.3mf",
      names=["Handle+scales.stl", "Connector+pin.stl"], kit=[2, 2], material="PLA",
      notes=["One kit = 2 handle scales + 2 connector pins, which is what one hook needs.",
             "Pins are the designer's 95%-scaled version from the 3mf, not the loose STL."]),
 dict(id=14, slug="flipper-nail-clipper-large",
      title="Flipper Nail Clipper (large clippers)", designer="saad.caffeine",
      link="https://makerworld.com/en/models/47915-flipper-the-one-handed-nail-clipper-adjusted-for-l",
      ref=M+"Nail Clipper Holder (PLA)/Flipper+Clipper+mod+for+large+size+nailcutter_a1mini.3mf",
      names=["Flipper Clipper mod for large size nailcutter.stl"], material="PLA",
      notes=["Print-in-place hinge: the two bodies stay in one object, as the designer had it.",
             "Designer notes PETG works better than PLA; folder says PLA, so PLA it is."]),
 dict(id=15, slug="flipper-clipper-v2", title="Flipper the Clipper v2 (Thingiverse)",
      designer="kafei", link="https://www.thingiverse.com/thing:5637570",
      stl=[M+"Nail Clipper Holder (PLA)/Nailcutter_v2.stl"], material="PLA",
      overrides={"sparse_infill_density": "80%", "skin_infill_density": "80%",
                 "skeleton_infill_density": "80%"},
      notes=["No designer 3mf exists, so this is the P1S 0.20 mm Standard profile plus "
             "the designer's one stated requirement: 80% infill."]),
 dict(id=16, slug="eating-utensil-aid", title="Eating Utensil Aid (kit)",
      designer="Keebitzenny",
      link="https://makerworld.com/en/models/192317-eating-utensil-aid-no-supports-updated-v2-files-in#profileId-212499",
      ref=M+"Eating Utensil Aid (PLA)/Eating+Utensil+Aid.3mf",
      names=["Spoon Holder.stl", "Nut for Spoon Holder.stl"], kit=[1, 1], material="PLA",
      notes=["Designer recommends ABS and supplies a PLA profile; PLA used per the folder.",
             "PETG would be the tougher option for a utensil aid that gets washed."]),
 dict(id=17, slug="shoe-horn", title="Quick-Slip Shoe Horn", designer="Stag 3D",
      link="https://makerworld.com/en/models/1024414-quick-slip-shoe-horn#profileId-1006338",
      ref=M+"Shoe Horn (PETG)/Shoe+Horn+3MF.3mf", names=["Shoe Horn.stl"], material="PETG",
      notes=["Designer: PETG or stronger is required.",
             "Profile came from an H2S; speeds and accelerations rebased to the P1S."]),
 dict(id=18, slug="tube-opener", title="Tuber Opener", designer="MakeAble",
      link="https://makerworld.com/en/models/1737344-tuber-opener#profileId-1845987",
      ref=M+"Tube Opener/Tube_Opener.3mf", indices=[0], material="PLA"),
 dict(id=19, slug="toothbrush-grip", title="Arthritis Toothbrush Grip",
      designer="MyMiniFactory",
      link="https://www.myminifactory.com/object/3d-print-arthritis-toothbrush-grip-77601",
      stl=[M+"Toothbrush Grip (PLA)/6066726cbda58_arthritis-toothbrush-grip/toofbrushgrip.stl"],
      material="PLA", cap=19,
      notes=["No designer profile exists; P1S 0.20 mm Standard used.",
             "Heavy part: check the reported filament weight before starting a full plate."]),
 dict(id=20, slug="book-holder", title="One-Handed Page Holder", designer="MakeAble",
      link="https://makerworld.com/en/models/1740474-one-handed-page-holder#profileId-1849552",
      ref=M+"Other/One_Handed_Book_Holder.3mf", names=["One_Handed_Book_Holder.stl"],
      material="PLA"),
 dict(id=21, slug="phone-magnifier-stand", title="Smartphone Magnification Stand",
      designer="MakeAble",
      link="https://makerworld.com/en/models/1737380-smartphone-magnification-stand#profileId-1846025",
      ref=M+"Other/Smartphone+Magnification+Stand.3mf",
      names=["Smartphone Magnification Stand.stl"], material="PLA"),
]

EYE_DROP = [
 ("eda-pliers-bd20", "Eye Drop Assist pliers (bottle 20 mm)", "edab_pliers_07_bd20.stl"),
 ("eda-pliers-bd22", "Eye Drop Assist pliers (bottle 22 mm)", "edab_pliers_07_bd22.stl"),
 ("eda-pliers-bd24", "Eye Drop Assist pliers (bottle 24 mm)", "edab_pliers_07_bd24.stl"),
 ("eda-pliers-bd25", "Eye Drop Assist pliers (bottle 25 mm)", "EDA_Pliers_Bottle_06Bc_BD25.stl"),
 ("eda-eyepiece-03a", "Eye Drop Assist eyepiece 03 A", "EDA_EyePiece_03_A.stl"),
 ("eda-eyepiece-03b", "Eye Drop Assist eyepiece 03 B", "EDA_EyePiece_03_B.stl"),
 ("eda-eyepiece-03c", "Eye Drop Assist eyepiece 03 C", "EDA_EyePiece_03_C.stl"),
 ("eda-eyepiece-04d", "Eye Drop Assist eyepiece 04 D", "eda_eyepiece_04_d.stl"),
 ("eda-eyepiece-04e", "Eye Drop Assist eyepiece 04 E", "eda_eyepiece_04_e.stl"),
]
for i, (slug, title, fn) in enumerate(EYE_DROP, start=22):
    DEVICES.append(dict(
        id=i, slug=slug, title=title, designer="jhw (Printables)",
        link="https://www.printables.com/model/1031668-eye-drop-assist-for-bottles",
        stl=[M+"Eye Drop Assist (PLA)/"+fn], material="PLA",
        notes=["No designer 3mf; P1S 0.20 mm Standard used. The Printables pages are "
               "behind a bot check, so the designer's own settings are unverified."]))

MW_STD = "MakerWorld Standard Digital File License"
CANE = N + "adjustable-cane-holder-model_files/Recommended Print Files/"
GIMBAL = N + "universal-travel-coffee-gimbal-model_files/"
PEN = N + "Pen Ball - 2810069/files/"

DEVICES += [
 dict(id=31, slug="bedside-box", title="Bedside Hook-On Storage Box (kit)", designer="StefB",
      link="https://makerworld.com/en/models/1051323-bedside-hook-on-storage-box-organizer#profileId-1038131",
      ref=N+"Bedside+Holder+v3.3mf", names=["Bedside Holder v3.stl", "Bedside Holder v3 hook.stl"],
      kit=[1, 2], keep_layout=True, material="PLA", license=MW_STD,
      notes=["One kit = the storage box + two hooks, as on the designer's plate.",
             "The box is 240 mm long and lies diagonally across the bed. The packer cannot fit "
             "it inside the usual 5 mm margin, so the designer's own arrangement is used, "
             "centred (their X1 has the same bed and excluded corner as the P1S).",
             "The designer's variable layer height on the box is kept."]),
 dict(id=32, slug="toothpaste-squeezer-gear", title="Toothpaste Squeezer, external gear (kit)",
      designer="Tazio design",
      link="https://makerworld.com/en/models/2423006-toothpaste-squeezer-external-gear#profileId-2657457",
      ref=N+"ToothSqeez_ExterGear_SeigaihaPattern.3mf", objects=[12, 2, 4],
      rename=["Squeezer base (Seigaiha pattern)", "Key head", "Key shaft 0.7 mm (standard)"],
      kit=[1, 1, 1], cap=8, material="PLA", license=MW_STD,
      notes=["One kit = base + key head + the 0.7 mm 'Standard' key shaft. The designer also "
             "offers 1.0, 1.3 and 1.6 mm shafts for thicker tube ends (left out).",
             "The key parts keep the designer's own 15% gyroid; the base uses their 3 walls, "
             "25% grid.",
             "Designer: PLA, PLA+, PETG or ASA - not silk PLA, which cracks at the key."]),
 dict(id=33, slug="chopstick-helper", title="Chopstick Helper (small)", designer="Daranto",
      link="https://makerworld.com/en/models/1088273-chopstick-helper-refreshed-design#profileId-1082781",
      ref=N+"chopstick_helper_new_design_PLA_Small.3mf", names=["chopstick_helper_smooth.stl"],
      material="PLA", license=MW_STD,
      notes=["Small size: 6.12 mm holes. Medium (6.80 mm) and large (7.75 mm) exist on the page.",
             "Designer's profile: 6 walls, 100% infill."]),
 dict(id=34, slug="soup-can-opener", title="Soup Can Opener (no magnets)", designer="Makerneer",
      link="https://makerworld.com/en/models/1030162-soup-can-opener-for-poor-grip-strength#profileId-1012846",
      ref=N+"Soup+Can+Opener+-+no+pause+for+magnets.3mf", names=["Soup Can Opener v5.stl"],
      material="PETG", license="CC0",
      notes=["The designer printed it in Bambu PETG HF, so PETG it is.",
             "The 'no magnets' profile: no pause, the magnet holes stay empty."]),
 dict(id=35, slug="jar-opener-vacuum", title="Jar Opener / Vacuum Releaser",
      designer="AlbertMakes",
      link="https://makerworld.com/en/models/1642031-jar-opener-tuned-for-all-bambu-printers#profileId-1735123",
      ref=N+"Jar+Opener+Bambu+ULTRA+FAST.3mf", names=["Body_03"], material="PLA",
      license=MW_STD, flatten_bottom=True,
      notes=["Mesh fix: four vertices formed a 0.1 x 0.5 mm spike 0.36 mm below the flat "
             "base, so the part stood on the spike and its first layer was empty - the "
             "slicer refuses it (the designer's own file fails the same way in OrcaSlicer). "
             "Those four vertices were moved up onto the base; nothing else in the mesh "
             "changed.",
             "Profile was an A1 mini 0.24 mm Draft profile; rebased onto the P1S 0.24 mm Draft.",
             "The page text suggests 0.2 mm, 6 walls, 60% infill; the downloaded profile uses "
             "0.24 mm, 2 walls, 10% gyroid. The profile wins, as agreed."]),
 # a plate arranged by hand in Bambu Studio: delivered byte for byte (build.supplied_device)
 dict(id=36, slug="younger-grip", title="Younger Grip Lid Wrench (no magnets)",
      designer="SFYoung",
      link="https://makerworld.com/en/models/1493731-younger-grip-lid-wrench-arthritis-aid#profileId-1572614",
      ref=N+"PRJ___YOUNGER_GRIP_NO_Magnets_.3mf", names=["YOUNGER__GRIP_NO Magnets_.stl"],
      indices=[0], supplied=True, material="PLA", license=MW_STD,
      notes=["Replaces the earlier glue-in-magnets plate with the designer's 'NO MAGNETS' "
             "profile: the magnet cavities are filled in, so there is nothing to glue.",
             "The designer's single-colour plate, 8 copies; their profile (0.2 mm, 3 walls, "
             "10% gyroid) on the P1S presets.",
             "Their height-range layer settings are kept: 0.12 mm layers over the finger-well "
             "overhang, 0.24 mm for the bridge above it, 0.2 mm elsewhere."]),
 dict(id=37, slug="plug-puller", title="Plug Puller (WATAP)", designer="WATAP_3D",
      link="https://makerworld.com/en/models/421822-plug-puller-assistive-technology-by-watap#profileId-324742",
      ref=N+"Plug+Puller+by+WATAP.3mf", names=["Plug Puller WATAP.stl"], material="PLA",
      license="CC BY-NC-SA",
      hardware="2 small zip ties (about 15 cm / 6 in) per puller",
      notes=["The designer's variable layer height is kept."]),
 # a plate arranged by hand in Bambu Studio: delivered byte for byte (build.supplied_device)
 dict(id=38, slug="pinky-saver", title="Pinky Saver 3 & Phone Stand", designer="aqua3D",
      link="https://makerworld.com/en/models/1842862-pinky-saver-3#profileId-1969044",
      ref=N+"PinkySaver3_x19.3mf", names=["pinky saver 3.stl"], indices=[0],
      supplied=True, material="PLA", license=MW_STD,
      notes=["Replaces the earlier Pinky Saver & Phone Stand (standard holes, model 941286) "
             "with the designer's newer one-piece Pinky Saver 3.",
             "The designer's profile (0.2 mm, 2 walls, 15% infill) on the P1S presets.",
             "The supplied file is named x19 but holds 18 copies; Orca and Bambu's own plate "
             "thumbnail agree."]),
 dict(id=39, slug="cup-holder", title="Universal Cup Holder (kit)", designer="RED_eleven",
      link="https://makerworld.com/en/models/1969980-universal-cup-holder#profileId-2118034",
      ref=N+"STOLLER_CUP_HOLDER_v2.0.3mf",
      names=["UPDATED CUP.stp", "JOY-000280230", "JOY-000280234", "KNOB.stp", "SPACER.stp",
             "SCREW.stp_A", "SCREW.stp_B", "FINGERS.stp"],
      kit=[1, 1, 1, 1, 1, 1, 1, 3], gap=8.0, material="PLA", license=MW_STD,
      notes=["One kit = cup, both clamp halves, knob, spacer, the two halves of the split "
             "screw and three gripping fingers - the designer's 'Cup Holder & Clamp V2' plate.",
             "Designer's profile: 6 walls, tree supports, painted brim ears on the fingers "
             "(kept)."]),
 dict(id=40, slug="cane-holder", title="Adjustable Cane Holder (kit)",
      designer="newhouse24 (Printables)",
      link="https://www.printables.com/model/203631-adjustable-cane-holder",
      stl=[CANE+"texture_on_cane_holder_v3.stl", CANE+"alt_screw_updates.stl",
           CANE+"clamp_protector_tri.stl"],
      stl_names=["Cane holder (textured clamp)", "Clamp screw (easy grip)", "Clamp protector"],
      kit=[1, 1, 1], cap=6, material="PLA", license="CC BY-NC-SA 4.0",
      overrides={"sparse_infill_density": "60%", "skin_infill_density": "60%",
                 "skeleton_infill_density": "60%", "enable_support": "1",
                 "support_on_build_plate_only": "1", "support_base_pattern_spacing": "4"},
      part_overrides={"Clamp screw (easy grip)": {"brim_type": "outer_only",
                                                  "brim_width": "5"}},
      notes=["The page's 'Recommended Print Files': textured holder, easy-grip screw, "
             "textured clamp protector.",
             "Designer's stated settings: 60% infill, supports touching the build plate at "
             "about 10% density (support line spacing 4 mm), a brim for the screw. Everything "
             "else is the P1S 0.20 mm Standard."]),
] + [
 dict(id=41 + i, slug=f"hand-press-{lvl.lower()}",
      title=f"Hand Press / Grip Strengthener ({lvl})", designer="Sakul",
      link="https://makerworld.com/en/models/531052-hand-press-grip-strengthening#profileId-447870",
      ref=N+"Fingergrip+Press (1).3mf", names=[f"Fingergrip Press {lvl}.stl"],
      material="PETG", license=MW_STD,
      notes=[f"The {lvl.lower()} grip: {walls} walls (the designer's per-object setting).",
             "Designer: print it in PETG, PLA tends to deform."])
 for i, (lvl, walls) in enumerate([("Light", 4), ("Medium", 5), ("Hard", 6)])
] + [
 dict(id=44, slug="coffee-gimbal", title="Universal Travel Coffee Gimbal (kit)",
      designer="mobiobi (Printables)",
      link="https://www.printables.com/model/129329-universal-travel-coffee-gimbal",
      stl=[GIMBAL+"Gimbal.stl", GIMBAL+"Clamp.stl", GIMBAL+"Bolt.stl", GIMBAL+"MPC Washer.stl"],
      stl_names=["Gimbal", "Clamp", "Bolt", "Washer"], kit=[1, 1, 1, 1], kit_by_size=True,
      gap=8.0,
      material="PETG",
      license="CC BY-NC 4.0",
      overrides={"wall_loops": "4"},
      part_overrides={"Clamp": {"enable_support": "1", "support_type": "tree(auto)",
                                "support_on_build_plate_only": "1"}},
      notes=["One kit = gimbal + clamp + bolt + washer. The optional long bolt, nut, cup and "
             "flat-surface adapters, vertical gimbal and TPU bar wrap are left out.",
             "Designer: 4 perimeters, no supports on the gimbal. The clamp has a large "
             "overhang in its print orientation, so it alone gets tree supports.",
             "PETG rather than PLA: it holds hot cups and may sit on a car dashboard."]),
 dict(id=45, slug="pen-ball", title="Pen Ball (kit)",
      designer="makersmakingchange (Thingiverse)",
      link="https://www.thingiverse.com/thing:2810069",
      stl=[PEN+"Pen_Ball_Top_v.1.0.0.STL", PEN+"Pen_Ball_Bottom_v.1.0.0.stl"],
      stl_names=["Pen Ball top", "Pen Ball bottom"], kit=[1, 1], cap=4, material="PETG",
      license="CC BY-NC-SA",
      overrides={"sparse_infill_density": "50%", "skin_infill_density": "50%",
                 "skeleton_infill_density": "50%", "enable_support": "1",
                 "support_on_build_plate_only": "1"},
      hardware="5 x #6-32 x 3/4 in round-head screws + 5 x #6-32 hex nuts per ball",
      notes=["Designer's spec sheet: 0.2 mm layers, 50% infill, supports only in the centre "
             "cavity, both halves printed together. Build-plate-only supports reach just "
             "that cavity.",
             "Designer used ABS; PETG is the closest of the two filaments here."]),
 dict(id=46, slug="card-holder-4row", title="Playing Card Holder (4 rows)",
      designer="Djones1t (Thingiverse)", link="https://www.thingiverse.com/thing:2863434",
      stl=[N+"Full Size Playing Card Holder - 2863434/files/holder-4row.stl"], material="PLA",
      license="CC BY",
      notes=["The four-row holder (holder-4row.stl and holder-4rows.stl are the same shape).",
             "Designer: prints fine without supports. P1S 0.20 mm Standard."]),
 dict(id=47, slug="boot-jack", title="Shoe Lifter / Boot Jack", designer="Chio97",
      link="https://makerworld.com/en/models/1040127-shoe-lifter-boot-jack#profileId-1024783",
      ref=N+"SchuhauszieherV2 (1).3mf", names=["SchuhauszieherV2.stl_A_A"], material="PLA",
      license=MW_STD,
      notes=["The designer's 'ohne Support' (no supports) profile; they state it prints "
             "without supports. A with-supports profile exists on the page."]),
 dict(id=48, slug="pencil-grip", title="Adaptive Pencil Grip", designer="DTaylor (Printables)",
      link="https://www.printables.com/model/520212-adaptive-pencil-grip",
      stl=[N+"adaptive-pencil-grip-model_files/Adaptive writer.stl"], material="PLA",
      license="CC BY-NC-SA 4.0",
      notes=["Designer: default settings, no supports. P1S 0.20 mm Standard.",
             "The pencil hole is just over 7 mm; the page's small test piece is left out."]),
]

FILAMENT = {"PLA": PLA, "PETG": PETG}

# a Bambu project holds at most 36 plates, so the one-per-plate catalogue is split
CATALOGUES = {
    1: dict(file="Catalogue - one device per plate.3mf", ids=range(1, 31),
            data="catalogue_data.json", slices="slices_catalogue.json"),
    2: dict(file="Catalogue 2 - one device per plate.3mf", ids=range(31, 49),
            data="catalogue2_data.json", slices="slices_catalogue2.json"),
}
