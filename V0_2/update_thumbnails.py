import bpy
import os
from os.path import join
import subprocess

for line in bpy.data.texts["BML_material_list"].lines:
    if not line.body:
        continue

    material , BML_render_type = line.body.split(';')
    BML_render_type = '_' + BML_render_type

    library_path = os.path.dirname(__file__)
    BML_shader_library = join(library_path, 'Shader_Library.blend')
    BML_thumbnails_directory = join(library_path, 'Thumbnails', BML_render_type[1:])
    BML_generate_script = join(library_path, 'generate_thumbnails.py')


    list_files = os.listdir(join(library_path, 'Thumbnails', 'Cloth')) + os.listdir(join(library_path, 'Thumbnails', 'Softbox')) + os.listdir(join(library_path, 'Thumbnails', 'Sphere')) + os.listdir(join(library_path, 'Thumbnails', 'Hair'))
    if material in [file.split('.jpeg')[0] for file in list_files if file.endswith('.jpeg')]: # ajouter option pour forcer le recalcul
        continue

    sub = subprocess.Popen([bpy.app.binary_path, BML_shader_library, '-b', '--python', BML_generate_script, material, BML_thumbnails_directory, BML_render_type])
    sub.wait() # à désactiver (option ?) pour tout rendre en même temps



os.remove( join(os.path.dirname(os.path.abspath(__file__)), 'Thumbnails', 'generate_thumbs_placeholder.txt') )