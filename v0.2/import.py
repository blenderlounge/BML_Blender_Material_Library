import bpy
import os
from os.path import join
import subprocess
import sys

# Copie des fonctions, a defaut d'import fonctionnel - a corriger si possible

def import_materials_from_files(self, context):
    
    library_path = os.path.dirname(__file__)   

    SECTION   = "Material" # on importe un materiau
    mat_name = (bpy.data.window_managers["WinMan"].my_previews.split("."))[0]
   
    if mat_name in bpy.data.materials:
        bpy.context.active_object.active_material = bpy.data.materials[mat_name]
       
    else:                  
        blendfile_1 = join(library_path,'Shader_Library.blend')
        source_files = [blendfile_1] # liste des fichiers ou tu va chercher les materiau
 
        with bpy.data.libraries.load(blendfile_1) as (data_from, data_to):
            if data_from.materials:                 
                directory = join(blendfile_1, SECTION)
               
                bpy.ops.wm.append(filename=mat_name, directory=directory)
       
        apply_material(mat_name)

def get_enum_previews(self, context):
    """EnumProperty callback"""
    
    return enum_previews_from_directory_items() 

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

def generate_preview(material):
    library_path = os.path.dirname(os.path.abspath(__file__))
    
    BSL_thumbnails_directory = join(library_path, 'Thumbnails')
    BSL_shader_library = join(library_path, 'Shader_Library.blend') # ou bpy.utils.resource_path('USER') + "scripts/addons/material_library"
    BSL_generate_script = join(library_path, 'generate_preview.py')
    
    #print('[BSL] Generate Preview - ', 'Directory:', BSL_thumbnails_directory, 'Material:',material, 'Library:', BSL_shader_library, 'Script:',BSL_generate_script)
    
    sub = subprocess.Popen([bpy.app.binary_path, BSL_shader_library, '-b', '--python', BSL_generate_script, material, BSL_thumbnails_directory])    
    sub.wait()

if __name__ == '__main__':
    generate_preview(sys.argv[5])

#library_path = os.path.dirname(__file__)   
#os.remove(join(library_path, "BSL_temp.blend"))
