"""
This module defines the vast majority of the graphical user interface.
"""

import bpy
from . import icons
from . import sorting_functions


class BaseItemUIList(bpy.types.UIList):
    """
    List UI for including or excluding sorting-categories that don't need anything special.
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
    List UI for attribute sorting-categories that make use of the additional 'value' and 'GREATER_THAN'/'LESS_THAN' properties.
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


class PatternCollectionPanel:
    """
    Variables and methods all pattern collection panels should inherit.
    """
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "collection"

    @classmethod
    def poll(cls, context):
        collection = context.collection
        return collection != context.scene.collection


class PATTERN_COLLECTION_PT_pattern_collection(PatternCollectionPanel, bpy.types.Panel):
    """
    Main (parent) panel.
    """
    bl_idname = "PATTERN_COLLECTION_PT_pattern_collection"
    bl_label = "Sorting Pattern"

    def draw(self, context):
        collection = context.collection
        layout = self.layout

        row = layout.row(align=True)
        if collection.name not in sorting_functions.sorting_timers:
            row.operator("pattern_collection.register_timer", text="", icon="RADIOBUT_OFF")
        else:
            row.operator("pattern_collection.unregister_timer", text="", icon="RADIOBUT_ON", depress=True)
        row.operator("pattern_collection.sort_collection")

        col = layout.column()
        col.operator("pattern_collection.import_json", text="Import", icon="IMPORT")
        col.operator("pattern_collection.export_json", text="Export", icon="EXPORT")


class PATTERN_COLLECTION_PT_uilist(PatternCollectionPanel, bpy.types.Panel):
    """
    List panel all sorting category panels should inherit.
    """
    bl_parent_id = "PATTERN_COLLECTION_PT_pattern_collection"
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
        row.template_list(self.uilist_class, "",
                          collection.pattern_collection_properties, self.category,
                          collection.pattern_collection_properties, self.active_index)

        match self.default_name:
            case "context_object":
                add_name = object.name if object else "Object"
            case "context_type":
                add_name = object.type if object else "MYTYPE"
            case "context_material":
                add_name = object.active_material.name if (object and object.active_material) else "Material"
            case "context_uv_layer":
                add_name = object.data.uv_layer_clone.name if object and len(object.data.uv_layers) > 0 else "UVMap"
            case _:
                add_name = self.default_name

        col = row.column(align=True)
        op = col.operator("list.add_item", icon="ADD", text="")
        op.prop = self.category
        op.name = add_name
        op = col.operator("list.remove_item", icon="REMOVE", text="")
        op.prop = self.category
        op.idx_prop = self.active_index
        op = col.operator("list.duplicate_item", icon="DUPLICATE", text="")
        op.prop = self.category
        op.idx_prop = self.active_index

        is_sortable = len(getattr(collection.pattern_collection_properties, self.category)) >= 2
        if is_sortable:
            col.separator()
            op = col.operator("list.move_item", icon="TRIA_UP", text="")
            op.prop = self.category
            op.idx_prop = self.active_index
            op.direction = "UP"
            op = col.operator("list.move_item", icon="TRIA_DOWN", text="")
            op.prop = self.category
            op.idx_prop = self.active_index
            op.direction = "DOWN"
