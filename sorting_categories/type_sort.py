from .. import gui
import bpy


class PATTERN_COLLECTION_UL_included_types(gui.BaseItemUIList, bpy.types.UIList):
    pass


class PATTERN_COLLECTION_UL_excluded_types(gui.BaseItemUIList, bpy.types.UIList):
    pass


class PATTERN_COLLECTION_PT_included_types(gui.PATTERN_COLLECTION_PT_uilist, bpy.types.Panel):
    custom_label = "Included Types"
    uilist_class = "PATTERN_COLLECTION_UL_included_types"
    category = "included_types"
    active_index = "active_included_type_index"
    default_name = "context_type"


class PATTERN_COLLECTION_PT_excluded_types(gui.PATTERN_COLLECTION_PT_uilist, bpy.types.Panel):
    custom_label = "Excluded Types"
    uilist_class = "PATTERN_COLLECTION_UL_excluded_types"
    category = "excluded_types"
    active_index = "active_excluded_type_index"
    default_name = "context_type"