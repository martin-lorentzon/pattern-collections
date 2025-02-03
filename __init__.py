bl_info = {
    "name": "Pattern Collections",
    "description": "Pattern-based Collection Sorting",
    "author": "Martin Lorentzon",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "location": "Properties > Collection > Sorting Pattern",
    "doc_url": "https://github.com/martin-lorentzon/blender-pattern-collections",
    "tracker_url": "https://github.com/martin-lorentzon/blender-pattern-collections/issues",
    "support": "COMMUNITY",
    "category": "Tools"
}


if "bpy" in locals():
    from importlib import reload
    reload(addon_preferences)
    reload(icons)
    reload(utils)
    reload(list_utils)
    reload(sorting_functions)
    reload(category_item_properties)
    reload(properties)
    reload(operators)
    reload(gui)
    # Sorting categories
    reload(name_sort)
    reload(hierarchy_sort)
    reload(type_sort)
    reload(material_sort)
    reload(collection_sort)
    reload(uv_layer_sort)
    reload(attribute_sort)
else:
    import bpy
    from . import addon_preferences
    from . import icons
    from . import utils
    from . import list_utils
    from . import sorting_functions
    from . import category_item_properties
    from . import properties
    from . import operators
    from . import gui

    from .sorting_categories import (
        name_sort,
        hierarchy_sort,
        type_sort,
        material_sort,
        collection_sort,
        uv_layer_sort,
        attribute_sort,
    )


classes = (
    addon_preferences.PATTERN_COLLECTIONS_Preferences,

    category_item_properties.BaseItemPropertyGroup,
    category_item_properties.AttributeItemPropertyGroup,

    properties.PatternCollectionPropertyGroup,

    list_utils.LIST_OT_add_item,
    list_utils.LIST_OT_remove_item,
    list_utils.LIST_OT_duplicate_item,
    list_utils.LIST_OT_move_item,

    operators.PATTERN_COLLECTIONS_OT_sort_collection,
    operators.PATTERN_COLLECTIONS_OT_register_timer,
    operators.PATTERN_COLLECTIONS_OT_unregister_timer,
    operators.PATTERN_COLLECTIONS_OT_import_pattern,
    operators.PATTERN_COLLECTIONS_OT_export_pattern,
    operators.PATTERN_COLLECTIONS_OT_open_preferences,
    operators.PATTERN_COLLECTIONS_OT_open_tracker,
    operators.PATTERN_COLLECTIONS_OT_open_documentation,

    gui.PATTERN_COLLECTIONS_PT_pattern_collection,

    # region Sorting categories classes
    name_sort.PATTERN_COLLECTIONS_UL_included_names,
    name_sort.PATTERN_COLLECTIONS_UL_excluded_names,
    name_sort.PATTERN_COLLECTIONS_PT_included_names,
    name_sort.PATTERN_COLLECTIONS_PT_excluded_names,

    hierarchy_sort.PATTERN_COLLECTIONS_UL_included_hierarchies,
    hierarchy_sort.PATTERN_COLLECTIONS_UL_excluded_hierarchies,
    hierarchy_sort.PATTERN_COLLECTIONS_PT_included_hierarchies,
    hierarchy_sort.PATTERN_COLLECTIONS_PT_excluded_hierarchies,

    type_sort.PATTERN_COLLECTIONS_UL_included_types,
    type_sort.PATTERN_COLLECTIONS_UL_excluded_types,
    type_sort.PATTERN_COLLECTIONS_PT_included_types,
    type_sort.PATTERN_COLLECTIONS_PT_excluded_types,

    material_sort.PATTERN_COLLECTIONS_UL_included_materials,
    material_sort.PATTERN_COLLECTIONS_UL_excluded_materials,
    material_sort.PATTERN_COLLECTIONS_PT_included_materials,
    material_sort.PATTERN_COLLECTIONS_PT_excluded_materials,

    collection_sort.PATTERN_COLLECTIONS_UL_included_collections,
    collection_sort.PATTERN_COLLECTIONS_UL_excluded_collections,
    collection_sort.PATTERN_COLLECTIONS_PT_included_collections,
    collection_sort.PATTERN_COLLECTIONS_PT_excluded_collections,

    uv_layer_sort.PATTERN_COLLECTIONS_UL_included_uv_layers,
    uv_layer_sort.PATTERN_COLLECTIONS_UL_excluded_uv_layers,
    uv_layer_sort.PATTERN_COLLECTIONS_PT_included_uv_layers,
    uv_layer_sort.PATTERN_COLLECTIONS_PT_excluded_uv_layers,

    attribute_sort.PATTERN_COLLECTIONS_UL_included_attributes,
    attribute_sort.PATTERN_COLLECTIONS_UL_excluded_attributes,
    attribute_sort.PATTERN_COLLECTIONS_PT_included_attributes,
    attribute_sort.PATTERN_COLLECTIONS_PT_excluded_attributes,
    # endregion
)

preview_collections = {}


def register():
    import os
    import bpy.utils.previews
    from bpy.app.handlers import persistent
    
    pcoll = bpy.utils.previews.new()
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    pcoll.load("CASE_SENSITIVITY_ON", os.path.join(icons_dir, "case_sensitivity_on.png"), "IMAGE")
    pcoll.load("CASE_SENSITIVITY_OFF", os.path.join(icons_dir, "case_sensitivity_off.png"), "IMAGE")
    icons.preview_collections["main"] = pcoll

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Collection.pattern_collection_properties = bpy.props.PointerProperty(
        type=properties.PatternCollectionPropertyGroup,
        name="Pattern"
        )

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
