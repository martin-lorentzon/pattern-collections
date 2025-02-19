import bpy
from bpy.types import Operator, CollectionProperty
from bpy.props import StringProperty
from bpy_extras.io_utils import ExportHelper, ImportHelper
from . import sorting_functions
from . import utils
import functools
import time
import json
import webbrowser


def sort_collection(context, collection):
    t0 = time.perf_counter()
    sorting_commands = sorting_functions.sort_objects(collection, context.scene.objects)
    sorting_functions.process_sorting_commands(sorting_commands)
    t1 = time.perf_counter()
    return t1 - t0


class PATTERN_COLLECTIONS_OT_sort(Operator):
    bl_idname = "scene.pattern_collection_sort"
    bl_label = "Sort Collection"
    bl_description = "Sort all objects for the active collection"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        collection = context.collection
        delta_t = sort_collection(context, collection)
        self.report({"INFO"}, f"Finished sorting in {delta_t:.4f} sec")
        return {"FINISHED"}


class PATTERN_COLLECTIONS_OT_register_timer(Operator):
    bl_idname = "scene.pattern_collection_register_timer"
    bl_label = "Enable Automatic Sorting"
    bl_description = "Sort all objects for the active collection at regular intervals\n(WARNING: May cause Blender to momentarily freeze for larger scenes)"

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__package__].preferences
        collection = context.collection

        if collection.name in sorting_functions.sorting_timers:
            self.report({"WARNING"}, f"Automatic sorting is already enabled for collection {collection.name}")
            return {"CANCELLED"}

        if addon_prefs.safe_intervals:
            def timer_func(collection_name, interval_seconds):
                delta_t = sort_collection(bpy.context, bpy.data.collections[collection_name])
                print(f"Finished sorting in {delta_t:.4f} sec")
                return max(interval_seconds, delta_t * 10)
        else:
            def timer_func(collection_name, interval_seconds):
                delta_t = sort_collection(bpy.context, bpy.data.collections[collection_name])
                print(f"Finished sorting in {delta_t:.4f} sec")
                return (interval_seconds)

        partial = functools.partial(timer_func, collection.name, addon_prefs.sorting_interval)
        bpy.app.timers.register(partial, first_interval=addon_prefs.sorting_interval)
        sorting_functions.sorting_timers[collection.name] = partial

        utils.redraw_ui()
        return {"FINISHED"}


class PATTERN_COLLECTIONS_OT_unregister_timer(Operator):
    bl_idname = "scene.pattern_collection_unregister_timer"
    bl_label = "Disable Automatic Sorting"
    bl_description = "Sort all objects for the active collection at regular intervals\n(WARNING: May cause Blender to momentarily freeze for larger scenes)"

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
    bl_idname = "scene.pattern_collection_export"
    bl_label = "Export Pattern"
    bl_description = "Export sorting pattern to a JSON file"

    filter_glob: StringProperty(default="*.json;", options={"HIDDEN"})
    filename_ext = ".json"

    def execute(self, context):
        collection = context.collection
        properties = collection.pattern_collection_properties

        if not self.filepath.endswith(".json"):
            self.report({"WARNING"}, "Unsupported format")
            return {"CANCELLED"}

        categories = [
            "included_names",       "excluded_names",
            "included_hierarchies", "excluded_hierarchies",
            "included_types",       "excluded_types",
            "included_materials",   "excluded_materials",
            "included_collections", "excluded_collections",
            "included_uv_layers",   "excluded_uv_layers",
            "included_attributes",  "excluded_attributes"
        ]

        categories_data = dict()

        for category_name in categories:
            category: CollectionProperty = getattr(properties, category_name)

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
    bl_idname = "scene.pattern_collection_import"
    bl_label = "Import Pattern"
    bl_description = "Import sorting pattern from a JSON file"
    bl_options = {"REGISTER", "UNDO"}

    filter_glob: StringProperty(default="*.json;", options={"HIDDEN"})

    def execute(self, context):
        collection = context.collection
        properties = collection.pattern_collection_properties

        if not self.filepath.endswith(".json"):
            self.report({"WARNING"}, "Unsupported format")
            return {"CANCELLED"}

        sorting_categories = [
            "included_names",       "excluded_names",
            "included_hierarchies", "excluded_hierarchies",
            "included_types",       "excluded_types",
            "included_materials",   "excluded_materials",
            "included_collections", "excluded_collections",
            "included_uv_layers",   "excluded_uv_layers",
            "included_attributes",  "excluded_attributes"
        ]

        with open(bpy.path.abspath(self.filepath), "r") as data:
            categories_data = json.load(data)

        for category_name in sorting_categories:
            category: CollectionProperty = getattr(properties, category_name)

            category.clear()

            for data in categories_data.get(category_name, []):
                item = category.add()

                for prop, value in data.items():
                    setattr(item, prop, value)
        return {"FINISHED"}


class PATTERN_COLLECTIONS_OT_open_preferences(Operator):
    bl_idname = "pattern_collections.open_preferences"
    bl_description = "Open the add-on preferences"
    bl_label = "Preferences"

    def execute(self, context):
        bpy.ops.screen.userpref_show("INVOKE_DEFAULT")
        bpy.data.window_managers["WinMan"].addon_search = "Pattern Collections"
        bpy.context.preferences.active_section = "ADDONS"
        bpy.data.window_managers["WinMan"].addon_support = {
            "OFFICIAL", "COMMUNITY"
        }
        return {"FINISHED"}


class PATTERN_COLLECTIONS_OT_open_tracker(Operator):
    bl_idname = "pattern_collections.open_tracker"
    bl_description = "Open the issue tracker"
    bl_label = "Feedback"

    def execute(self, context):
        url = "https://github.com/martin-lorentzon/pattern-collections/issues"
        webbrowser.open(url)
        return {"FINISHED"}


class PATTERN_COLLECTIONS_OT_open_documentation(Operator):
    bl_idname = "pattern_collections.open_documentation"
    bl_label = "Documentation"
    bl_description = "Open the documentation"

    def execute(self, context):
        url = "https://github.com/martin-lorentzon/pattern-collections?#pattern-based-collections-for-blender"
        webbrowser.open(url)
        return {"FINISHED"}
