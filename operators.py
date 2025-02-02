import bpy
from bpy_extras.io_utils import ExportHelper, ImportHelper
from . import sorting_functions
from . import utils
import functools
import time
import json


class PATTERN_COLLECTION_OT_sort_collection(bpy.types.Operator):
    bl_idname = "pattern_collection.sort_collection"
    bl_label = "Sort Collection"
    bl_description = "Sort all objects for the active collection"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        collection = context.collection
        sorting_commands = sorting_functions.sort_objects(collection, bpy.data.objects)

        sorting_functions.process_sorting_commands(sorting_commands)
        return {"FINISHED"}


class PATTERN_COLLECTION_OT_register_timer(bpy.types.Operator):
    bl_idname = "pattern_collection.register_timer"
    bl_label = "Register Sort Timer"
    bl_description = "Sort all objects for the active collection at regular intervals\n(WARNING: May cause Blender to momentarily hang for larger scenes)"

    interval_seconds: bpy.props.FloatProperty(
        name="Interval Seconds",
        default=1.0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        collection = context.collection

        if collection.name in sorting_functions.sorting_timers:
            self.report({"WARNING"}, "Cannot register timer for collection with auto-sort already enabled")
            return {"CANCELLED"}

        def timer_func(interval_seconds, collection_name):
            start_time = time.time()  # Timing the function to prevent it from completely freeze or crash Blender
            collection = bpy.data.collections[collection_name]
            sorting_commands = sorting_functions.sort_objects(collection, bpy.data.objects)

            sorting_functions.process_sorting_commands(sorting_commands)

            execution_time = time.time() - start_time
            return max(interval_seconds, execution_time * 10)

        partial = functools.partial(timer_func, self.interval_seconds, collection.name)

        bpy.app.timers.register(partial, first_interval=self.interval_seconds)
        sorting_functions.sorting_timers[collection.name] = partial

        utils.redraw_ui()
        return {"FINISHED"}


class PATTERN_COLLECTION_OT_unregister_timer(bpy.types.Operator):
    bl_idname = "pattern_collection.unregister_timer"
    bl_label = "Unregister Sort Timer"
    bl_description = "Sort all objects for the active collection at regular intervals\n(WARNING: May cause Blender to momentarily hang for larger scenes)"

    def execute(self, context):
        collection = context.collection
        if collection.name not in sorting_functions.sorting_timers:
            self.report({"WARNING"}, "Cannot unregister timer for collection with auto-sort already disabled")
            return {"CANCELLED"}

        bpy.app.timers.unregister(sorting_functions.sorting_timers[collection.name])
        sorting_functions.sorting_timers.pop(collection.name)

        utils.redraw_ui()
        return {"FINISHED"}


class PATTERN_COLLECTION_OT_export_json(bpy.types.Operator, ExportHelper):
    bl_idname = "pattern_collection.export_json"
    bl_label = "Export JSON"
    bl_description = "Exports a pattern collection config to a JSON file"

    filter_glob: bpy.props.StringProperty(default="*.json;", options={"HIDDEN"})
    filename_ext = ".json"

    def execute(self, context):  # TODO: Clean up this mess
        collection = context.collection
        properties = collection.pattern_collection_properties
        filepath = self.filepath

        write_dict = dict()

        categories = ["included_names",       "excluded_names",
                      "included_hierarchies", "excluded_hierarchies",
                      "included_types",       "excluded_types",
                      "included_materials",   "excluded_materials",
                      "included_collections", "excluded_collections",
                      "included_uv_layers",   "excluded_uv_layers",
                      "included_attributes",  "excluded_attributes"]

        # item_properties = ["name", "anchor", "case_sensitive", "enable", "value"]

        for category in categories:
            category = getattr(properties, category)

            if category is None:
                continue

            write_dict.setdefault(category, [])

            for item in category:  # item -> property group | category -> collection property
                # write_item = {prop: getattr(item, prop) for prop in desired_properties if hasattr(item, prop)}  # <- Works, but requires a list of keys

                # write_item = {prop: getattr(item, prop) for prop in item.keys()}  # <- Can only read properties that have been set by the user
                # (not intended behavior)

                write_item = {prop.identifier: getattr(item, prop.identifier)  # <- Accomplishes the intention of the dict comprehension above
                              # (why is bl_rna superior in this scenario?)
                              for prop in item.bl_rna.properties
                              if not prop.is_readonly}

                write_dict[category].append(write_item)

        with open(bpy.path.abspath(filepath), "w") as data:
            json.dump(write_dict, data, indent=4)
        return {"FINISHED"}


class PATTERN_COLLECTION_OT_import_json(bpy.types.Operator, ImportHelper):
    bl_idname = "pattern_collection.import_json"
    bl_label = "Import JSON"
    bl_description = "Loads a pattern collection config from a JSON file"
    bl_options = {"REGISTER", "UNDO"}

    filter_glob: bpy.props.StringProperty(
        default="*.json;", options={"HIDDEN"})

    def execute(self, context):
        collection = context.collection
        properties = collection.pattern_collection_properties
        filepath = self.filepath

        with open(bpy.path.abspath(filepath), "r") as data:
            properties_dict = json.load(data)

        sorting_categories = ["included_names",       "excluded_names",
                              "included_hierarchies", "excluded_hierarchies",
                              "included_types",       "excluded_types",
                              "included_materials",   "excluded_materials",
                              "included_collections", "excluded_collections",
                              "included_uv_layers",   "excluded_uv_layers",
                              "included_attributes",  "excluded_attributes"]

        for category in sorting_categories:
            collection_property = getattr(properties, category, None)

            if collection_property is None:
                continue

            collection_property.clear()

            for data in properties_dict.get(category, []):
                item = collection_property.add()

                for prop, value in data.items():
                    setattr(item, prop, value)
        return {"FINISHED"}
