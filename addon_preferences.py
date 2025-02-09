import bpy
from bpy.types import AddonPreferences
from bpy.props import FloatProperty, BoolProperty, StringProperty
from . import icons


class PATTERN_COLLECTIONS_Preferences(AddonPreferences):
    bl_idname = __package__

    sorting_interval: FloatProperty(
        name="Automatic Sorting Interval",
        description="Time between each automatic sort",
        min=0.1,
        default=1,
        subtype="TIME_ABSOLUTE"
    )
    safe_intervals: BoolProperty(
        name="Safe Automatic Sorting",
        description="Adjusts the sorting interval based on the previous sort duration to prevent Blender freezing indefinitely (multiplies by 10)",
        default=True
    )
    filename_suffix: StringProperty(
        name="Filename Suffix",
        description="Suffix at the end of exported JSON files",
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

        def draw_filename_prefs(layout: bpy.types.UILayout):
            split = layout.split(factor=0.5)
            split.label(text="Filename Suffix", icon="FILE")
            split.prop(self, "filename_suffix", text="")

            split = layout.split(factor=0.5)
            split.label(text="Lowercase Filenames", icon_value=pcoll["CASE_SENSITIVITY_OFF"].icon_id)
            split.prop(self, "lowercase_filename", text="")

        def draw_automatic_sorting_prefs(layout: bpy.types.UILayout):
            split = layout.split(factor=0.5)
            split.label(text="Automatic Sorting Interval", icon="TIME")
            split.prop(self, "sorting_interval", text="")

            split = layout.split(factor=0.5)
            split.label(text="Safe Automatic Sorting", icon="FAKE_USER_ON")
            split.prop(self, "safe_intervals", text="")

        if bpy.app.version >= (4, 1, 0):
            header, panel = layout.panel("filenames_panel", default_closed=True)
            header.label(text="Filenames")
            if panel:
                draw_filename_prefs(panel)

            header, panel = layout.panel("automatic_sorting_panel", default_closed=True)
            header.label(text="Automatic Sorting")
            if panel:
                draw_automatic_sorting_prefs(panel)
        else:
            draw_filename_prefs(panel)
            draw_automatic_sorting_prefs(panel)
