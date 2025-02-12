from ..resources.drawable import *
from ..tools.meshhelper import *
from ..tools.utils import *
from ..ydr.ydrexport import drawable_from_object
from ..tools import jenkhash
from ..sollumz_properties import SollumType


def get_hash(item):
    return jenkhash.Generate(item[1].name.split(".")[0])


def drawable_dict_from_object(exportop, obj, filepath, export_settings):

    drawable_dict = DrawableDictionary()

    bones = None
    for child in obj.children:
        if child.sollum_type == SollumType.DRAWABLE and child.type == 'ARMATURE' and len(child.pose.bones) > 0:
            bones = child.pose.bones
            break

    for child in obj.children:
        if child.sollum_type == SollumType.DRAWABLE:
            drawable = drawable_from_object(
                exportop, child, filepath, bones, export_settings)
            drawable_dict[drawable.name] = drawable

    drawable_dict.sort(key=get_hash)

    return drawable_dict


def export_ydd(exportop, obj, filepath, export_settings):
    drawable_dict_from_object(exportop, obj, filepath,
                              export_settings).write_xml(filepath)
