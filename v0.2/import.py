import bpy
import os
from os.path import join
import subprocess
import sys
from bpy.types import WindowManager
from bpy.props import EnumProperty
import bpy.utils.previews

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
    return enum_previews_from_directory_items()

def register_pcoll_preview():
    wm = bpy.context.window_manager
    

    global preview_collections
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
        
    WindowManager.my_previews = EnumProperty( # Nom à changer - pas clair, trop de preview dans les noms
            items=get_enum_previews,
            update=import_materials_from_files)
    
    pcoll = bpy.utils.previews.new() # pcoll pour preview collection
    pcoll.my_previews_dir = ""
    pcoll.my_previews = ()
    
    preview_collections = {}
    preview_collections["main"] = pcoll

def generate_thumbnails(material, thumbnail_type):
    
    library_path = os.path.dirname(os.path.abspath(__file__))
    
    if thumbnail_type == "_Render_Model":
        thumbnail_directory = "Sphere"
    elif thumbnail_type == "_Cloth_Model":
        thumbnail_directory = "Cloth" 
    elif thumbnail_type == "_Light_Model":
        thumbnail_directory = "Softbox"
    """
    #### Mettre sécurité (else) sur valeur par défaut en cas d'erreur + print
    else:
        print()
    """
    
    BML_thumbnails_directory = join(library_path, 'Thumbnails', thumbnail_directory)
    BML_shader_library = join(library_path, 'Shader_Library.blend') # ou bpy.utils.resource_path('USER') + "scripts/addons/material_library"
    BML_generate_script = join(library_path, 'generate_thumbnails.py')

    print('[BSL] Generate Thumbnails - ', 'Directory:', BML_thumbnails_directory, 'Material:',material, 'Library:', BML_shader_library, 'Script:',BML_generate_script)

    sub = subprocess.Popen([bpy.app.binary_path, BML_shader_library, '-b', '--python', BML_generate_script, material, BML_thumbnails_directory, thumbnail_type])
    sub.wait()

if __name__ == '__main__':
    generate_thumbnails(sys.argv[5],sys.argv[6]) # matériaux, type de thumbnails
    