# -*- coding: utf-8 -*-

import bpy
import os
import bpy.utils.previews
from os import listdir
from os.path import join
from bpy.types import WindowManager
from bpy.props import EnumProperty
from . bml_import_utils import import_materials_from_BML


BML_preview_collections = {}


#class UpdateThumbnails(bpy.types.Operator):
#    bl_idname = "material.update_thumbnails"
#    bl_label = "Update Thumbnails"
#    bl_description = "(Re)generate thumbnails images. May take a while"
#    bl_options = {'REGISTER', 'INTERNAL'}

#    def execute(self, context):
#        
#        register_BML_pcoll_preview()
#        self.report({'INFO'}, "Thumbnails and preview updated") # marche que si appel depuis l'UI

#        return {'FINISHED'}


def update_preview_type(self, context):
    register_BML_pcoll_preview()


def get_enum_previews(self, context): # self et context demandés par l'API
    """ """
    return enum_previews_from_directory_items(context.window_manager.is_generating_preview)


def enum_previews_from_directory_items(is_generating_preview):
    """ N'utilise pas self et context, pour un appel externe au preset de Blender """
    enum_items = []

    if bpy.context is None:
        return enum_items

    wm = bpy.context.window_manager

    if wm.preview_type == '_Sphere':
        thumbnail_type= "Sphere"
    elif wm.preview_type == '_Cloth':
        thumbnail_type= "Cloth"
    elif wm.preview_type == '_Softbox':
        thumbnail_type= "Softbox"
    elif wm.preview_type == '_Hair':
        thumbnail_type= "Hair"
        
    directory = join(os.path.dirname(__file__), "Thumbnails",thumbnail_type )

    # Get the preview collection (defined in register func).
    pcoll = BML_preview_collections["main"]

    if is_generating_preview or directory == pcoll.BML_previews_dir:
        return pcoll.BML_previews

    print("[BML] Scanning thumbnails directory: %s" % directory)

    if directory and os.path.exists(directory):
        # Scan the directory for jpg files
        image_paths = []
        for fn in os.listdir(directory):
            if fn.lower().endswith(".jpg") or fn.lower().endswith(".jpeg") or fn.lower().endswith(".png"):
                image_paths.append(fn)

        for i, name in enumerate(image_paths):
            # generates a thumbnail preview for a file.
            filepath = os.path.join(directory, name)
            thumb = pcoll.load(filepath, filepath, 'IMAGE')
            enum_items.append((name, name, name, thumb.icon_id, i)) # 3 bpy.utils.resource_path('USER') + "scripts/addons/material_lib

    pcoll.BML_previews = enum_items
    
    # print('[BML] - Thumbnails list:', enum_items)
    print('[BML] - Thumbnails list:', [item[0] for item in enum_items], 'Length:', len(enum_items))
    pcoll.BML_previews_dir = directory
    
    
def register_BML_pcoll_preview():
    wm = bpy.context.window_manager

    global BML_preview_collections
    for pcoll in BML_preview_collections.values():
        bpy.utils.previews.remove(pcoll)
        
    WindowManager.BML_previews = EnumProperty(
            items=get_enum_previews,
            update=import_materials_from_BML)
    
    pcoll = bpy.utils.previews.new() # pcoll pour preview collection
    pcoll.BML_previews_dir = ""
    pcoll.BML_previews = ()
    
    BML_preview_collections = {}
    BML_preview_collections["main"] = pcoll


def unregister_BML_pcoll_preview():

    del WindowManager.BLM_previews

    for pcoll in BML_preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    BML_preview_collections.clear()