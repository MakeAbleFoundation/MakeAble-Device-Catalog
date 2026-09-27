#!/usr/bin/env python3
"""Build a P1S project profile for one device.

Precedence, high to low:
  1. machine keys            -> always the P1S system preset (never the designer's printer)
  2. filament keys           -> always the filament the user picked
  3. speeds / accelerations / elephant-foot -> the P1S preset, UNLESS the designer changed
     that value in their own preset (then their value is a deliberate choice and wins)
  4. every other process key -> the designer's effective value from the reference 3mf
  5. explicit overrides made on purpose, each recorded for the report
"""
import json
from resolve_preset import resolve

SKELETON_3MF = "/Users/justinrui/Desktop/M/Tube Opener/Tube_Opener.3mf"   # P1S, Studio 2.2.2
MACHINE = "Bambu Lab P1S 0.4 nozzle"
STUDIO_VERSION = "02.02.02.56"

META_KEYS = {"type", "name", "from", "setting_id", "instantiation", "inherits",
             "is_custom_defined", "version", "different_settings_to_system",
             "inherits_group", "print_settings_id", "filament_settings_id",
             "printer_settings_id", "print_compatible_printers", "filament_ids",
             "filament_id", "print_sequence_customized",
             # compatibility bookkeeping: belongs to the preset, never to a project copy
             "compatible_printers", "compatible_printers_condition", "compatible_prints",
             "compatible_prints_condition", "upward_compatible_machine",
             "default_print_profile", "default_filament_profile", "printer_technology",
             "description", "filament_description"}

# Tied to the machine, not the model: these follow the P1S preset unless the designer
# deliberately moved them away from their own printer's default.
KINEMATIC = {
    "default_acceleration", "travel_speed", "travel_speed_z", "travel_acceleration",
    "initial_layer_acceleration", "initial_layer_travel_acceleration",
    "outer_wall_acceleration", "inner_wall_acceleration", "top_surface_acceleration",
    "sparse_infill_acceleration", "internal_solid_infill_acceleration",
    "bridge_acceleration", "accel_to_decel_enable", "accel_to_decel_factor",
    "smooth_coefficient", "smooth_speed_discontinuity_area", "enable_height_slowdown",
    "slowdown_start_speed", "slowdown_start_acc", "slowdown_start_height",
    "slowdown_end_speed", "slowdown_end_acc", "slowdown_end_height",
    "elefant_foot_compensation",
    "outer_wall_speed", "inner_wall_speed", "sparse_infill_speed",
    "internal_solid_infill_speed", "top_surface_speed", "gap_infill_speed",
    "support_speed", "support_interface_speed", "bridge_speed", "initial_layer_speed",
    "initial_layer_infill_speed", "small_perimeter_speed", "small_perimeter_threshold",
    "vertical_shell_speed", "overhang_1_4_speed", "overhang_2_4_speed",
    "overhang_3_4_speed", "overhang_4_4_speed", "overhang_totally_speed",
    "print_extruder_id", "print_extruder_variant", "enable_overhang_speed",
    "max_volumetric_extrusion_rate_slope",
    "max_volumetric_extrusion_rate_slope_segment_length",
}

PRESET_MAP = {
    "0.20mm Standard @BBL A1M": "0.20mm Standard @BBL X1C",
    "0.20mm Strength @BBL A1M": "0.20mm Strength @BBL X1C",
    "0.20mm Standard @BBL H2S": "0.20mm Standard @BBL X1C",
    "0.20mm Standard @BBL P2S": "0.20mm Standard @BBL X1C",
    "0.16mm Optimal @BBL P2S": "0.16mm Optimal @BBL X1C",
    "0.20mm Standard @BBL A1": "0.20mm Standard @BBL X1C",
}

ALIASES = {
    # same meaning, different vocabulary between slicer generations
    "ensure_vertical_shell_thickness": [{"0", "disabled", "none"},
                                        {"1", "enabled", "ensure_all", "all"}],
}


def norm(v):
    return [str(x) for x in v] if isinstance(v, list) else [str(v)]


def same(a, b, key=None):
    """Equal after list/scalar normalisation, allowing enum renames and numeric equality."""
    na, nb = norm(a), norm(b)
    if na == nb:
        return True
    if len(na) != len(nb):
        return False
    groups = ALIASES.get(key or "")
    for x, y in zip(na, nb):
        if x == y:
            continue
        if groups and any(x in g and y in g for g in groups):
            continue
        try:
            if abs(float(x) - float(y)) < 1e-9:
                continue
        except ValueError:
            return False
        return False
    return True


def coerce(value, like):
    """Give `value` the shape the target key already uses (scalar vs 1-element list)."""
    n = norm(value)
    if isinstance(like, list):
        return n[:1] if len(like) == 1 else n
    return n[0]


def skeleton():
    import zipfile
    return json.loads(zipfile.ZipFile(SKELETON_3MF).read("Metadata/project_settings.config"))


def preset_keys(d):
    return {k: v for k, v in d.items() if k not in META_KEYS}


def p1s_process_for(ref_preset, inherits=None):
    if ref_preset in PRESET_MAP:
        return PRESET_MAP[ref_preset], ref_preset
    try:
        resolve("process", ref_preset)
        return ref_preset, ref_preset
    except FileNotFoundError:
        base = inherits or "0.20mm Standard @BBL X1C"
        return PRESET_MAP.get(base, base), base


def build(ref_settings, ref_preset, inherits, filaments, overrides=None, process_from=None):
    """Return (project_settings, info)."""
    out = skeleton()
    machine = preset_keys(resolve("machine", MACHINE))
    target_preset, base_preset = p1s_process_for(process_from or ref_preset, inherits)
    proc_full = resolve("process", target_preset)
    proc = preset_keys(proc_full)
    try:
        base = preset_keys(resolve("process", base_preset))
        base_note = None
    except FileNotFoundError:
        base, base_note = {}, f"{base_preset} is not in this Studio's profile set"

    fil_presets = [preset_keys(resolve("filament", f)) for f in filaments]
    fil_keys = set().union(*[set(f) for f in fil_presets]) if fil_presets else set()

    # keys that carry one value per filament slot: rebuild them for OUR spools rather
    # than inheriting the count from whatever the designer had loaded. Matched by name,
    # never by list length -- printable_area is also a 4-element list.
    n_sk = len(out.get("filament_settings_id", [1]))
    slot_keys = {k for k in out if k.startswith(("filament_", "flush_", "default_filament",
                                                 "extruder_ams", "prime_tower", "wipe_tower"))}
    slot_keys |= {"pre_start_fan_time", "enable_pressure_advance",
                  "enable_overhang_bridge_fan", "nozzle_temperature",
                  "nozzle_temperature_initial_layer", "long_retractions_when_cut",
                  "retraction_distances_when_cut", "impact_strength_z",
                  "physical_extruder_map", "wall_filament", "sparse_infill_filament",
                  "solid_infill_filament", "support_filament",
                  "support_interface_filament", "ooze_prevention",
                  "first_layer_sequence_choice", "other_layers_sequence_choice"}
    # per-EXTRUDER settings look filament-ish but track the printer's extruder count,
    # which is 1 on a P1S. Expanding them per filament makes the slicer reject the
    # project ("Flush volumes matrix do not match to the correct size").
    slot_keys -= {"flush_multiplier", "physical_extruder_map", "extruder_ams_count",
                  "filament_map_mode", "extruder_type", "extruder_printable_area",
                  "extruder_printable_height"}
    slot_keys &= set(out)
    slot_keys -= fil_keys

    out.update(machine)
    out["printer_settings_id"] = MACHINE
    out["printer_model"] = "Bambu Lab P1S"
    out["printer_variant"] = "0.4"
    out.update(proc)
    out["print_settings_id"] = target_preset

    # what the designer explicitly modified in their own project, as Studio recorded it
    dss = (ref_settings or {}).get("different_settings_to_system")
    explicit = set()
    if isinstance(dss, list) and dss:
        explicit = {x for x in str(dss[0]).split(";") if x}
    elif isinstance(dss, str):
        explicit = {x for x in dss.split(";") if x}

    taken, kept_p1s, ambiguous = {}, {}, {}
    for k, rv in (ref_settings or {}).items():
        if k in META_KEYS or k in machine or k in fil_keys or k in slot_keys or k not in out:
            continue
        if same(rv, out[k], k):
            continue
        in_base = k in base
        designer_moved = (k in explicit) or (in_base and not same(rv, base[k], k))
        if k in KINEMATIC and not base:
            # designer's preset isn't in this Studio (e.g. a P2S profile): without a
            # baseline we can't tell a choice from a default, so machine-side values
            # stay P1S rather than importing another printer's kinematics
            kept_p1s[k] = (norm(rv)[0], norm(out[k])[0])
            ambiguous[k] = (norm(rv)[0], norm(out[k])[0])
            continue
        if not designer_moved and (in_base or base):
            kept_p1s[k] = (norm(rv)[0], norm(out[k])[0])
            if not in_base:
                ambiguous[k] = (norm(rv)[0], norm(out[k])[0])
            continue
        new = coerce(rv, out[k])
        taken[k] = (norm(out[k])[0] if not isinstance(out[k], list) or len(out[k]) == 1
                    else str(out[k]),
                    norm(new)[0] if len(norm(new)) == 1 else str(new))
        out[k] = new

    for k in fil_keys:
        vals = []
        for f in fil_presets:
            v = f.get(k)
            if v is None:
                v = out.get(k)
            if isinstance(v, list):
                v = v[0] if v else ""
            vals.append(v)
        out[k] = vals
    n = len(filaments)
    for k in slot_keys:
        v = out.get(k)
        if not isinstance(v, list) or not v:
            continue
        if len(v) == n_sk * n_sk and n_sk > 1:
            out[k] = ["0"] * (n * n)
        elif len(v) == 2 * n_sk:
            out[k] = [str(v[0])] * (2 * n)
        else:
            out[k] = [str(v[0])] * n
    out["filament_settings_id"] = list(filaments)
    out["filament_colour"] = ["#00AE42", "#0080FF", "#F72323", "#FFFFFF"][:n]
    out["filament_ids"] = [""] * n
    out["filament_map"] = ["1"] * n
    out["flush_volumes_matrix"] = ["0"] * (n * n)
    out["flush_volumes_vector"] = ["140"] * (2 * n)
    out["filament_multi_colour"] = list(out["filament_colour"])
    out["filament_self_index"] = [str(i) for i in range(1, n + 1)]
    if proc_full.get("compatible_printers"):
        out["print_compatible_printers"] = list(proc_full["compatible_printers"])
    out["enable_prime_tower"] = "0"          # one material per plate
    out["version"] = STUDIO_VERSION

    applied = {}
    for k, v in (overrides or {}).items():
        applied[k] = (out.get(k), v)
        out[k] = v

    fil_diff = []
    for name, f in zip(filaments, fil_presets):
        try:
            sysname = resolve("filament", name).get("inherits") or name
            b = preset_keys(resolve("filament", sysname))
            fil_diff.append(";".join(sorted(k for k, v in f.items()
                                            if k in b and not same(v, b[k], k))))
        except FileNotFoundError:
            fil_diff.append("")
    out["different_settings_to_system"] = [
        ";".join(sorted(set(taken) | set(applied)))] + fil_diff + [""]

    info = dict(target_preset=target_preset, base_preset=base_preset, base_note=base_note,
                from_reference=taken, kept_p1s=kept_p1s, ambiguous=ambiguous,
                overrides=applied, filaments=list(filaments))
    return out, info
