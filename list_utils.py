"""
Generic list operators.
"""

import bpy
from bpy.types import Operator
from bpy.props import StringProperty, EnumProperty
from bl_math import clamp


def get_property_group(context, domain: str, group: str):
    context_domain = getattr(context, domain, None)
    property_group = getattr(context_domain, group, None)
    return property_group


class LIST_OT_add_item(Operator):
    bl_idname = "list.add_item"
    bl_label = "Add Item"
    bl_description = "Add a new item"
    bl_options = {"REGISTER", "UNDO"}

    domain: StringProperty()
    property_group: StringProperty()

    property: StringProperty()
    new_name: StringProperty(default="New Item")

    def execute(self, context):
        properties = get_property_group(context, self.domain, self.property_group)
        collection_property = getattr(properties, self.property, None)

        if collection_property is None:
            self.report({"WARNING"}, "Unable to add item")
            return {"CANCELLED"}

        new_item = collection_property.add()
        new_item.name = self.new_name
        return {"FINISHED"}


class LIST_OT_remove_item(Operator):
    bl_idname = "list.remove_item"
    bl_label = "Remove Item"
    bl_description = "Remove the active item"
    bl_options = {"REGISTER", "UNDO"}

    domain: StringProperty()
    property_group: StringProperty()

    property: StringProperty()
    idx_property: StringProperty()

    def execute(self, context):
        properties = get_property_group(context, self.domain, self.property_group)
        collection_property = getattr(properties, self.property, None)
        index = getattr(properties, self.idx_property, -1)

        if collection_property is None or index < 0:
            self.report({"WARNING"}, f"Unable to remove item, index {index}")
            return {"CANCELLED"}

        collection_property.remove(index)

        idx_min = 0
        idx_max = len(collection_property) - 1 if collection_property else 0

        setattr(properties, self.idx_property, int(clamp(index, idx_min, idx_max)))
        return {"FINISHED"}


class LIST_OT_duplicate_item(Operator):
    bl_idname = "list.duplicate_item"
    bl_label = "Duplicate Item"
    bl_description = "Duplicate the active item"
    bl_options = {"REGISTER", "UNDO"}

    domain: StringProperty()
    property_group: StringProperty()

    property: StringProperty()
    idx_property: StringProperty()

    def execute(self, context):
        properties = get_property_group(context, self.domain, self.property_group)
        collection_property = getattr(properties, self.property, None)
        index = getattr(properties, self.idx_property, -1)

        if collection_property is None or index < 0:
            self.report({"WARNING"}, f"Unable to duplicate item, index {index}")
            return {"CANCELLED"}

        original_item = collection_property[index]
        new_item = collection_property.add()

        for attr in dir(original_item):
            if not attr.startswith("_") and not callable(getattr(original_item, attr)):
                try:
                    setattr(new_item, attr, getattr(original_item, attr))
                except AttributeError:
                    pass  # Skip read-only or protected attributes

        idx_min = 0
        idx_max = len(collection_property) - 1 if collection_property else 0

        setattr(properties, self.idx_property, int(clamp(index, idx_min, idx_max)))
        return {"FINISHED"}


class LIST_OT_move_item(bpy.types.Operator):
    bl_idname = "list.move_item"
    bl_label = "Move Item"
    bl_description = "Move the active item up/down in the list"
    bl_options = {"REGISTER", "UNDO"}

    domain: StringProperty()
    property_group: StringProperty()

    property: StringProperty()
    idx_property: StringProperty()

    direction: EnumProperty(
        items=[("UP", "Up", ""),
               ("DOWN", "Down", "")]
        )

    def execute(self, context):
        properties = get_property_group(context, self.domain, self.property_group)
        collection_property = getattr(properties, self.property, None)
        index = getattr(properties, self.idx_property, -1)

        if collection_property is None or index < 0:
            self.report({"WARNING"}, f"Unable to move item, index {index}")
            return {"CANCELLED"}

        neighbor = index + (-1 if self.direction == "UP" else 1)
        new_index = index + (-1 if self.direction == "UP" else 1)

        idx_min = 0
        idx_max = len(collection_property) - 1 if collection_property else 0

        collection_property.move(neighbor, index)
        setattr(properties, self.idx_property, int(clamp(new_index, idx_min, idx_max)))
        return {"FINISHED"}