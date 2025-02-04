from bpy.types import AddonPreferences
from bpy.props import FloatProperty, BoolProperty, StringProperty
from . import icons

class PATTERN_COLLECTIONS_Preferences(AddonPreferences):
    bl_idname = __package__
    
    sorting_interval: FloatProperty(
        name="Automatic Sorting Interval",
        description = "Time between each automatic sort",
        min=0.1,
        default=1,
        subtype="TIME_ABSOLUTE"
    )
    safe_intervals: BoolProperty(
        name="Safe Automatic Sorting",
        description="Adjusts the sorting interval based on the previous sort duration to prevent Blender freezing (multiplies by 10)",
        default=True
    )
    filename_suffix: StringProperty(
        name="Filename Suffix",
        description="Suffix at the end of JSON files",
        default="_col_pattern"
    )
    lowercase_filename: BoolProperty(
        name="Lowercase Filenames",
        description="Turn filenames lowercase",
        default=True
    )
    
    def draw(self, context):
        layout = self.layout
        pcoll = icons.preview_collections["main"]

        row = layout.row()
        row.alignment = "LEFT"
        row.label(text="", icon="FILE")
        row.prop(self, "filename_suffix", text="")
        row.label(text="Filename Suffix")

        row = layout.row()
        row.alignment = "LEFT"
        icon = pcoll["CASE_SENSITIVITY_OFF"] if self.lowercase_filename else pcoll["CASE_SENSITIVITY_ON"]
        row.label(text="", icon_value=icon.icon_id)
        row.prop(self, "lowercase_filename")

        row = layout.row()
        row.alignment = "LEFT"
        row.label(text="", icon="TIME")
        row.prop(self, "sorting_interval", text="")
        row.label(text="Automatic Sorting Interval")

        row = layout.row()
        row.alignment = "LEFT"
        row.label(text="", icon="FAKE_USER_ON")
        row.prop(self, "safe_intervals")
