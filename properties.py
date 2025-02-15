"""
This module defines the (pattern collection) property group that gets assigned to every collection.
"""

from bpy.props import CollectionProperty, IntProperty
from bpy.types import PropertyGroup
from .category_item_properties import BaseItemPropertyGroup, AttributeItemPropertyGroup


# fmt: off
class PatternCollectionPropertyGroup(PropertyGroup):
    included_names: CollectionProperty(name="Included Names", type=BaseItemPropertyGroup)
    excluded_names: CollectionProperty(name="Excluded Names", type=BaseItemPropertyGroup)
    active_included_name_index: IntProperty(name="Active Included Name Index", default=0)
    active_excluded_name_index: IntProperty(name="Active Excluded Name Index", default=0)

    included_hierarchies: CollectionProperty(name="Included Hierarchies", type=BaseItemPropertyGroup)
    excluded_hierarchies: CollectionProperty(name="Excluded Hierarchies", type=BaseItemPropertyGroup)
    active_included_hierarchy_index: IntProperty(name="Active Included Hierarchy Index", default=0)
    active_excluded_hierarchy_index: IntProperty(name="Active Excluded Hierarchy Index", default=0)

    included_types: CollectionProperty(name="Included Types", type=BaseItemPropertyGroup)
    excluded_types: CollectionProperty(name="Excluded Types", type=BaseItemPropertyGroup)
    active_included_type_index: IntProperty(name="Active Included Type Index", default=0)
    active_excluded_type_index: IntProperty(name="Active Excluded Type Index", default=0)

    included_materials: CollectionProperty(name="Included Materials", type=BaseItemPropertyGroup)
    excluded_materials: CollectionProperty(name="Excluded Materials", type=BaseItemPropertyGroup)
    active_included_material_index: IntProperty(name="Active Included Material Index", default=0)
    active_excluded_material_index: IntProperty(name="Active Excluded Material Index", default=0)

    excluded_collections: CollectionProperty(name="Excluded Collections", type=BaseItemPropertyGroup)
    included_collections: CollectionProperty(name="Included Collections", type=BaseItemPropertyGroup)
    active_included_collection_index: IntProperty(name="Active Included Collection Index", default=0)
    active_excluded_collection_index: IntProperty(name="Active Excluded Collection Index", default=0)

    included_uv_layers: CollectionProperty(name="Included UV Layers", type=BaseItemPropertyGroup)
    excluded_uv_layers: CollectionProperty(name="Excluded UV Layers", type=BaseItemPropertyGroup)
    active_included_uv_layer_index: IntProperty(name="Active Included UV Layer Index", default=0)
    active_excluded_uv_layer_index: IntProperty(name="Active Excluded UV Layer Index", default=0)

    included_attributes: CollectionProperty(name="Included Attributes", type=AttributeItemPropertyGroup)
    excluded_attributes: CollectionProperty(name="Excluded Attributes", type=AttributeItemPropertyGroup)
    active_included_attribute_index: IntProperty(name="Active Included Attribute Index", default=0)
    active_excluded_attribute_index: IntProperty(name="Active Excluded Attribute Index", default=0)
# fmt: on