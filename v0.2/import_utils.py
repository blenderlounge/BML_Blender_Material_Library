import bpy
import os
import subprocess
from os import listdir
from os.path import join


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
        ob.active_material = mat
    else:
        # no slots
        ob.data.materials.append(mat)
    
    
       
   
def import_materials_from_files(self, context):
    
    library_path = os.path.dirname(__file__)   

    SECTION   = "Material" # on importe un materiau
    mat_name = (bpy.data.window_managers["WinMan"].my_previews.split("."))[0]
    obj_list = []
    
    for item in bpy.context.selected_objects:
        name = item.name
        obj_list.append(name)
    
    for obj in obj_list:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[obj].select = True
        bpy.context.scene.objects.active = bpy.data.objects[obj]
        
        if mat_name in bpy.data.materials:
            bpy.context.active_object.active_material = bpy.data.materials[mat_name]
           
        else:                  
            blendfile_1 = join(library_path,'Shader_Library.blend')
            source_files = [blendfile_1] # liste des fichiers ou tu va chercher les materiaux
     
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
    
    # print('[BSL] Import - ', 'File:', blendfile, 'Material:', material, 'Library:', BSL_shader_library, 'Script:', BSL_import_script)
    
    sub = subprocess.Popen([bpy.app.binary_path, BSL_shader_library, '-b', '--python', BSL_import_script, blendfile, material])
    sub.wait()
    
    
class ImportIntoBSL(bpy.types.Operator):
    bl_idname = "material.import_into_bsl"
    bl_label = "Add Material to BSL"
    bl_description = "Import the current material into BSL - Needs a saved file to work"
    bl_options = {"REGISTER", "INTERNAL"}
    
    @classmethod
    def poll(cls, context):
        object = bpy.context.active_object.name
        return bpy.data.objects[object].active_material
      
    def execute(self, context):
        
        import_materials_in_library()
        
        library_path = os.path.dirname(__file__)
        material = bpy.context.object.active_material.name # a faire avant lancement subprocess, qui n'y aura plus acces (au context du fichier courant)
        
        context.window_manager.is_generating_preview = True
        
        #bpy.utils.previews.remove(preview_collections["main"])
        subprocess.Popen([bpy.app.binary_path, join(library_path, 'Shader_Library.blend'), '-b', '--python', join(library_path, 'import.py'), material])
        
        context.window_manager.is_generating_preview = False
        
        #bpy.ops.material.update_thumbnails() ### A modifier (modal ?) pour qu'il attende la fin de la generation, sans etre bloquant
        
        return {"FINISHED"}

        
class DeleteUnusedMaterials(bpy.types.Operator):
    bl_idname = "material.delete_unused_materials"
    bl_label = "Delete Unused Materials"
    bl_description = ""
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


class RemoveMaterialFromBML(bpy.types.Operator):
    bl_idname = "material.remove_material_from_bml"
    bl_label = "Remove material from BML"
    bl_description = "Remove selected material from your library"
    bl_options = {"REGISTER", "INTERNAL"}
    
    @classmethod
    def poll(cls, context):
        object = bpy.context.active_object.name
        return bpy.data.objects[object].active_material
    
    def execute(self, context):
        remove_material_from_library()
        
        return{"FINISHED"}
    
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
    
    