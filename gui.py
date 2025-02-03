"""
This module defines the vast majority of the graphical user interface.
"""

import bpy
from . import icons
from . import sorting_functions


class BaseItemUIList(bpy.types.UIList):
    """
    List Item UI for sorting categories that don't need anything special.
    """
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        pcoll = icons.preview_collections["main"]

        if self.layout_type in {"DEFAULT", "COMPACT"}:
            row = layout.row(align=True)

            enable_icon = "CHECKBOX_HLT" if item.enable else "CHECKBOX_DEHLT"
            row.prop(item, "enable", text="", icon=enable_icon, emboss=False)
            row.prop(item, "name", text="", emboss=False)

            sub = row.row(align=True)
            sub.alignment = "RIGHT"

            case_sub = sub.row(align=True)
            case_sub.enabled = "REGEX" not in item.anchor
            case_sensitivity_icon = pcoll["CASE_SENSITIVITY_ON"] if item.case_sensitive else pcoll["CASE_SENSITIVITY_OFF"]
            case_sub.prop(item, "case_sensitive", text="", icon_value=case_sensitivity_icon.icon_id, emboss=False)

            sub.prop(item, "anchor", text="", emboss=False)

        elif self.layout_type == "GRID":
            layout.alignment = "CENTER"


class AttributeItemUIList(bpy.types.UIList):
    """
    List Item UI for attribute-sorting categories that make use of the additional 'value' and 'GREATER_THAN'/'LESS_THAN' properties.
    """
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        pcoll = icons.preview_collections["main"]

        if self.layout_type in {"DEFAULT", "COMPACT"}:
            row = layout.row(align=True)

            enable_icon = "CHECKBOX_HLT" if item.enable else "CHECKBOX_DEHLT"
            row.prop(item, "enable", text="", icon=enable_icon, emboss=False)

            row.prop(item, "name", text="", emboss=False)
            row.prop(item, "value", text="", emboss=False)

            sub = row.row(align=True)
            sub.alignment = "RIGHT"

            case_sub = sub.row(align=True)
            case_sub.alignment = "RIGHT"
            case_sub.enabled = not any([s in item.anchor for s in ["REGEX", "GREATER_THAN", "LESS_THAN"]])
            case_sensitivity_icon = pcoll["CASE_SENSITIVITY_ON"] if item.case_sensitive else pcoll["CASE_SENSITIVITY_OFF"]
            case_sub.prop(item, "case_sensitive", text="", icon_value=case_sensitivity_icon.icon_id, emboss=False)

            sub.prop(item, "anchor", text="", emboss=False)

        elif self.layout_type == "GRID":
            layout.alignment = "CENTER"


class PatternCollectionsPanel(bpy.types.Panel):
    """
    Members all pattern collection panels should inherit.
    """
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "collection"

    @classmethod
    def poll(cls, context):
        collection = context.collection
        return collection != context.scene.collection


class PATTERN_COLLECTIONS_PT_pattern_collection(PatternCollectionsPanel):  # MARK: Main Panel
    """
    Main (parent) panel.
    """
    bl_label = "Sorting Pattern"

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        collection = context.collection
        layout = self.layout

        row = layout.row(align=True)
        if collection.name not in sorting_functions.sorting_timers:
            row.operator("collection.register_sort_timer", text="", icon="RADIOBUT_OFF")
        else:
            row.operator("collection.unregister_sort_timer", text="", icon="RADIOBUT_ON", depress=True)
        row.operator("collection.sort_collection")

        col = layout.column(align=True)
        col.operator("collection.import_pattern", text="Import", icon="IMPORT")
        col.operator("collection.export_pattern", text="Export", icon="EXPORT")

        row = layout.row(align=True)
        row.operator("pattern_collections.open_preferences")
        row.operator("pattern_collections.open_tracker")
        row.operator("pattern_collections.open_documentation", text="Docs")


class PATTERN_COLLECTIONS_PT_uilist(PatternCollectionsPanel):
    """
    List panel all sorting category panels should inherit.
    """
    bl_parent_id = "PATTERN_COLLECTIONS_PT_pattern_collection"
    bl_label = ""
    bl_options = {"DEFAULT_CLOSED"}

    uilist_class = ""  # UIList to be displayed
    custom_label = ""  # Panel label override (as the label is currently empty)
    category = ""      # Panels collection property
    active_index = ""  # Active index property
    default_name = ""  # Default name for any added items

    def draw_header(self, context):
        collection = context.collection
        layout = self.layout
        property = getattr(collection.pattern_collection_properties, self.category)
        layout.label(text=f"{self.custom_label} ✱" if property else self.custom_label)

    def draw(self, context):
        collection = context.collection
        object = context.view_layer.objects.active
        layout = self.layout

        row = layout.row(align=False)
        row.template_list(
            self.uilist_class, "",
            collection.pattern_collection_properties, self.category,
            collection.pattern_collection_properties, self.active_index
            )

        match self.default_name:
            case "context_object":
                new_name = object.name if object else "Object"
            case "context_type":
                new_name = object.type if object else "MY_TYPE"
            case "context_material":
                new_name = object.active_material.name if (object and object.active_material) else "Material"
            case "context_uv_layer":
                new_name = object.data.uv_layer_clone.name if object and len(object.data.uv_layers) > 0 else "UVMap"
            case _:
                new_name = self.default_name

        panel_list_operators = []

        col = row.column(align=True)
        add_op = col.operator("list.add_item", icon="ADD", text="")
        add_op.new_name = new_name
        remove_op = col.operator("list.remove_item", icon="REMOVE", text="")
        duplicate_op = col.operator("list.duplicate_item", icon="DUPLICATE", text="")
        panel_list_operators.extend([add_op, remove_op, duplicate_op])

        is_sortable = len(getattr(collection.pattern_collection_properties, self.category)) >= 2
        if is_sortable:
            col.separator()
            up_op = col.operator("list.move_item", icon="TRIA_UP", text="")
            up_op.direction = "UP"
            down_op = col.operator("list.move_item", icon="TRIA_DOWN", text="")
            down_op.direction = "DOWN"
            panel_list_operators.extend([up_op, down_op])

        for op in panel_list_operators:
            op.domain = "collection"
            op.property_group = "pattern_collection_properties"
            op.property = self.category
            if hasattr(op, "idx_property"):
                op.idx_property = self.active_index