import bpy
from bpy.types import Operator
from bpy.props import StringProperty
from bpy_extras.io_utils import ExportHelper, ImportHelper
from . import sorting_functions
from . import utils
import functools
import time
import json


def sort_collection(collection):
    t0 = time.perf_counter()
    sorting_commands = sorting_functions.sort_objects(collection, bpy.data.objects)
    sorting_functions.process_sorting_commands(sorting_commands)
    t1 = time.perf_counter()
    return t1 - t0


class PATTERN_COLLECTIONS_OT_sort_collection(Operator):
    bl_idname = "collection.sort_collection"
    bl_label = "Sort Collection"
    bl_description = "Sort all objects for the active collection"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        collection = context.collection
        delta_t = sort_collection(collection)
        self.report({"INFO"}, f"Finished sorting {delta_t:.4f} in sec")
        return {"FINISHED"}


class PATTERN_COLLECTIONS_OT_register_timer(Operator):
    bl_idname = "collection.register_pattern_sort_timer"
    bl_label = "Enable Automatic Sorting"
    bl_description = "Sort all objects for the active collection at regular intervals\n(WARNING: May cause Blender to momentarily hang for larger scenes)"

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__package__].preferences
        collection = context.collection

        if collection.name in sorting_functions.sorting_timers:
            self.report({"WARNING"}, f"Automatic sorting is already enabled for collection {collection.name}")
            return {"CANCELLED"}

        if addon_prefs.safe_intervals:
            def timer_func(collection_name, interval_seconds):
                delta_t = sort_collection(bpy.data.collections[collection_name])
                print(f"Finished sorting {delta_t:.4f} in sec")
                return max(interval_seconds, delta_t * 10)
        else:
            def timer_func(collection_name, interval_seconds):
                delta_t = sort_collection(bpy.data.collections[collection_name])
                print(f"Finished sorting {delta_t:.4f} in sec")
                return (interval_seconds)

        partial = functools.partial(timer_func, collection.name, addon_prefs.sorting_interval)

        bpy.app.timers.register(partial, addon_prefs.sorting_interval)
        sorting_functions.sorting_timers[collection.name] = partial

        utils.redraw_ui()
        return {"FINISHED"}


class PATTERN_COLLECTIONS_OT_unregister_timer(Operator):
    bl_idname = "collection.unregister_pattern_sort_timer"
    bl_label = "Disable Automatic Sorting"
    bl_description = "Sort all objects for the active collection at regular intervals\n(WARNING: May cause Blender to momentarily hang for larger scenes)"

    def execute(self, context):
        collection = context.collection

        if collection.name not in sorting_functions.sorting_timers:
            self.report({"WARNING"}, f"Automatic sorting is already disabled for collection {collection.name}")
            return {"CANCELLED"}

        bpy.app.timers.unregister(sorting_functions.sorting_timers[collection.name])
        sorting_functions.sorting_timers.pop(collection.name)

        utils.redraw_ui()
        return {"FINISHED"}


class PATTERN_COLLECTIONS_OT_export_pattern(Operator, ExportHelper):
    bl_idname = "collection.export_pattern"
    bl_label = "Export Pattern"
    bl_description = "Exports a pattern collection config to a JSON file"

    filter_glob: StringProperty(default="*.json;", options={"HIDDEN"})
    filename_ext = ".json"

    def execute(self, context):
        collection = context.collection
        properties = collection.pattern_collection_properties

        categories = ["included_names",       "excluded_names",
                      "included_hierarchies", "excluded_hierarchies",
                      "included_types",       "excluded_types",
                      "included_materials",   "excluded_materials",
                      "included_collections", "excluded_collections",
                      "included_uv_layers",   "excluded_uv_layers",
                      "included_attributes",  "excluded_attributes"]

        categories_data = dict()

        for category_name in categories:
            category = getattr(properties, category_name, None)

            if category is None:
                continue

            categories_data.setdefault(category_name, [])

            for item in category:
                item_data = {
                    p.identifier: getattr(item, p.identifier) 
                    for p in item.bl_rna.properties if not p.is_readonly
                }
                categories_data[category_name].append(item_data)

        with open(bpy.path.abspath(self.filepath), "w") as data:
            json.dump(categories_data, data, indent=4)
        return {"FINISHED"}


class PATTERN_COLLECTIONS_OT_import_pattern(Operator, ImportHelper):
    bl_idname = "collection.import_pattern"
    bl_label = "Import Pattern"
    bl_description = "Loads a pattern collection config from a JSON file"
    bl_options = {"REGISTER", "UNDO"}

    filter_glob: StringProperty(
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
