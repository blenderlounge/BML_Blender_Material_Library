import bpy
import os
from os.path import join
import subprocess



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
    library_path = os.path.dirname(__file__) 
    bpy.ops.wm.save_mainfile(filepath = library_path + "\BSL_temp.blend")
    
    blendfile = library_path + "\BSL_temp.blend"
    material = bpy.context.object.active_material.name
    
    BSL_shader_directory = os.path.dirname(os.path.abspath(__file__))
    BSL_shader_library = join(BSL_shader_directory, 'Shader_Library.blend') # ou bpy.utils.resource_path('USER') + "scripts/addons/material_library"
    BSL_import_script = join(BSL_shader_directory, 'import_in_library_from_external_file.py')
    
    # print('File:', blendfile, 'Material:',material, 'Library:', BSL_shader_library, 'Script:',BSL_import_script)
    
    subprocess.Popen([bpy.app.binary_path, BSL_shader_library, '-b', '--python', BSL_import_script, blendfile, material])


class ImportIntoBSL(bpy.types.Operator):
    bl_idname = "material.import_into_bsl"
    bl_label = "Add Material to BSL"
    bl_description = "Import the current material into BSL - Needs a saved file to work"
    bl_options = {"REGISTER"}
    
    @classmethod
    def poll(cls, context):
        return bpy.context.object.active_material
      
    def execute(self, context):
        import_materials_in_library()        
        # problème sauvegarde (shader pas à jour, ...) > faire une copie du fichier, importer depuis copie, détruire copie
        
        return {"FINISHED"}
    

class DeleteUnusedMaterials(bpy.types.Operator):
    bl_idname = "material.delete_unused_materials"
    bl_label = "Delete Unused Materials"
    bl_description = ""
    bl_options = {"REGISTER"}
   
    @classmethod
    def poll(cls, context):
        return True
   
    def execute(self, context):
        materials = bpy.data.materials
 
        for material in bpy.data.materials:
            if not material.users:
                materials.remove(material)
       
        return {"FINISHED"}
