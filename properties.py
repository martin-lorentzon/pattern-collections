"""
This module defines the (pattern collection) property group that gets assigned to every collection.
"""

import bpy
from . import category_item_properties


# fmt: off
class PatternCollectionPropertyGroup(bpy.types.PropertyGroup):
    included_names: bpy.props.CollectionProperty(name="Included Names", type=category_item_properties.BaseItemPropertyGroup)
    excluded_names: bpy.props.CollectionProperty(name="Excluded Names", type=category_item_properties.BaseItemPropertyGroup)
    active_included_name_index: bpy.props.IntProperty(name="Active Included Name Index", default=0)
    active_excluded_name_index: bpy.props.IntProperty(name="Active Excluded Name Index", default=0)

    included_hierarchies: bpy.props.CollectionProperty(name="Included Hierarchies", type=category_item_properties.BaseItemPropertyGroup)
    excluded_hierarchies: bpy.props.CollectionProperty(name="Excluded Hierarchies", type=category_item_properties.BaseItemPropertyGroup)
    active_included_hierarchy_index: bpy.props.IntProperty(name="Active Included Hierarchy Index", default=0)
    active_excluded_hierarchy_index: bpy.props.IntProperty(name="Active Excluded Hierarchy Index", default=0)

    included_types: bpy.props.CollectionProperty(name="Included Types", type=category_item_properties.BaseItemPropertyGroup)
    excluded_types: bpy.props.CollectionProperty(name="Excluded Types", type=category_item_properties.BaseItemPropertyGroup)
    active_included_type_index: bpy.props.IntProperty(name="Active Included Type Index", default=0)
    active_excluded_type_index: bpy.props.IntProperty(name="Active Excluded Type Index", default=0)

    included_materials: bpy.props.CollectionProperty(name="Included Materials", type=category_item_properties.BaseItemPropertyGroup)
    excluded_materials: bpy.props.CollectionProperty(name="Excluded Materials", type=category_item_properties.BaseItemPropertyGroup)
    active_included_material_index: bpy.props.IntProperty(name="Active Included Material Index", default=0)
    active_excluded_material_index: bpy.props.IntProperty(name="Active Excluded Material Index", default=0)

    included_collections: bpy.props.CollectionProperty(name="Included Collections", type=category_item_properties.BaseItemPropertyGroup)
    excluded_collections: bpy.props.CollectionProperty(name="Excluded Collections", type=category_item_properties.BaseItemPropertyGroup)
    active_included_collection_index: bpy.props.IntProperty(name="Active Included Collection Index", default=0)
    active_excluded_collection_index: bpy.props.IntProperty(name="Active Excluded Collection Index", default=0)

    included_uv_layers: bpy.props.CollectionProperty(name="Included UV Layers", type=category_item_properties.BaseItemPropertyGroup)
    excluded_uv_layers: bpy.props.CollectionProperty(name="Excluded UV Layers", type=category_item_properties.BaseItemPropertyGroup)
    active_included_uv_layer_index: bpy.props.IntProperty(name="Active Included UV Layer Index", default=0)
    active_excluded_uv_layer_index: bpy.props.IntProperty(name="Active Excluded UV Layer Index", default=0)

    included_attributes: bpy.props.CollectionProperty(name="Included Attributes", type=category_item_properties.AttributeItemPropertyGroup)
    excluded_attributes: bpy.props.CollectionProperty(name="Excluded Attributes", type=category_item_properties.AttributeItemPropertyGroup)
    active_included_attribute_index: bpy.props.IntProperty(name="Active Included Attribute Index", default=0)
    active_excluded_attribute_index: bpy.props.IntProperty(name="Active Excluded Attribute Index", default=0)
# fmt: on