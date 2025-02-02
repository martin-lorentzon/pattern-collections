bl_info = {
    "name": "Pattern Collections",
    "description": "Sort scene objects by anything",
    "author": "Martin Lorentzon",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "location": "Properties > Collection > Sorting Pattern",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "User Interface"
}


if "bpy" in locals():
    import importlib
    importlib.reload(utils)
    importlib.reload(list_utils)
    importlib.reload(sorting_functions)
    importlib.reload(category_item_properties)
    importlib.reload(properties)
    importlib.reload(operators)
    importlib.reload(icons)
    importlib.reload(gui)
    importlib.reload(name_sort)
    importlib.reload(hierarchy_sort)
    importlib.reload(type_sort)
    importlib.reload(material_sort)
    importlib.reload(collection_sort)
    importlib.reload(uv_layer_sort)
    importlib.reload(attribute_sort)
else:
    from . import utils
    from . import list_utils
    from . import sorting_functions
    from . import category_item_properties
    from . import properties
    from . import operators
    from . import icons
    from . import gui
    from .sorting_categories import name_sort
    from .sorting_categories import hierarchy_sort
    from .sorting_categories import type_sort
    from .sorting_categories import material_sort
    from .sorting_categories import collection_sort
    from .sorting_categories import uv_layer_sort
    from .sorting_categories import attribute_sort

import bpy
import os


classes = (
    category_item_properties.BaseItemPropertyGroup,
    category_item_properties.AttributeItemPropertyGroup,

    properties.PatternCollectionPropertyGroup,

    list_utils.LIST_OT_add_item,
    list_utils.LIST_OT_remove_item,
    list_utils.LIST_OT_duplicate_item,
    list_utils.LIST_OT_move_item,

    operators.PATTERN_COLLECTION_OT_sort_collection,
    operators.PATTERN_COLLECTION_OT_register_timer,
    operators.PATTERN_COLLECTION_OT_unregister_timer,
    operators.PATTERN_COLLECTION_OT_import_json,
    operators.PATTERN_COLLECTION_OT_export_json,

    gui.PATTERN_COLLECTION_PT_pattern_collection,


    # region Sorting Categories Classes
    name_sort.PATTERN_COLLECTION_UL_included_names,
    name_sort.PATTERN_COLLECTION_UL_excluded_names,
    name_sort.PATTERN_COLLECTION_PT_included_names,
    name_sort.PATTERN_COLLECTION_PT_excluded_names,

    hierarchy_sort.PATTERN_COLLECTION_UL_included_hierarchies,
    hierarchy_sort.PATTERN_COLLECTION_UL_excluded_hierarchies,
    hierarchy_sort.PATTERN_COLLECTION_PT_included_hierarchies,
    hierarchy_sort.PATTERN_COLLECTION_PT_excluded_hierarchies,

    type_sort.PATTERN_COLLECTION_UL_included_types,
    type_sort.PATTERN_COLLECTION_UL_excluded_types,
    type_sort.PATTERN_COLLECTION_PT_included_types,
    type_sort.PATTERN_COLLECTION_PT_excluded_types,

    material_sort.PATTERN_COLLECTION_UL_included_materials,
    material_sort.PATTERN_COLLECTION_UL_excluded_materials,
    material_sort.PATTERN_COLLECTION_PT_included_materials,
    material_sort.PATTERN_COLLECTION_PT_excluded_materials,

    collection_sort.PATTERN_COLLECTION_UL_included_collections,
    collection_sort.PATTERN_COLLECTION_UL_excluded_collections,
    collection_sort.PATTERN_COLLECTION_PT_included_collections,
    collection_sort.PATTERN_COLLECTION_PT_excluded_collections,

    uv_layer_sort.PATTERN_COLLECTION_UL_included_uv_layers,
    uv_layer_sort.PATTERN_COLLECTION_UL_excluded_uv_layers,
    uv_layer_sort.PATTERN_COLLECTION_PT_included_uv_layers,
    uv_layer_sort.PATTERN_COLLECTION_PT_excluded_uv_layers,

    attribute_sort.PATTERN_COLLECTION_UL_included_attributes,
    attribute_sort.PATTERN_COLLECTION_UL_excluded_attributes,
    attribute_sort.PATTERN_COLLECTION_PT_included_attributes,
    attribute_sort.PATTERN_COLLECTION_PT_excluded_attributes,
    # endregion
)

preview_collections = {}

def register():
    import bpy.utils.previews
    from bpy.app.handlers import persistent
    
    pcoll = bpy.utils.previews.new()
    my_icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    pcoll.load("CASE_SENSITIVITY_ON", os.path.join(my_icons_dir, "case_sensitivity_on.png"), "IMAGE")
    pcoll.load("CASE_SENSITIVITY_OFF", os.path.join(my_icons_dir, "case_sensitivity_off.png"), "IMAGE")
    icons.preview_collections["main"] = pcoll

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Collection.pattern_collection_properties = bpy.props.PointerProperty(
        type=properties.PatternCollectionPropertyGroup,
        name="Pattern")
    
    @persistent
    def load_handler(dummy):
        sorting_functions.sorting_timers.clear()

    bpy.app.handlers.load_post.append(load_handler)


def unregister():
    import bpy.utils.previews

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Collection.pattern_collection_properties

    for pcoll in icons.preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    icons.preview_collections.clear()


if __name__ == "__main__":
    register()
