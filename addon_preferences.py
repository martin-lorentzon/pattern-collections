from bpy.types import AddonPreferences
from bpy.props import FloatProperty, BoolProperty

class PATTERN_COLLECTIONS_Preferences(AddonPreferences):
    bl_idname = __package__
    
    sorting_interval: FloatProperty(
        name="Automatic Sorting Interval",
        description = "Number of seconds between each automatic sort",
        min=0.1,
        default=1,
        subtype="TIME_ABSOLUTE"
    )
    safe_intervals: BoolProperty(
        name="Safe Automatic Sorting",
        description="Base the automatic sorting interval on the previous sort delta to ensure Blender doesn't lock as frequently (multiplies by 10)",
        default=True
    )
    
    def draw(self, context):
        layout = self.layout

        layout.separator(factor=0.1)

        row = layout.row()
        row.alignment = "LEFT"
        row.label(text="", icon="TIME")
        row.prop(self, "sorting_interval", text="")
        row.label(text="Automatic Sorting Interval")

        row = layout.row()
        row.alignment = "LEFT"
        row.label(text="", icon="FAKE_USER_ON")
        row.prop(self, "safe_intervals")

        layout.separator(factor=0.1)