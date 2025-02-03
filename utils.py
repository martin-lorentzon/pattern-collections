import bpy
import bmesh


def redraw_ui():
    for area in bpy.context.screen.areas:
        area.tag_redraw()


def all_parents(ob):
    parent = ob.parent
    parent_list = []
    while parent:
        parent_list.append(parent)
        parent = parent.parent
    return parent_list


def triangle_count(ob):
    if isinstance(ob, bpy.types.Object) and ob.type == "MESH":
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        bmesh.ops.triangulate(bm, faces=bm.faces[:])
        triagles = len(bm.faces)
        bm.free()
        return triagles
    else:
        return 0


def volume(ob):
    if isinstance(ob, bpy.types.Object) and ob.type == "MESH":
        return ob.dimensions.x * ob.dimensions.y * ob.dimensions.z
    else:
        return 0


def surface_area(ob):
    if isinstance(ob, bpy.types.Object) and ob.type == "MESH":
        bm = bmesh.new()
        bm.from_mesh(ob.data)

        for v in bm.verts:
            v.co = ob.matrix_world @ v.co  # Reverse world matrix

        surface_area = sum(f.calc_area() for f in bm.faces)
        bm.free()
        return surface_area
    else:
        return 0
