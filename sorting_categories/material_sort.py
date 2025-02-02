from .. import gui
import bpy


class PATTERN_COLLECTION_UL_included_materials(gui.BaseItemUIList, bpy.types.UIList):
    pass


class PATTERN_COLLECTION_UL_excluded_materials(gui.BaseItemUIList, bpy.types.UIList):
    pass


class PATTERN_COLLECTION_PT_included_materials(gui.PATTERN_COLLECTION_PT_uilist, bpy.types.Panel):
    custom_label = "Included Materials"
    uilist_class = "PATTERN_COLLECTION_UL_included_materials"
    category = "included_materials"
    active_index = "active_included_material_index"
    default_name = "context_material"


class PATTERN_COLLECTION_PT_excluded_materials(gui.PATTERN_COLLECTION_PT_uilist, bpy.types.Panel):
    custom_label = "Excluded Materials"
    uilist_class = "PATTERN_COLLECTION_UL_excluded_materials"
    category = "excluded_materials"
    active_index = "active_excluded_material_index"
    default_name = "context_material"