from .. import gui


class PATTERN_COLLECTIONS_UL_included_types(gui.BaseItemUIList):
    pass


class PATTERN_COLLECTIONS_UL_excluded_types(gui.BaseItemUIList):
    pass


class PATTERN_COLLECTIONS_PT_included_types(gui.PATTERN_COLLECTIONS_PT_uilist):
    custom_label = "Included Types"
    uilist_class = "PATTERN_COLLECTIONS_UL_included_types"
    category = "included_types"
    active_index = "active_included_type_index"
    default_name = "context_type"


class PATTERN_COLLECTIONS_PT_excluded_types(gui.PATTERN_COLLECTIONS_PT_uilist):
    custom_label = "Excluded Types"
    uilist_class = "PATTERN_COLLECTIONS_UL_excluded_types"
    category = "excluded_types"
    active_index = "active_excluded_type_index"
    default_name = "context_type"