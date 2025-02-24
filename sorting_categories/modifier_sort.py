from .. import gui


class PATTERN_COLLECTIONS_UL_included_modifiers(gui.BaseItemUIList):
    pass


class PATTERN_COLLECTIONS_UL_excluded_modifiers(gui.BaseItemUIList):
    pass


class PATTERN_COLLECTIONS_PT_included_modifiers(gui.PATTERN_COLLECTIONS_PT_uilist):
    custom_label = "Included Modifers"
    uilist_class = "PATTERN_COLLECTIONS_UL_included_modifiers"
    category = "included_modifiers"
    active_index = "active_included_modifier_index"
    default_name = "context_modifier"


class PATTERN_COLLECTIONS_PT_excluded_modifiers(gui.PATTERN_COLLECTIONS_PT_uilist):
    custom_label = "Excluded Modifers"
    uilist_class = "PATTERN_COLLECTIONS_UL_excluded_modifiers"
    category = "excluded_modifiers"
    active_index = "active_excluded_modifier_index"
    default_name = "context_modifier"