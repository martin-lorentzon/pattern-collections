from .. import gui
import bpy


class PATTERN_COLLECTIONS_UL_included_names(gui.BaseItemUIList, bpy.types.UIList):
    pass


class PATTERN_COLLECTIONS_UL_excluded_names(gui.BaseItemUIList, bpy.types.UIList):
    pass


class PATTERN_COLLECTIONS_PT_included_names(gui.PATTERN_COLLECTIONS_PT_uilist, bpy.types.Panel):
    custom_label = "Included Names"
    uilist_class = "PATTERN_COLLECTIONS_UL_included_names"
    category = "included_names"
    active_index = "active_included_name_index"
    default_name = "context_object"


class PATTERN_COLLECTIONS_PT_excluded_names(gui.PATTERN_COLLECTIONS_PT_uilist, bpy.types.Panel):
    custom_label = "Excluded Names"
    uilist_class = "PATTERN_COLLECTIONS_UL_excluded_names"
    category = "excluded_names"
    active_index = "active_excluded_name_index"
    default_name = "context_object"