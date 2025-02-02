import bpy
import bmesh


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def all_parents(obj):
    parent = obj.parent
    parent_list = []
    while parent:
        parent_list.append(parent)
        parent = parent.parent
    return parent_list


def triangle_count(obj):
    if isinstance(bpy.types.Object) and obj.type == "MESH":
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bmesh.ops.triangulate(bm, faces=bm.faces[:])
        triagles = len(bm.faces)
        bm.free()
        return triagles
    else:
        return 0


def volume(obj):
    if isinstance(bpy.types.Object) and obj.type == "MESH":
        return obj.dimensions.x * obj.dimensions.y * obj.dimensions.z
    else:
        return 0


def surface_area(obj):
    if isinstance(bpy.types.Object) and obj.type == "MESH":
        bm = bmesh.new()
        bm.from_mesh(obj.data)

        for v in bm.verts:
            v.co = obj.matrix_world @ v.co  # Reverse world matrix

        surface_area = sum(f.calc_area() for f in bm.faces)
        bm.free()
        return surface_area
    else:
        return 0


def redraw_ui():
    for area in bpy.context.screen.areas:
        area.tag_redraw()