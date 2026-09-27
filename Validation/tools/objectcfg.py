#!/usr/bin/env python3
"""Which settings can be baked onto an individual object.

These are Bambu's PrintObjectConfig + PrintRegionConfig options: written as
<metadata key=... value=.../> under <object> in model_settings.config, they stick to the
object even if someone switches process preset, and they are what lets one project hold
plates with different layer heights, wall counts and supports. Anything outside this list
is print-level and would be silently ignored, so it is never written here.

The catalogue file is validated by slicing: each plate must produce the same time and
filament as the matching single-device file, which is what proves these took effect.
"""

OBJECT_SCOPED = [
    "layer_height", "wall_loops", "wall_generator", "wall_sequence",
    "top_shell_layers", "top_shell_thickness", "bottom_shell_layers",
    "bottom_shell_thickness", "ensure_vertical_shell_thickness",
    "sparse_infill_density", "sparse_infill_pattern", "skin_infill_density",
    "skeleton_infill_density", "top_surface_pattern", "bottom_surface_pattern",
    "infill_direction", "infill_combination", "minimum_sparse_infill_area",
    "infill_wall_overlap", "detect_narrow_internal_solid_infill",
    "seam_position", "seam_gap", "detect_thin_wall", "detect_overhang_wall",
    "bridge_flow", "bridge_no_support", "max_bridge_length",
    "ironing_type", "ironing_flow", "ironing_spacing",
    "inner_wall_line_width", "outer_wall_line_width", "top_surface_line_width",
    "internal_solid_infill_line_width", "sparse_infill_line_width", "support_line_width",
    "outer_wall_speed", "inner_wall_speed", "sparse_infill_speed",
    "internal_solid_infill_speed", "top_surface_speed", "gap_infill_speed",
    "bridge_speed", "support_speed", "support_interface_speed",
    "brim_type", "brim_width", "brim_object_gap", "raft_layers",
    "xy_hole_compensation", "xy_contour_compensation", "elefant_foot_compensation",
    "enable_support", "support_type", "support_style", "support_threshold_angle",
    "support_on_build_plate_only", "support_critical_regions_only",
    "support_top_z_distance", "support_bottom_z_distance", "support_object_xy_distance",
    "support_object_first_layer_gap", "support_base_pattern",
    "support_base_pattern_spacing", "support_expansion", "support_interface_top_layers",
    "support_interface_bottom_layers", "support_interface_spacing",
    "support_interface_pattern", "support_interface_loop_pattern",
    "support_remove_small_overhang", "support_angle", "enforce_support_layers",
    "tree_support_branch_angle", "tree_support_branch_distance",
    "tree_support_branch_diameter", "tree_support_wall_count",
    "independent_support_layer_height",
]


def one(v):
    if isinstance(v, list):
        return str(v[0]) if v else ""
    return str(v)


def bake(cfg, ref_overrides=None, keys=None):
    """Per-object metadata for an object printed with `cfg`; the reference's own
    per-object overrides win over the device profile."""
    keys = keys or OBJECT_SCOPED
    md = {k: one(cfg[k]) for k in keys if k in cfg}
    for k, v in (ref_overrides or []):
        if k in keys:
            md[k] = one(v)
    return sorted(md.items())
