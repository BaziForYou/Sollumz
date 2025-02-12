import os
import shutil
import collections
import bmesh
import bpy
from ..resources.drawable import *
from ..resources.shader import ShaderManager
from ..tools.meshhelper import *
from ..tools.utils import *
from ..tools.blenderhelper import *
from ..sollumz_properties import BOUND_TYPES, SOLLUMZ_UI_NAMES, LightType, MaterialType, LODLevel, SollumType
from ..ybn.ybnexport import bound_from_object, composite_from_object


def get_used_materials(obj):

    materials = []

    for child in obj.children:
        for grandchild in child.children:
            if(grandchild.sollum_type == SollumType.DRAWABLE_GEOMETRY):
                mats = grandchild.data.materials
                for mat in mats:
                    if(mat.sollum_type == MaterialType.SHADER):
                        materials.append(mat)

    return materials


def get_shaders_from_blender(obj):
    shaders = []

    materials = get_used_materials(obj)

    for material in materials:
        shader = ShaderItem()
        # Maybe make this a property?
        shader.name = material.shader_properties.name
        shader.filename = material.shader_properties.filename
        shader.render_bucket = material.shader_properties.renderbucket

        for node in material.node_tree.nodes:
            if isinstance(node, bpy.types.ShaderNodeTexImage):
                param = TextureShaderParameter()
                param.name = node.name
                param.type = "Texture"
                if node.image == None:
                    param.texture_name = "givemechecker"
                else:
                    param.texture_name = node.image.name.split('.')[0]
                shader.parameters.append(param)
            elif isinstance(node, bpy.types.ShaderNodeValue):
                if node.name[-1] == "x":
                    param = VectorShaderParameter()
                    param.name = node.name[:-2]
                    param.type = "Vector"

                    x = node
                    y = material.node_tree.nodes[node.name[:-1] + "y"]
                    z = material.node_tree.nodes[node.name[:-1] + "z"]
                    w = material.node_tree.nodes[node.name[:-1] + "w"]

                    param.x = x.outputs[0].default_value
                    param.y = y.outputs[0].default_value
                    param.z = z.outputs[0].default_value
                    param.w = w.outputs[0].default_value

                    shader.parameters.append(param)

        shaders.append(shader)

    return shaders


def texture_item_from_node(n):
    texture_item = TextureItem()
    if n.image:
        texture_item.name = n.image.name.split('.')[0]
        texture_item.width = n.image.size[0]
        texture_item.height = n.image.size[1]
    else:
        texture_item.name = "none"
        texture_item.width = 0
        texture_item.height = 0

    texture_item.usage = SOLLUMZ_UI_NAMES[n.texture_properties.usage]
    texture_item.extra_flags = n.texture_properties.extra_flags
    texture_item.format = SOLLUMZ_UI_NAMES[n.texture_properties.format]
    texture_item.miplevels = 0
    texture_item.filename = texture_item.name + ".dds"
    # texture_item.unk32 = 0
    for prop in dir(n.texture_flags):
        value = getattr(n.texture_flags, prop)
        if value == True:
            texture_item.usage_flags.append(prop.upper())

    return texture_item


def texture_dictionary_from_materials(obj, exportpath):
    texture_dictionary = []
    messages = []

    has_td = False

    t_names = []
    for mat in get_used_materials(obj):
        nodes = mat.node_tree.nodes
        for n in nodes:
            if(isinstance(n, bpy.types.ShaderNodeTexImage)):
                if(n.texture_properties.embedded == True):
                    has_td = True
                    texture_item = texture_item_from_node(n)
                    if texture_item.name in t_names:
                        continue
                    else:
                        t_names.append(texture_item.name)
                    texture_dictionary.append(texture_item)

                    if n.image:
                        foldername = obj.name
                        folderpath = os.path.join(exportpath, foldername)
                        txtpath = bpy.path.abspath(n.image.filepath)
                        if os.path.isfile(txtpath):
                            if(os.path.isdir(folderpath) == False):
                                os.mkdir(folderpath)
                            dstpath = folderpath + "\\" + \
                                os.path.basename(txtpath)
                            # check if paths are the same because if they are no need to copy
                            if txtpath != dstpath:
                                shutil.copyfile(txtpath, dstpath)
                        else:
                            messages.append(
                                f"Missing Embedded Texture: {txtpath} please supply texture! The texture will not be copied to the texture folder until entered!")
                    else:
                        messages.append(
                            f"Material: {mat.name} is missing the {n.name} texture and will not be exported.")

    if(has_td):
        return texture_dictionary, messages
    else:
        return None, []


def get_blended_verts(mesh, vertex_groups, bones=None):
    bone_index_map = {}
    if(bones != None):
        for i in range(len(bones)):
            bone_index_map[bones[i].name] = i

    blend_weights = []
    blend_indices = []
    for v in mesh.vertices:
        if len(v.groups) > 0:
            bw = [0] * 4
            bi = [0] * 4
            valid_weights = 0
            total_weights = 0
            max_weights = 0
            max_weights_index = -1

            for element in v.groups:
                if element.group >= len(vertex_groups):
                    continue

                vertex_group = vertex_groups[element.group]
                bone_index = bone_index_map.get(vertex_group.name, -1)
                # 1/255 = 0.0039 the minimal weight for one vertex group
                weight = round(element.weight * 255)
                if (vertex_group.lock_weight == False and bone_index != -1 and weight > 0 and valid_weights < 4):
                    bw[valid_weights] = weight
                    bi[valid_weights] = bone_index
                    if (max_weights < weight):
                        max_weights_index = valid_weights
                        max_weights = weight
                    valid_weights += 1
                    total_weights += weight

            # weights normalization
            if valid_weights > 0 and max_weights_index != -1:
                bw[max_weights_index] = bw[max_weights_index] + \
                    (255 - total_weights)

            blend_weights.append(bw)
            blend_indices.append(bi)
        else:
            blend_weights.append([0, 0, 0, 0])
            blend_indices.append([0, 0, 0, 0])

    return blend_weights, blend_indices


def get_mesh_buffers(obj, mesh, vertex_type, bones=None, export_settings=None):
    # thanks dexy

    blend_weights, blend_indices = get_blended_verts(
        mesh, obj.vertex_groups, bones)

    vertices = {}
    indices = []

    for tri in mesh.loop_triangles:
        for loop_idx in tri.loops:
            loop = mesh.loops[loop_idx]
            vert_idx = loop.vertex_index
            mesh_layer_idx = 0

            kwargs = {}

            if "position" in vertex_type._fields:
                if mesh.vertices[vert_idx]:
                    if export_settings.use_transforms:
                        pos = float32_list(
                            obj.matrix_world @ mesh.vertices[vert_idx].co)
                    else:
                        pos = float32_list(
                            obj.matrix_basis @ mesh.vertices[vert_idx].co)
                    kwargs['position'] = tuple(pos)
                else:
                    kwargs["position"] = tuple([0, 0, 0])
            if "normal" in vertex_type._fields:
                if loop.normal:
                    normal = float32_list(loop.normal)
                    kwargs["normal"] = tuple(normal)
                else:
                    kwargs["normal"] = tuple([0, 0, 0])
            if "blendweights" in vertex_type._fields:
                kwargs['blendweights'] = tuple(blend_weights[vert_idx])
            if "blendindices" in vertex_type._fields:
                kwargs['blendindices'] = tuple(blend_indices[vert_idx])
            if "tangent" in vertex_type._fields:
                if loop.tangent:
                    tangent = float32_list(loop.tangent.to_4d())
                    tangent[3] = loop.bitangent_sign  # convert to float 32 ?
                    kwargs["tangent"] = tuple(tangent)
                else:
                    kwargs["tangent"] = tuple([0, 0, 0, 0])
            for i in range(6):
                if f"texcoord{i}" in vertex_type._fields:
                    key = f'texcoord{i}'
                    if mesh_layer_idx < len(mesh.uv_layers):
                        data = mesh.uv_layers[mesh_layer_idx].data
                        uv = float32_list(
                            flip_uv(data[loop_idx].uv))
                        kwargs[key] = tuple(uv)
                        mesh_layer_idx += 1
                    else:
                        kwargs[key] = (0, 0)
            for i in range(2):
                if f"colour{i}" in vertex_type._fields:
                    key = f'colour{i}'
                    if i < len(mesh.vertex_colors):
                        data = mesh.vertex_colors[i].data
                        kwargs[key] = tuple(
                            int(val * 255) for val in data[loop_idx].color)
                    else:
                        kwargs[key] = (0, 0, 0, 0)

            vertex = vertex_type(**kwargs)

            if vertex in vertices:
                idx = vertices[vertex]
            else:
                idx = len(vertices)
                vertices[vertex] = idx

            indices.append(idx)

    return vertices.keys(), indices


def get_semantic_from_object(shader, mesh):

    sematic = []

    # always has a position
    sematic.append(VertexSemantic.position)
    # add blend weights and blend indicies
    # maybe pass is_skinned param in this function and check there ?
    is_skinned = False
    for v in mesh.vertices:
        if len(v.groups) > 0:
            is_skinned = True
            break
    if is_skinned:
        sematic.append(VertexSemantic.blend_weight)
        sematic.append(VertexSemantic.blend_index)
    # add normal
    # dont know what to check so always add for now??
    sematic.append(VertexSemantic.normal)
    # add colors
    vcs = len(mesh.vertex_colors)
    if vcs > 0:
        for vc in mesh.vertex_colors:
            if vc.name != "TintColor":
                sematic.append(VertexSemantic.color)
    # add texcoords
    tcs = len(mesh.uv_layers)
    if tcs > 0:
        if tcs > 8:  # or tcs == 0: add this restriction?? although some vertexs buffers may not have uv data???
            raise Exception(f"To many uv layers or none on mesh: {mesh.name}")
        for i in range(tcs):
            sematic.append(VertexSemantic.texcoord)
    # add tangents
    if shader.required_tangent:
        sematic.append(VertexSemantic.tangent)

    return "".join(sematic)


def apply_and_triangulate_object(obj):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    obj_eval = obj.evaluated_get(depsgraph)
    mesh = bpy.data.meshes.new_from_object(
        obj_eval, preserve_all_data_layers=True, depsgraph=depsgraph)
    tempmesh = bmesh.new()
    tempmesh.from_mesh(mesh)
    bmesh.ops.triangulate(tempmesh, faces=tempmesh.faces)
    tempmesh.to_mesh(mesh)
    tempmesh.free()
    mesh.calc_tangents()
    mesh.calc_loop_triangles()
    return obj_eval, mesh


def get_shader_index(mats, mat):
    for i in range(len(mats)):
        if mats[i].as_pointer() == mat.as_pointer():
            return i


def geometry_from_object(obj, mats, bones=None, export_settings=None):
    geometry = GeometryItem()

    geometry.shader_index = get_shader_index(mats, obj.active_material)

    obj, mesh = apply_and_triangulate_object(obj)

    bbmin, bbmax = get_bound_extents(obj, world=export_settings.use_transforms)
    geometry.bounding_box_min = bbmin
    geometry.bounding_box_max = bbmax

    shader_name = obj.active_material.shader_properties.name
    shader = ShaderManager.shaders[shader_name]

    layout = shader.get_layout_from_semantic(
        get_semantic_from_object(shader, mesh))

    geometry.vertex_buffer.layout = layout.value
    vertex_buffer, index_buffer = get_mesh_buffers(
        obj, mesh, layout.vertex_type, bones, export_settings)

    geometry.vertex_buffer.data = vertex_buffer
    geometry.index_buffer.data = index_buffer

    return geometry


def drawable_model_from_object(obj, bones=None, export_settings=None):
    drawable_model = DrawableModelItem()

    drawable_model.render_mask = obj.drawable_model_properties.render_mask
    drawable_model.flags = obj.drawable_model_properties.flags

    # rawable_model.bone_index = 0
    if bones is not None:
        drawable_model.has_skin = 1
        drawable_model.unknown_1 = len(bones)

    for child in obj.children:
        if child.sollum_type == SollumType.DRAWABLE_GEOMETRY:
            if len(child.data.materials) > 1:
                # Preserve original order of materials
                mats = child.data.copy().materials
                objs = split_object(child, obj)
                for obj in objs:
                    geometry = geometry_from_object(
                        obj, mats, bones, export_settings)  # MAYBE WRONG ASK LOYALIST
                    drawable_model.geometries.append(geometry)
                join_objects(objs)
            else:
                geometry = geometry_from_object(
                    child, get_used_materials(obj.parent), bones, export_settings)
                drawable_model.geometries.append(geometry)

    return drawable_model


def bone_from_object(obj):

    bone = BoneItem()
    bone.name = obj.name
    bone.tag = obj.bone_properties.tag
    bone.index = obj["BONE_INDEX"]

    if obj.parent != None:
        bone.parent_index = obj.parent["BONE_INDEX"]
        children = obj.parent.children
        sibling = -1
        if len(children) > 1:
            for i, child in enumerate(children):
                if child["BONE_INDEX"] == obj["BONE_INDEX"] and i + 1 < len(children):
                    sibling = children[i + 1]["BONE_INDEX"]
                    break

        bone.sibling_index = sibling

    for flag in obj.bone_properties.flags:
        if len(flag.name) == 0:
            continue

        bone.flags.append(flag.name)

    if len(obj.children) > 0:
        bone.flags.append("Unk0")

    mat = obj.matrix_local
    if (obj.parent != None):
        mat = obj.parent.matrix_local.inverted() @ obj.matrix_local

    mat_decomposed = mat.decompose()

    bone.translation = mat_decomposed[0]
    bone.rotation = mat_decomposed[1]
    bone.scale = mat_decomposed[2]
    # transform_unk doesn't appear in openformats so oiv calcs it right
    # what does it do? the bone length?
    # default value for this seems to be <TransformUnk x="0" y="4" z="-3" w="0" />
    bone.transform_unk = Quaternion((0, 0, 4, -3))

    return bone


def skeleton_from_object(obj):

    if obj.type != 'ARMATURE' or len(obj.pose.bones) == 0:
        return None

    skeleton = SkeletonProperty()
    bones = obj.pose.bones

    ind = 0
    for pbone in bones:
        bone = pbone.bone
        bone["BONE_INDEX"] = ind
        ind = ind + 1

    for pbone in bones:
        bone = bone_from_object(pbone.bone)
        skeleton.bones.append(bone)

    return skeleton


def rotation_limit_from_object(obj):
    for con in obj.constraints:
        if con.type == 'LIMIT_ROTATION':
            joint = RotationLimitItem()
            joint.bone_id = obj.bone.bone_properties.tag
            joint.min = Vector((con.min_x, con.min_y, con.min_z))
            joint.max = Vector((con.max_x, con.max_y, con.max_z))
            return joint

    return None


def joints_from_object(obj):
    if obj.pose is None:
        return None

    joints = JointsProperty()
    for bone in obj.pose.bones:
        joint = rotation_limit_from_object(bone)
        if joint is not None:
            joints.rotation_limits.append(joint)

    return joints


def light_from_object(obj):
    light = LightItem()
    light.position = obj.location
    light.direction = obj.rotation_euler
    light.color = obj.data.color
    light.flashiness = obj.data.specular_factor * 100
    light.intensity = obj.data.energy
    light.type = SOLLUMZ_UI_NAMES[obj.data.light_properties.type]
    light.flags = obj.data.light_properties.flags
    light.bone_id = obj.data.light_properties.bone_id
    light.type = obj.data.light_properties.type
    light.group_id = obj.data.light_properties.group_id
    light.time_flags = obj.data.light_properties.time_flags
    light.falloff = obj.data.light_properties.falloff
    light.falloff_exponent = obj.data.light_properties.falloff_exponent
    cpn = obj.data.light_properties.culling_plane_normal
    light.culling_plane_normal = Vector((cpn[0], cpn[1], cpn[2]))
    light.culling_plane_offset = obj.data.light_properties.culling_plane_offset
    light.unknown_45 = obj.data.light_properties.unknown_45
    light.unknown_46 = obj.data.light_properties.unknown_46
    light.volume_intensity = obj.data.light_properties.volume_intensity
    light.volume_size_scale = obj.data.light_properties.volume_size_scale
    voc = obj.data.light_properties.volume_outer_color
    # relocate but works for now..
    color = collections.namedtuple("Color", ["r", "g", "b"])
    light.volume_outer_color = color(voc[0], voc[1], voc[2])
    light.light_hash = obj.data.light_properties.light_hash
    light.volume_outer_intensity = obj.data.light_properties.volume_outer_intensity
    light.corona_size = obj.data.light_properties.corona_size
    light.volume_outer_exponent = obj.data.light_properties.volume_outer_exponent
    light.light_fade_distance = obj.data.light_properties.light_fade_distance
    light.shadow_fade_distance = obj.data.light_properties.shadow_fade_distance
    light.specular_fade_distance = obj.data.light_properties.specular_fade_distance
    light.volumetric_fade_distance = obj.data.light_properties.volumetric_fade_distance
    light.shadow_near_clip = obj.data.light_properties.shadow_near_clip
    light.corona_intensity = obj.data.light_properties.corona_intensity
    light.corona_z_bias = obj.data.light_properties.corona_z_bias
    tnt = obj.data.light_properties.tangent
    light.tangent = Vector((tnt[0], tnt[1], tnt[2]))
    light.cone_inner_angle = obj.data.light_properties.cone_inner_angle
    light.cone_outer_angle = obj.data.light_properties.cone_outer_angle
    ext = obj.data.light_properties.extent
    light.extent = Vector((ext[0], ext[1], ext[2]))
    light.projected_texture_hash = obj.data.light_properties.projected_texture_hash

    return light


# REALLY NOT A FAN OF PASSING THIS EXPORT OP TO THIS AND APPENDING TO MESSAGES BUT WHATEVER
def drawable_from_object(exportop, obj, exportpath, bones=None, export_settings=None):
    drawable = Drawable()

    drawable.name = obj.name
    drawable.bounding_sphere_center = get_bound_center(
        obj, world=export_settings.use_transforms)
    drawable.bounding_sphere_radius = get_obj_radius(
        obj, world=export_settings.use_transforms)
    bbmin, bbmax = get_bound_extents(obj, world=export_settings.use_transforms)
    drawable.bounding_box_min = bbmin
    drawable.bounding_box_max = bbmax

    drawable.lod_dist_high = obj.drawable_properties.lod_dist_high
    drawable.lod_dist_med = obj.drawable_properties.lod_dist_high
    drawable.lod_dist_low = obj.drawable_properties.lod_dist_high
    drawable.lod_dist_vlow = obj.drawable_properties.lod_dist_high

    shaders = get_shaders_from_blender(obj)

    if len(shaders) == 0:
        raise Exception(
            f"No materials on object: {obj.name}, will be skipped.")

    for shader in shaders:
        drawable.shader_group.shaders.append(shader)

    td, messages = texture_dictionary_from_materials(
        obj, os.path.dirname(exportpath))
    drawable.shader_group.texture_dictionary = td
    exportop.messages += messages

    if bones is None:
        if obj.pose is not None:
            bones = obj.pose.bones

    drawable.skeleton = skeleton_from_object(obj)
    drawable.joints = joints_from_object(obj)
    if obj.pose is not None:
        for bone in drawable.skeleton.bones:
            pbone = obj.pose.bones[bone.index]
            for con in pbone.constraints:
                if con.type == 'LIMIT_ROTATION':
                    bone.flags.append("LimitRotation")
                    break

    highmodel_count = 0
    medmodel_count = 0
    lowhmodel_count = 0
    vlowmodel_count = 0

    for child in obj.children:
        if child.sollum_type == SollumType.DRAWABLE_MODEL:
            drawable_model = drawable_model_from_object(
                child, bones, export_settings)
            if child.drawable_model_properties.sollum_lod == LODLevel.HIGH:
                highmodel_count += 1
                drawable.drawable_models_high.append(drawable_model)
            elif child.drawable_model_properties.sollum_lod == LODLevel.MEDIUM:
                medmodel_count += 1
                drawable.drawable_models_med.append(drawable_model)
            elif child.drawable_model_properties.sollum_lod == LODLevel.LOW:
                lowhmodel_count += 1
                drawable.drawable_models_low.append(drawable_model)
            elif child.drawable_model_properties.sollum_lod == LODLevel.VERYLOW:
                vlowmodel_count += 1
                drawable.drawable_models_vlow.append(drawable_model)
        if child.sollum_type in BOUND_TYPES:
            if child.sollum_type == SollumType.BOUND_COMPOSITE:
                drawable.bound = composite_from_object(child, export_settings)
            else:
                drawable.bound = bound_from_object(child, export_settings)
        elif child.type == 'LIGHT' and child.data.light_properties.type != LightType.NONE:
            drawable.lights.append(light_from_object(child))

    # flags = model count for each lod
    drawable.flags_high = highmodel_count
    drawable.flags_med = medmodel_count
    drawable.flags_low = lowhmodel_count
    drawable.flags_vlow = vlowmodel_count
    # drawable.unknown_9A = ?

    return drawable


def export_ydr(exportop, obj, filepath, export_settings):
    drawable_from_object(exportop, obj, filepath, None,
                         export_settings).write_xml(filepath)
