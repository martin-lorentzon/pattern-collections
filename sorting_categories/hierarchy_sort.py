from .. import gui


class PATTERN_COLLECTIONS_UL_included_hierarchies(gui.BaseItemUIList):
    pass


class PATTERN_COLLECTIONS_UL_excluded_hierarchies(gui.BaseItemUIList):
    pass


class PATTERN_COLLECTIONS_PT_included_hierarchies(gui.PATTERN_COLLECTIONS_PT_uilist):
    custom_label = "Included Hierarchies"
    uilist_class = "PATTERN_COLLECTIONS_UL_included_hierarchies"
    category = "included_hierarchies"
    active_index = "active_included_hierarchy_index"
    default_name = "context_object"


class PATTERN_COLLECTIONS_PT_excluded_hierarchies(gui.PATTERN_COLLECTIONS_PT_uilist):
    custom_label = "Excluded hierarchies"
    uilist_class = "PATTERN_COLLECTIONS_UL_excluded_hierarchies"
    category = "excluded_hierarchies"
    active_index = "active_excluded_hierarchy_index"
    default_name = "context_object"