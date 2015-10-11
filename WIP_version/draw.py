# -*- coding: utf-8 -*-

import bpy
import os
import subprocess
from os import listdir
from os.path import isfile, join
 
preview_collections = {}
 
        #########################
        ####    FONCTIONS    ####
        #########################
 
def apply_material(mat_name):
    ob = bpy.context.active_object
 
    # Get material
    if bpy.data.materials.get(mat_name):
        mat = bpy.data.materials[mat_name]
    else:
        # create material
        mat = bpy.data.materials.new(name=mat_name)
 
    # Assign it to object
    if len(ob.data.materials):
        # assign to 1st material slot
        ob.data.materials[0] = mat
    else:
        # no slots
        ob.data.materials.append(mat)
       
   
def import_materials_from_files(self, context):
    
    library_path = os.path.dirname(__file__)   

    SECTION   = "Material" # on importe un matériau
    mat_name = (bpy.data.window_managers["WinMan"].my_previews.split("."))[0]
   
    if mat_name in bpy.data.materials:
        bpy.context.active_object.active_material = bpy.data.materials[mat_name]
       
    else:                  
        blendfile_1 = join(library_path,'Shader_Library.blend')
        source_files = [blendfile_1] # liste des fichiers où tu va chercher les matériaux
 
        with bpy.data.libraries.load(blendfile_1) as (data_from, data_to):
            if data_from.materials:                 
                directory = join(blendfile_1, SECTION)
               
                bpy.ops.wm.append(filename=mat_name, directory=directory)
       
        apply_material(mat_name)

def import_materials_in_library():
    library_path = os.path.dirname(os.path.abspath(__file__)) 
    
    blendfile = join(library_path, "BSL_temp.blend")
    material = bpy.context.object.active_material.name
    
    bpy.ops.wm.save_mainfile(filepath = blendfile)
    
    BSL_shader_library = join(library_path, 'Shader_Library.blend') # ou bpy.utils.resource_path('USER') + "scripts/addons/material_library"
    BSL_import_script = join(library_path, 'import_in_library_from_external_file.py')
    
    print('[BSL] Import - ', 'File:', blendfile, 'Material:', material, 'Library:', BSL_shader_library, 'Script:', BSL_import_script)
    
    sub = subprocess.Popen([bpy.app.binary_path, BSL_shader_library, '-b', '--python', BSL_import_script, blendfile, material])
    sub.wait()
    
def generate_preview():
    library_path = os.path.dirname(os.path.abspath(__file__))
    
    material = bpy.context.object.active_material.name
    
    BSL_thumbnails_directory = join(library_path, 'Thumbnails')
    BSL_shader_library = join(library_path, 'Shader_Library.blend') # ou bpy.utils.resource_path('USER') + "scripts/addons/material_library"
    BSL_generate_script = join(library_path, 'generate_preview.py')
    
    #print('[BSL] Generate Preview - ', 'Directory:', BSL_thumbnails_directory, 'Material:',material, 'Library:', BSL_shader_library, 'Script:',BSL_generate_script)
    
    sub = subprocess.Popen([bpy.app.binary_path, BSL_shader_library, '-b', '--python', BSL_generate_script, material, BSL_thumbnails_directory])    
    sub.wait()

def remove_material_from_library():
    library_path = os.path.dirname(os.path.abspath(__file__))    
    material = bpy.context.object.active_material.name
    BSL_shader_library = join(library_path, 'Shader_Library.blend')
    BSL_generate_script = join(library_path, 'remove_material_from_library.py')
    BSL_thumbnails_directory = join(library_path, 'Thumbnails')
    thumbnail_remove = join(BSL_thumbnails_directory, material + ".jpeg")
    
    sub = subprocess.Popen([bpy.app.binary_path, BSL_shader_library, '-b', '--python', BSL_generate_script, material])    
    sub.wait()
    
    os.remove(thumbnail_remove)

    
def get_enum_previews(self, context): # self et context demandés par l'API
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
 
    print("Scanning thumbnails directory: %s" % directory)
 
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
            enum_items.append((name, name, name, thumb.icon_id, i)) # 3pts\addons\material_library\import_in_library_from_external_fil
 
    pcoll.my_previews = enum_items
    print('[BSL] - Thumbnails list:', enum_items)
    pcoll.my_previews_dir = directory
    
    return pcoll.my_previews

class ImportIntoBSL(bpy.types.Operator):
    bl_idname = "material.import_into_bsl"
    bl_label = "Add Material to BSL"
    bl_description = "Import the current material into BSL - Needs a saved file to work"
    bl_options = {"REGISTER", "INTERNAL"}
    
    @classmethod
    def poll(cls, context):
        return bpy.context.object.active_material
      
    def execute(self, context):
        
        import_materials_in_library()
        
        library_path = os.path.dirname(__file__)
        material = bpy.context.object.active_material.name # à faire avant lancement subprocess, qui n'y aura plus accès (au context du fichier courant)
        
        context.window_manager.is_generating_preview = True
        
        #bpy.utils.previews.remove(preview_collections["main"])
        subprocess.Popen([bpy.app.binary_path, join(library_path, 'Shader_Library.blend'), '-b', '--python', join(library_path, 'import.py'), material])
        
        context.window_manager.is_generating_preview = False
        
        #bpy.ops.material.update_thumbnails() ### A modifier (modal ?) pour qu'il attende la fin de la génération, sans être bloquant
        
        return {"FINISHED"}

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

        
class DeleteUnusedMaterials(bpy.types.Operator):
    bl_idname = "material.delete_unused_materials"
    bl_label = "Delete Unused Materials"
    bl_description = "Delete Unused Materials"
    bl_options = {"REGISTER", "INTERNAL"}
   
    @classmethod
    def poll(cls, context):
        return True
   
    def execute(self, context):
        materials = bpy.data.materials
 
        for material in bpy.data.materials:
            if not material.users:
                materials.remove(material)
       
        return {"FINISHED"}
 

class RemoveMaterialFromBSL(bpy.types.Operator):
    bl_idname = "material.remove_material_from_bsl"
    bl_label = "Remove material from BSL"
    bl_description = "Remove selected material from your library"
    bl_options = {"REGISTER", "INTERNAL"}
    
    @classmethod
    def poll(cls, context):
        return bpy.context.object.active_material
    
    def execute(self, context):
        remove_material_from_library()
        
        return{"FINISHED"}
       
        #####################
        ####    PANEL    ####
        #####################
 
class BSL_panel(bpy.types.Panel):
    bl_idname = "BSL_panel"
    bl_label = "BSL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
   
   
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        
        #layout.operator("material.delete_unused_materials",text="Remove", icon='CANCEL')
        layout.template_icon_view(wm, "my_previews")
         
        layout.label("Objects:", icon='OBJECT_DATAMODE')
        row = layout.row(align=True)
        row.operator("object.material_slot_remove",text="Remove Material", icon='X')          
        row.operator("material.delete_unused_materials",text="Unused", icon='X')
        layout.operator("object.select_linked", icon='RESTRICT_SELECT_OFF').type='MATERIAL'
        


def BSL_AddMaterial(self, context):
    layout = self.layout
    wm = context.window_manager
    
    layout.label("Blender Shader Library")   
    row = layout.row(align=True)
    row.operator("material.import_into_bsl",text="Add Material To Library", icon='ZOOMIN')
    row.operator("material.update_thumbnails",text="", icon='FILE_REFRESH')
    row = layout.row(align=True)
    row.operator("material.remove_material_from_bsl", text="Remove material")
    layout.template_icon_view(wm, "my_previews")  
           
    
    layout.operator("material.delete_unused_materials",text="Delete Unused Material", icon='X')
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
