from .. import gui


class PATTERN_COLLECTIONS_UL_included_materials(gui.BaseItemUIList):
    pass


class PATTERN_COLLECTIONS_UL_excluded_materials(gui.BaseItemUIList):
    pass


class PATTERN_COLLECTIONS_PT_included_materials(gui.PATTERN_COLLECTIONS_PT_uilist):
    custom_label = "Included Materials"
    uilist_class = "PATTERN_COLLECTIONS_UL_included_materials"
    category = "included_materials"
    active_index = "active_included_material_index"
    default_name = "context_material"


class PATTERN_COLLECTIONS_PT_excluded_materials(gui.PATTERN_COLLECTIONS_PT_uilist):
    custom_label = "Excluded Materials"
    uilist_class = "PATTERN_COLLECTIONS_UL_excluded_materials"
    category = "excluded_materials"
    active_index = "active_excluded_material_index"
    default_name = "context_material"