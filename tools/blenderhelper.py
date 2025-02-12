import bpy
from mathutils import Vector


def create_brush(name):
    bpy.data.brushes.new(name=name, mode="VERTEX_PAINT")
    return bpy.data.brushes[name]


def apply_brush_settings(brush, idx):
    if idx < 5:
        brush.blend = "MIX"
    if idx == 1:
        brush.color = (0, 0, 0)
    elif idx == 2:
        brush.color = (0, 0, 1)
    elif idx == 3:
        brush.color = (0, 1, 0)
    elif idx == 4:
        brush.color = (0, 1, 1)
    elif idx == 5:
        alpha = bpy.context.scene.vert_paint_alpha
        if alpha > 0:
            brush.color = (1, 1, 1)
            brush.blend = "ADD_ALPHA"
            brush.strength = alpha
        else:
            brush.color = (0, 0, 0)
            brush.blend = "ERASE_ALPHA"
            brush.strength = alpha * -1
    return brush


def get_terrain_texture_brush(idx):
    name = "TerrainBrush"

    try:
        brush = bpy.data.brushes[name]
    except:
        brush = create_brush(name)
    apply_brush_settings(brush, idx)
    return brush


def copy_children(res, children):
    for child in children:
        resc = child.copy()
        bpy.context.collection.objects.link(resc)
        resc.parent = res
        if len(child.children) > 0:
            copy_children(res, child.children)


def copy_object(obj, children=False):
    if children:
        res = obj.copy()
        bpy.context.collection.objects.link(res)
        copy_children(res, obj.children)
        return res
    else:
        return obj.copy()


def split_object(obj, parent):
    objs = []
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.separate(type='MATERIAL')
    bpy.ops.object.mode_set(mode='OBJECT')
    for child in parent.children:
        objs.append(child)
    return objs


def join_objects(objs):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = objs[0]
    for obj in objs:
        obj.select_set(True)
    bpy.ops.object.join()
    bpy.ops.object.select_all(action='DESELECT')
    return

# MIT License

# Copyright (c) 2017 GiveMeAllYourCats

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Code author: GiveMeAllYourCats
# Repo: https://github.com/michaeldegroot/cats-blender-plugin
# Edits by: GiveMeAllYourCats, Hotox


def remove_unused_vertex_groups_of_mesh(mesh):
    remove_count = 0
    mesh.update_from_editmode()

    vgroup_used = {i: False for i, k in enumerate(mesh.vertex_groups)}

    for v in mesh.data.vertices:
        for g in v.groups:
            if g.weight > 0.0:
                vgroup_used[g.group] = True

    for i, used in sorted(vgroup_used.items(), reverse=True):
        if not used:
            mesh.vertex_groups.remove(mesh.vertex_groups[i])
            remove_count += 1
    return remove_count


def get_selected_vertices(obj):
    mode = obj.mode
    if obj.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    # We need to switch from Edit mode to Object mode so the vertex selection gets updated (disgusting!)
    verts = [obj.matrix_world @ Vector((v.co.x, v.co.y, v.co.z))
             for v in obj.data.vertices if v.select]
    bpy.ops.object.mode_set(mode=mode)
    return verts


def build_tag_bone_map(armature):
    if (armature == None):
        return None

    if (armature.pose == None):
        return None

    tag_bone_map = {}
    for pose_bone in armature.pose.bones:
        tag_bone_map[pose_bone.bone.bone_properties.tag] = pose_bone.name

    return tag_bone_map
