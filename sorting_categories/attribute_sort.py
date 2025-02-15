from .. import gui


class PATTERN_COLLECTIONS_UL_included_attributes(gui.AttributeItemUIList):
    pass


class PATTERN_COLLECTIONS_UL_excluded_attributes(gui.AttributeItemUIList):
    pass


class PATTERN_COLLECTIONS_PT_included_attributes(gui.PATTERN_COLLECTIONS_PT_uilist):
    custom_label = "Included Attributes"
    uilist_class = "PATTERN_COLLECTIONS_UL_included_attributes"
    category = "included_attributes"
    active_index = "active_included_attribute_index"
    default_name = "Attribute"


class PATTERN_COLLECTIONS_PT_excluded_attributes(gui.PATTERN_COLLECTIONS_PT_uilist):
    custom_label = "Excluded Attributes"
    uilist_class = "PATTERN_COLLECTIONS_UL_excluded_attributes"
    category = "excluded_attributes"
    active_index = "active_excluded_attribute_index"
    default_name = "Attribute"