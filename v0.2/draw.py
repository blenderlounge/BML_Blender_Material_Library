import bpy
import os
import subprocess
from os import listdir
from os.path import join
from . import_utils import (ImportIntoBSL,
                            DeleteUnusedMaterials,
                            import_materials_from_files,
                            RemoveMaterialFromBML)
from bpy.types import Panel
 
preview_collections = {}
 
        ####################################
        ####    THUMBNAILS FONCTIONS    ####
        ####################################
        
        
class UpdateThumbnails(bpy.types.Operator):
    bl_idname = "material.update_thumbnails"
    bl_label = "Update Thumbnails"
    bl_description = "(Re)generate thumbnails images. May take a while"
    bl_options = {"REGISTER", "INTERNAL"}
      
    def execute(self, context):
        
        global preview_collections
        #del preview_collections["main"]
        preview_collections = {}
        register_pcoll_preview()
        
        return {"FINISHED"}
    
'''def generate_preview():
    library_path = os.path.dirname(os.path.abspath(__file__))
    
    material = bpy.context.object.active_material.name
    
    BSL_thumbnails_directory = join(library_path, 'Thumbnails')
    BSL_shader_library = join(library_path, 'Shader_Library.blend') # ou bpy.utils.resource_path('USER') + "scripts/addons/material_library"
    BSL_generate_script = join(library_path, 'generate_preview.py')
    
    #print('[BSL] Generate Preview - ', 'Directory:', BSL_thumbnails_directory, 'Material:',material, 'Library:', BSL_shader_library, 'Script:',BSL_generate_script)
    
    sub = subprocess.Popen([bpy.app.binary_path, BSL_shader_library, '-b', '--python', BSL_generate_script, material, BSL_thumbnails_directory])    
    sub.wait()'''

def get_enum_previews(self, context): # self et context demandes par l'API
    """EnumProperty callback"""
    return enum_previews_from_directory_items(context.window_manager.is_generating_preview)

def enum_previews_from_directory_items(is_generating_preview):
    """ N'utilise pas self et context, pour un appel externe au preset de Blender """
    enum_items = []
 
    if bpy.context is None:
        return enum_items
    
    library_path = os.path.dirname(__file__)
    directory = join(library_path, "Thumbnails")
        
    # Get the preview collection (defined in register func).
    pcoll = preview_collections["main"]
 
    if is_generating_preview or directory == pcoll.my_previews_dir:
        return pcoll.my_previews
 
    # print("Scanning thumbnails directory: %s" % directory)
 
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
 
    pcoll.my_previews = enum_items
    # print('[BSL] - Thumbnails list:', enum_items)
    pcoll.my_previews_dir = directory
    
    return pcoll.my_previews

  
        ######################
        ####    PANELS    ####
        ######################

   
     
class VIEW3D_PT_view_3d_bml(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Blender Material Library"
       
   
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        
        # layout.operator("material.delete_unused_materials",text="Remove", icon='CANCEL')
       
        layout.template_icon_view(wm, "my_previews")
         
        # layout.label("Objects:", icon='OBJECT_DATAMODE')
        row = layout.row(align=True)
#        row.operator("object.material_slot_remove",text="Remove Material", icon='X')          
#        row.operator("material.delete_unused_materials",text="Unused")
        layout.operator("object.select_linked", icon='RESTRICT_SELECT_OFF').type='MATERIAL'
#        layout.operator("material.import_into_bsl", icon='APPEND_BLEND')
#        layout.operator("material.update_thumbnails", icon='FILE_REFRESH')



class VIEW3D_PT_tools_bml(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "BML"
    bl_label = "Blender Material Library"
       
   
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        
        # layout.operator("material.delete_unused_materials",text="Remove", icon='CANCEL')
       
        layout.template_icon_view(wm, "my_previews")
         
        # layout.label("Objects:", icon='OBJECT_DATAMODE')
        row = layout.row(align=True)
#        row.operator("object.material_slot_remove",text="Remove Material", icon='X')          
#        row.operator("material.delete_unused_materials",text="Unused")
        layout.operator("object.select_linked", icon='RESTRICT_SELECT_OFF').type='MATERIAL'
#        layout.operator("material.import_into_bsl", icon='APPEND_BLEND')
#        layout.operator("material.update_thumbnails", icon='FILE_REFRESH')
        


class view3d_header_preview_bml(bpy.types.Menu):
    bl_idname = "material.view3d_header_preview"
    bl_label = "BML preview"
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        layout.template_icon_view(wm, "my_previews")
        
def VIEW3D_HT_header_bml_preview(self, context):
    layout = self.layout
    layout.menu("material.view3d_header_preview", text=" BML", icon='MATERIAL')
    
    

class NODE_PT_tools_bml(Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = "BML"
    bl_label = "Blender Material Library"
    
    def draw(self, context):                
        layout = self.layout
        wm = context.window_manager
        layout.template_icon_view(wm, "my_previews")
        row = layout.row(align=True)
        row.operator("material.import_into_bsl", icon='APPEND_BLEND')
        row.operator("material.update_thumbnails", icon='FILE_REFRESH')


class NODE_PT_ui_bml(Panel): 
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "Blender Material Library"  
    
    def draw(self, context):
        
        layout = self.layout
        wm = context.window_manager
        
        layout.template_icon_view(wm, "my_previews")
        row = layout.row(align=True)
        row.operator("material.import_into_bsl", icon='APPEND_BLEND')
        row.operator("material.update_thumbnails", icon='FILE_REFRESH')
            

class node_header_preview_bml(bpy.types.Menu):
    bl_idname = "material.node_header_preview"
    bl_label = "BML preview"
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        layout.template_icon_view(wm, "my_previews")
        
def NODE_HT_header_bml_preview(self, context):
    layout = self.layout
    layout.menu("material.node_header_preview", text=" BML", icon='MATERIAL')
    
                 
class Cycles_PT_bml_panel(Panel):
    '''Blender Material Library preview'''
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'    
    bl_label = "Blender Material Library"
    
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        row = layout.row(align=True)
        row.operator("material.import_into_bsl", icon='APPEND_BLEND')
        row.operator("material.remove_material_from_bml", icon='CANCEL')
        row.operator("material.update_thumbnails", text="", icon='FILE_REFRESH')
        layout.template_icon_view(wm, "my_previews")
        layout.operator("material.delete_unused_materials",text="Delete unused materials")
        layout.operator("object.select_linked", icon='RESTRICT_SELECT_OFF').type='MATERIAL'        
    
          
def register_pcoll_preview():  
    from bpy.types import WindowManager
    from bpy.props import EnumProperty
            
    WindowManager.my_previews = EnumProperty(
            items=get_enum_previews,
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
