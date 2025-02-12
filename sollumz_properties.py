import bpy
from enum import Enum


class SollumType(str, Enum):
    NONE = "sollumz_none"

    FRAGMENT = "sollumz_fragment"
    LOD = "sollumz_lod"
    ARCHETYPE = "sollumz_archetype"
    CHILD = "sollumz_child"

    DRAWABLE_DICTIONARY = "sollumz_drawable_dictionary"
    DRAWABLE = "sollumz_drawable"
    DRAWABLE_MODEL = "sollumz_drawable_model"
    DRAWABLE_GEOMETRY = "sollumz_drawable_geometry"
    SKELETON = "sollumz_skeleton"
    LIGHT = "sollumz_light"

    BOUND_BOX = "sollumz_bound_box"
    BOUND_SPHERE = "sollumz_bound_sphere"
    BOUND_CAPSULE = "sollumz_bound_capsule"
    BOUND_CYLINDER = "sollumz_bound_cylinder"
    BOUND_DISC = "sollumz_bound_disc"
    BOUND_CLOTH = "sollumz_bound_cloth"
    BOUND_GEOMETRY = "sollumz_bound_geometry"
    BOUND_GEOMETRYBVH = "sollumz_bound_geometrybvh"
    BOUND_COMPOSITE = "sollumz_bound_composite"

    BOUND_POLY_BOX = "sollumz_bound_poly_box"
    BOUND_POLY_SPHERE = "sollumz_bound_poly_sphere"
    BOUND_POLY_CAPSULE = "sollumz_bound_poly_capsule"
    BOUND_POLY_CYLINDER = "sollumz_bound_poly_cylinder"
    BOUND_POLY_TRIANGLE = "sollumz_bound_poly_triangle"


class LightType(str, Enum):
    NONE = 'sollumz_light_none'
    POINT = 'sollumz_light_point'
    SPOT = 'sollumz_light_spot'
    CAPSULE = 'sollumz_light_capsule'


class MaterialType(str, Enum):
    NONE = "sollumz_material_none",
    SHADER = "sollumz_material_shader",
    COLLISION = "sollumz_material_collision"


class TextureUsage(str, Enum):
    UNKNOWN = "sollumz_unknown"
    TINTPALETTE = "sollumz_tintpalette"
    DEFAULT = "sollumz_default"
    TERRAIN = "sollumz_terrain"
    CLOUDDENSITY = "sollumz_clouddensity"
    CLOUDNORMAL = "sollumz_cloudnormal"
    CABLE = "sollumz_cable"
    FENCE = "sollumz_fence"
    ENVEFFECT = "sollumz_env.effect"
    SCRIPT = "sollumz_script"
    WATERFLOW = "sollumz_waterflow"
    WATERFOAM = "sollumz_waterfoam"
    WATERFOG = "sollumz_waterfog"
    WATEROCEAN = "sollumz_waterocean"
    WATER = "sollumz_water"
    FOAMOPACITY = "sollumz_foamopacity"
    FOAM = "sollumz_foam"
    DIFFUSEDETAIL = "sollumz_diffusedetail"
    DIFFUSEDARK = "sollumz_diffusedark"
    DIFFUSEALPHAOPAQUE = "sollumz_diffuseaplhaopaque"
    DETAIL = "sollumz_detail"
    NORMAL = "sollumz_normal"
    SPECULAR = "sollumz_specular"
    EMMISIVE = "sollumz_emmisive"
    SKIPPROCESSING = "sollumz_skipprocessing"
    DONTOPTIMIZE = "sollumz_dontoptimize"
    TEST = "sollumz_test"
    COUNT = "sollumz_count"
    DIFFUSE = "sollumz_diffuse"


class TextureFormat(str, Enum):
    DXT1 = "sollumz_dxt1"
    DXT3 = "sollumz_dxt3"
    DXT5 = "sollumz_dxt5"
    ATI1 = "sollumz_ati1"
    ATI2 = "sollumz_ati2"
    BC7 = "sollumz_bc7"
    A1R5G5B5 = "sollumz_a1r5g5b5"
    A1R8G8B8 = "sollumz_a1r8g8b8"
    A8R8G8B8 = "sollumz_a8r8g8b8"
    A8 = "sollumz_a8"
    L8 = "sollumz_l8"


class LODLevel(str, Enum):
    HIGH = "sollumz_high"
    MEDIUM = "sollumz_medium"
    LOW = "sollumz_low"
    VERYLOW = "sollumz_verylow"


class EntityLodLevel(str, Enum):
    LODTYPES_DEPTH_HD = "sollumz_lodtypes_depth_hd"
    LODTYPES_DEPTH_LOD = "sollumz_lodtypes_depth_lod"
    LODTYPES_DEPTH_SLOD1 = "sollumz_lodtypes_depth_slod1"
    LODTYPES_DEPTH_SLOD2 = "sollumz_lodtypes_depth_slod2"
    LODTYPES_DEPTH_SLOD3 = "sollumz_lodtypes_depth_slod3"
    LODTYPES_DEPTH_SLOD4 = "sollumz_lodtypes_depth_slod4"
    LODTYPES_DEPTH_ORPHANHD = "sollumz_lodtypes_depth_orphanhd"


class EntityPriorityLevel(str, Enum):
    PRI_REQUIRED = "sollumz_pri_required"
    PRI_OPTIONAL_HIGH = "sollumz_pri_optional_high"
    PRI_OPTIONAL_MEDIUM = "sollumz_pri_optional_medium"
    PRI_OPTIONAL_LOW = "sollumz_pri_optional_low"


FRAGMENT_TYPES = [
    SollumType.FRAGMENT,
    SollumType.LOD,
    SollumType.CHILD,
    SollumType.ARCHETYPE,
]

BOUND_TYPES = [
    SollumType.BOUND_COMPOSITE,
    SollumType.BOUND_BOX,
    SollumType.BOUND_SPHERE,
    SollumType.BOUND_CYLINDER,
    SollumType.BOUND_CAPSULE,
    SollumType.BOUND_DISC,
    SollumType.BOUND_GEOMETRY,
    SollumType.BOUND_GEOMETRYBVH,
    SollumType.BOUND_GEOMETRYBVH,
]

BOUND_POLYGON_TYPES = [
    SollumType.BOUND_POLY_BOX,
    SollumType.BOUND_POLY_SPHERE,
    SollumType.BOUND_POLY_CAPSULE,
    SollumType.BOUND_POLY_CYLINDER,
    SollumType.BOUND_POLY_TRIANGLE,
]

DRAWABLE_TYPES = [
    SollumType.DRAWABLE_DICTIONARY,
    SollumType.DRAWABLE,
    SollumType.DRAWABLE_MODEL,
    SollumType.DRAWABLE_GEOMETRY,
    SollumType.SKELETON,
]

SOLLUMZ_UI_NAMES = {
    SollumType.BOUND_BOX: "Bound Box",
    SollumType.BOUND_SPHERE: "Bound Sphere",
    SollumType.BOUND_CAPSULE: "Bound Capsule",
    SollumType.BOUND_CYLINDER: "Bound Cylinder",
    SollumType.BOUND_DISC: "Bound Disc",
    SollumType.BOUND_CLOTH: "Bound Cloth",
    SollumType.BOUND_GEOMETRY: "Bound Geometry",
    SollumType.BOUND_GEOMETRYBVH: "Bound GeometryBVH",
    SollumType.BOUND_COMPOSITE: "Bound Composite",

    SollumType.BOUND_POLY_BOX: "Bound Poly Box",
    SollumType.BOUND_POLY_SPHERE: "Bound Poly Sphere",
    SollumType.BOUND_POLY_CAPSULE: "Bound Poly Capsule",
    SollumType.BOUND_POLY_CYLINDER: "Bound Poly Cylinder",
    SollumType.BOUND_POLY_TRIANGLE: "Bound Poly Mesh",

    SollumType.FRAGMENT: "Fragment",
    SollumType.LOD: "Fragment LOD",
    SollumType.ARCHETYPE: "Fragment Archetype",
    SollumType.CHILD: "Fragment Child",

    SollumType.NONE: "None",
    SollumType.DRAWABLE_DICTIONARY: "Drawable Dictionary",
    SollumType.DRAWABLE: "Drawable",
    SollumType.DRAWABLE_MODEL: "Drawable Model",
    SollumType.DRAWABLE_GEOMETRY: "Geometry",
    SollumType.SKELETON: "Skeleton",
    SollumType.LIGHT: "Light",

    MaterialType.NONE: "None",
    MaterialType.SHADER: "Sollumz Material",
    MaterialType.COLLISION: "Sollumz Collision Material",

    TextureUsage.UNKNOWN: "UNKNOWN",
    TextureUsage.TINTPALETTE: "TINTPALETTE",
    TextureUsage.DEFAULT: "DEFAULT",
    TextureUsage.TERRAIN: "TERRAIN",
    TextureUsage.CLOUDDENSITY: "CLOUDDENSITY",
    TextureUsage.CLOUDNORMAL: "CLOUDNORMAL",
    TextureUsage.CABLE: "CABLE",
    TextureUsage.FENCE: "FENCE",
    TextureUsage.ENVEFFECT: "ENV.EFFECT",
    TextureUsage.SCRIPT: "SCRIPT",
    TextureUsage.WATERFLOW: "WATERFLOW",
    TextureUsage.WATERFOAM: "WATERFOAM",
    TextureUsage.WATERFOG: "WATERFOG",
    TextureUsage.WATEROCEAN: "WATEROCEAN",
    TextureUsage.WATER: "WATER",
    TextureUsage.FOAMOPACITY: "FOAMOPACITY",
    TextureUsage.FOAM: "FOAM",
    TextureUsage.DIFFUSEDETAIL: "DIFFUSEDETAIL",
    TextureUsage.DIFFUSEDARK: "DIFFUSEDARK",
    TextureUsage.DIFFUSEALPHAOPAQUE: "DIFFUSEALPHAOPAQUE",
    TextureUsage.DETAIL: "DETAIL",
    TextureUsage.NORMAL: "NORMAL",
    TextureUsage.SPECULAR: "SPECULAR",
    TextureUsage.EMMISIVE: "EMMISIVE",
    TextureUsage.SKIPPROCESSING: "SKIPPROCESSING",
    TextureUsage.DONTOPTIMIZE: "DONTOPTIMIZE",
    TextureUsage.TEST: "TEST",
    TextureUsage.COUNT: "COUNT",
    TextureUsage.DIFFUSE: "DIFFUSE",

    TextureFormat.DXT1: "D3DFMT_DXT1",
    TextureFormat.DXT3: "D3DFMT_DXT3",
    TextureFormat.DXT5: "D3DFMT_DXT5",
    TextureFormat.ATI1: "D3DFMT_ATI1",
    TextureFormat.ATI2: "D3DFMT_ATI2",
    TextureFormat.BC7: "D3DFMT_DXT1",
    TextureFormat.A1R5G5B5: "D3DFMT_DXT1",
    TextureFormat.A1R8G8B8: "D3DFMT_DXT1",
    TextureFormat.A8R8G8B8: "D3DFMT_DXT1",
    TextureFormat.A8: "D3DFMT_DXT1",
    TextureFormat.L8: "D3DFMT_DXT1",

    LODLevel.HIGH: "High",
    LODLevel.MEDIUM: "Med",
    LODLevel.LOW: "Low",
    LODLevel.VERYLOW: "Vlow",

    EntityLodLevel.LODTYPES_DEPTH_HD: "DEPTH HD",
    EntityLodLevel.LODTYPES_DEPTH_LOD: "DEPTH LOD",
    EntityLodLevel.LODTYPES_DEPTH_SLOD1: "DEPTH SLOD1",
    EntityLodLevel.LODTYPES_DEPTH_SLOD2: "DEPTH SLOD2",
    EntityLodLevel.LODTYPES_DEPTH_SLOD3: "DEPTH SLOD3",
    EntityLodLevel.LODTYPES_DEPTH_SLOD4: "DEPTH SLOD4",
    EntityLodLevel.LODTYPES_DEPTH_ORPHANHD: "DEPTH ORPHAN HD",

    EntityPriorityLevel.PRI_REQUIRED: "REQUIRED",
    EntityPriorityLevel.PRI_OPTIONAL_HIGH: "OPTIONAL HIGH",
    EntityPriorityLevel.PRI_OPTIONAL_MEDIUM: "OPTIONAL MEDIUM",
    EntityPriorityLevel.PRI_OPTIONAL_LOW: "OPTIONAL LOW",

    LightType.NONE: 'None',
    LightType.POINT: 'Point',
    LightType.SPOT: 'Spot',
    LightType.CAPSULE: 'Capsule',
}

# Generate items from provided enums


def items_from_enums(*enums):
    items = []
    for enum in enums:
        for item in enum:
            if item not in SOLLUMZ_UI_NAMES:
                raise KeyError(
                    f"UI name mapping not found for key {item} of {enum}.")
            items.append(
                (item.value, SOLLUMZ_UI_NAMES[item], ""))
    return items


class EntityProperties(bpy.types.PropertyGroup):
    archetype_name: bpy.props.StringProperty(name="ArchetypeName")
    flags: bpy.props.IntProperty(name="Flags")
    guid: bpy.props.FloatProperty(name="Guid")
    parent_index: bpy.props.IntProperty(name="ParentIndex")
    lod_dist: bpy.props.FloatProperty(name="Lod Distance")
    child_lod_dist: bpy.props.FloatProperty(name="Child Lod Distance")
    lod_level: bpy.props.EnumProperty(
        items=items_from_enums(EntityLodLevel),
        name="LOD Level",
        default=EntityLodLevel.LODTYPES_DEPTH_HD,
        options={"HIDDEN"}
    )
    num_children: bpy.props.IntProperty(name="Number of Children")
    priority_level: bpy.props.EnumProperty(
        items=items_from_enums(EntityPriorityLevel),
        name="Priority Level",
        default=EntityPriorityLevel.PRI_REQUIRED,
        options={"HIDDEN"}
    )
    # extensions?
    ambient_occlusion_multiplier: bpy.props.FloatProperty(
        name="Ambient Occlusion Multiplier")
    artificial_ambient_occlusion: bpy.props.FloatProperty(
        name="Artificial Ambient Occlusion")
    tint_value: bpy.props.FloatProperty(name="Tint Value")


def hide_obj_and_children(obj, value):
    if obj.name in bpy.context.view_layer.objects:
        obj.hide_set(value)
    for child in obj.children:
        hide_obj_and_children(child, value)


def get_bool_prop(obj, key):
    try:
        return obj[key]
    except KeyError:
        return False


def get_hide_collisions(self):
    return get_bool_prop(self, "hide_collision")


def set_hide_collisions(self, value):
    self["hide_collision"] = value

    for obj in bpy.context.collection.all_objects:
        if(obj.sollum_type in BOUND_TYPES or obj.sollum_type in BOUND_POLYGON_TYPES):
            if obj.name in bpy.context.view_layer.objects:
                obj.hide_set(value)


def get_hide_high_lods(self):
    return get_bool_prop(self, "hide_high_lods")


def set_hide_high_lods(self, value):
    self["hide_high_lods"] = value

    for obj in bpy.context.collection.all_objects:
        if(obj.sollum_type == SollumType.DRAWABLE_MODEL):
            if(obj.drawable_model_properties.sollum_lod == LODLevel.HIGH):
                hide_obj_and_children(obj, value)


def get_hide_medium_lods(self):
    return get_bool_prop(self, "hide_medium_lods")


def set_hide_medium_lods(self, value):
    self["hide_medium_lods"] = value

    for obj in bpy.context.collection.all_objects:
        if(obj.sollum_type == SollumType.DRAWABLE_MODEL):
            if(obj.drawable_model_properties.sollum_lod == LODLevel.MEDIUM):
                hide_obj_and_children(obj, value)


def get_hide_low_lods(self):
    return get_bool_prop(self, "hide_low_lods")


def set_hide_low_lods(self, value):
    self["hide_low_lods"] = value

    for obj in bpy.context.collection.all_objects:
        if(obj.sollum_type == SollumType.DRAWABLE_MODEL):
            if(obj.drawable_model_properties.sollum_lod == LODLevel.LOW):
                hide_obj_and_children(obj, value)


def get_hide_very_low_lods(self):
    return get_bool_prop(self, "hide_very_low_lods")


def set_hide_very_low_lods(self, value):
    self["hide_very_low_lods"] = value

    for obj in bpy.context.collection.all_objects:
        if(obj.sollum_type == SollumType.DRAWABLE_MODEL):
            if(obj.drawable_model_properties.sollum_lod == LODLevel.VERYLOW):
                hide_obj_and_children(obj, value)


def register():
    bpy.types.Object.sollum_type = bpy.props.EnumProperty(
        items=items_from_enums(SollumType),
        name="Sollumz Type",
        default=SollumType.NONE,
        options={"HIDDEN"}
    )

    bpy.types.Material.sollum_type = bpy.props.EnumProperty(
        items=items_from_enums(MaterialType),
        name="Sollumz Material Type",
        default=MaterialType.NONE,
        options={"HIDDEN"}
    )

    bpy.types.ShaderNode.is_sollumz = bpy.props.BoolProperty(default=False)

    bpy.types.Object.entity_properties = bpy.props.PointerProperty(
        type=EntityProperties)

    bpy.types.Scene.hide_collision = bpy.props.BoolProperty(
        name="Hide Collision", get=get_hide_collisions, set=set_hide_collisions)
    bpy.types.Scene.hide_high_lods = bpy.props.BoolProperty(
        name="Hide High LODS", get=get_hide_high_lods, set=set_hide_high_lods)
    bpy.types.Scene.hide_medium_lods = bpy.props.BoolProperty(
        name="Hide Medium LODS", get=get_hide_medium_lods, set=set_hide_medium_lods)
    bpy.types.Scene.hide_low_lods = bpy.props.BoolProperty(
        name="Hide Low LODS", get=get_hide_low_lods, set=set_hide_low_lods)
    bpy.types.Scene.hide_very_low_lods = bpy.props.BoolProperty(
        name="Hide Very Low LODS", get=get_hide_very_low_lods, set=set_hide_very_low_lods)
    bpy.types.Scene.vert_paint_color = bpy.props.FloatVectorProperty(
        name="Vertex Color",
        subtype="COLOR",
        default=(1.0, 1.0, 1.0, 1.0),
        size=4
    )
    bpy.types.Scene.vert_paint_alpha = bpy.props.FloatProperty(
        name="Alpha", min=-1, max=1)
    bpy.types.Scene.create_seperate_objects = bpy.props.BoolProperty(
        name="Separate Objects", description="Create a object for each selected mesh.")
    bpy.types.Scene.use_mesh_name = bpy.props.BoolProperty(
        name="Use Name(s)", description="Use the names of the meshes for the created objects.", default=True)

    bpy.types.Scene.debug_sollum_type = bpy.props.EnumProperty(
        items=[(SollumType.DRAWABLE.value, SOLLUMZ_UI_NAMES[SollumType.DRAWABLE], SOLLUMZ_UI_NAMES[SollumType.DRAWABLE]),
               (SollumType.BOUND_COMPOSITE.value, SOLLUMZ_UI_NAMES[SollumType.BOUND_COMPOSITE], SOLLUMZ_UI_NAMES[SollumType.BOUND_COMPOSITE])],
        name="Hierarchy Type",
        default=SollumType.DRAWABLE,
        options={"HIDDEN"}
    )


def unregister():
    del bpy.types.Object.sollum_type
    del bpy.types.Material.sollum_type
    del bpy.types.Object.entity_properties
    del bpy.types.Scene.hide_collision
    del bpy.types.Scene.hide_high_lods
    del bpy.types.Scene.hide_medium_lods
    del bpy.types.Scene.hide_low_lods
    del bpy.types.Scene.hide_very_low_lods
    del bpy.types.Scene.vert_paint_color
    del bpy.types.Scene.vert_paint_alpha
    del bpy.types.Scene.create_seperate_objects
    del bpy.types.Scene.use_mesh_name
    del bpy.types.Scene.debug_sollum_type
