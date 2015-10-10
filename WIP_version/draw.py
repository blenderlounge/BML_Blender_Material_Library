import bpy
import os
import subprocess
from os import listdir
from os.path import join
from . utils import ImportIntoBSL, DeleteUnusedMaterials, import_materials_from_files
 
preview_collections = {}
 
        #########################
        ####    FONCTIONS    ####
        #########################

   
def enum_previews_from_directory_items(self, context):
    """EnumProperty callback"""
    enum_items = [] 
 
    if context is None:
        return enum_items
    
    library_path = os.path.dirname(__file__)
    directory = join(library_path, "Thumbnails")
        
    # Get the preview collection (defined in register func).
    pcoll = preview_collections["main"]
 
    if directory == pcoll.my_previews_dir:
        return pcoll.my_previews
 
    print("Scanning directory: %s" % directory)
 
    if directory and os.path.exists(directory):
        # Scan the directory for png files
        image_paths = []
        for fn in os.listdir(directory):
            if fn.lower().endswith(".jpg"):
                image_paths.append(fn)
 
        for i, name in enumerate(image_paths):
            # generates a thumbnail preview for a file.
            filepath = os.path.join(directory, name)
            thumb = pcoll.load(filepath, filepath, 'IMAGE')
            enum_items.append((name, name, "", thumb.icon_id, i))
 
    pcoll.my_previews = enum_items
    pcoll.my_previews_dir = directory
    return pcoll.my_previews
  
   
        #####################
        ####    PANEL    ####
        #####################
 
class BSL_panel(bpy.types.Panel):
    bl_idname = "BSL_panel"
    bl_label = "BSL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
   
   
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        layout.label("Library:", icon='FILESEL')
        row = layout.row(align=True)
        row.operator("wm.save_as_mainfile",text="Save", icon='SAVE_AS')
        row.operator("material.delete_unused_materials",text="Remove", icon='CANCEL')
       
        layout.template_icon_view(wm, "my_previews")
         
        layout.label("Objects:", icon='OBJECT_DATAMODE')
        row = layout.row(align=True)
        row.operator("object.material_slot_remove",text="Remove Material", icon='X')          
        row.operator("material.delete_unused_materials",text="Unused")
        layout.operator("object.select_linked", icon='RESTRICT_SELECT_OFF').type='MATERIAL'
        layout.operator("material.import_into_bsl")


def BSL_AddMaterial(self, context):
    layout = self.layout
    layout.label("BSL fonctions")            
    layout.operator("material.delete_unused_materials",text="Delete unused")
    layout.operator("material.import_into_bsl")
           
 
       
def register_pcoll_preview():  
    from bpy.types import WindowManager
    from bpy.props import EnumProperty
            
    WindowManager.my_previews = EnumProperty(
            items=enum_previews_from_directory_items,
            update=import_materials_from_files) 
           
    import bpy.utils.previews
    wm = bpy.context.window_manager
    pcoll = bpy.utils.previews.new()
    pcoll.my_previews_dir = ""
    pcoll.my_previews = ()
 
    preview_collections["main"] = pcoll
    
def unregister_pcoll_preview():
    from bpy.types import WindowManager
 
    del WindowManager.my_previews
 
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()
