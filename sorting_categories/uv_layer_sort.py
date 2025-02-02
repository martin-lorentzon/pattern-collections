from .. import gui
import bpy


class PATTERN_COLLECTIONS_UL_included_uv_layers(gui.BaseItemUIList, bpy.types.UIList):
    pass


class PATTERN_COLLECTIONS_UL_excluded_uv_layers(gui.BaseItemUIList, bpy.types.UIList):
    pass


class PATTERN_COLLECTIONS_PT_included_uv_layers(gui.PATTERN_COLLECTIONS_PT_uilist, bpy.types.Panel):
    custom_label = "Included UV Layers"
    uilist_class = "PATTERN_COLLECTIONS_UL_included_uv_layers"
    category = "included_uv_layers"
    active_index = "active_included_uv_layer_index"
    default_name = "context_uv_layer"


class PATTERN_COLLECTIONS_PT_excluded_uv_layers(gui.PATTERN_COLLECTIONS_PT_uilist, bpy.types.Panel):
    custom_label = "Excluded UV Layers"
    uilist_class = "PATTERN_COLLECTIONS_UL_excluded_uv_layers"
    category = "excluded_uv_layers"
    active_index = "active_excluded_uv_layer_index"
    default_name = "context_uv_layer"