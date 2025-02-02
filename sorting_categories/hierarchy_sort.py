from .. import gui
import bpy


class PATTERN_COLLECTION_UL_included_hierarchies(gui.BaseItemUIList, bpy.types.UIList):
    pass


class PATTERN_COLLECTION_UL_excluded_hierarchies(gui.BaseItemUIList, bpy.types.UIList):
    pass


class PATTERN_COLLECTION_PT_included_hierarchies(gui.PATTERN_COLLECTION_PT_uilist, bpy.types.Panel):
    custom_label = "Included Hierarchies"
    uilist_class = "PATTERN_COLLECTION_UL_included_hierarchies"
    category = "included_hierarchies"
    active_index = "active_included_hierarchy_index"
    default_name = "context_object"


class PATTERN_COLLECTION_PT_excluded_hierarchies(gui.PATTERN_COLLECTION_PT_uilist, bpy.types.Panel):
    custom_label = "Excluded hierarchies"
    uilist_class = "PATTERN_COLLECTION_UL_excluded_hierarchies"
    category = "excluded_hierarchies"
    active_index = "active_excluded_hierarchy_index"
    default_name = "context_object"