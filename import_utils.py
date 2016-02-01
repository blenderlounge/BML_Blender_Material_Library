# -*- coding: utf-8 -*-

'''
Copyright (C) 2015-2016 Lapineige, Pitiwazou, Pistiwique

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import bpy
import bmesh
import os
import subprocess
from os.path import join
from bpy.types import Operator



def apply_material(mat_name, assign_mat): # Called in the import_materials_from_files fonction
    ob = bpy.context.active_object

    if assign_mat:
        bpy.ops.object.material_slot_add()

    # Get material
    if bpy.data.materials.get(mat_name):
        mat = bpy.data.materials[mat_name]
    else:
        # create material
        mat = bpy.data.materials.new(name=mat_name)

    # Assign it to object
    if len(ob.data.materials):
        # assign to active material slot
        ob.active_material = mat
    else:
        # no slots
        ob.data.materials.append(mat)


#############################################
##            Import depuis BML           ###
#############################################

def import_materials_from_BML(self, context):
    # Bloque si appel depuis un script (réinitialisation,...)
    if context.window_manager.BML.preview_block_update:
        return

    library_path = os.path.dirname(__file__)
    SECTION = "Material" # on importe un materiau
    mat_name = bpy.data.window_managers["WinMan"].BML_previews.split(".jpeg")[0] # Get the name of material from the preview but without the extention file
    obj_name = bpy.context.active_object.name
    assign_mat = False

    if context.object.mode == 'EDIT':
        obj = bpy.context.object
        bm = bmesh.from_edit_mesh(obj.data)

        selected_face = [f for f in bm.faces if f.select] # Test if some faces are selected

        if selected_face:
            assign_mat = True

        bpy.ops.object.mode_set(mode='OBJECT')

        if mat_name in bpy.data.materials:
            if assign_mat:
                apply_material(mat_name, assign_mat)
            else:
                bpy.context.active_object.active_material = bpy.data.materials[mat_name]

        else:
            blendfile_1 = join(library_path,'Shader_Library.blend')
            source_files = [blendfile_1] # liste des fichiers ou tu va chercher les materiaux

            with bpy.data.libraries.load(blendfile_1) as (data_from, data_to):
                if data_from.materials:
                    directory = join(blendfile_1, SECTION)

                    bpy.ops.wm.append(filename=mat_name, directory=directory)

            apply_material(mat_name, assign_mat)

        bpy.data.objects[obj_name].select = True

        bpy.ops.object.mode_set(mode='EDIT')
        if assign_mat:
            bpy.ops.object.material_slot_assign()

    elif context.object.mode == 'OBJECT':
        assign_mat = False

        obj_list = [item.name for item in context.selected_objects]

        for obj in obj_list:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[obj].select = True
            bpy.context.scene.objects.active = bpy.data.objects[obj]

            if mat_name in bpy.data.materials:
                bpy.context.active_object.active_material = bpy.data.materials[mat_name]
                bpy.data.objects[obj].select = True
            else:
                blendfile_1 = join(library_path,'Shader_Library.blend')
                source_files = [blendfile_1] # liste des fichiers ou tu va chercher les materiaux

                with bpy.data.libraries.load(blendfile_1) as (data_from, data_to):
                    if data_from.materials:
                        directory = join(blendfile_1, SECTION)

                        bpy.ops.wm.append(filename=mat_name, directory=directory)

                apply_material(mat_name, assign_mat)
        for obj in obj_list:
            bpy.data.objects[obj].select = True


#############################################
##             Ajout dans BML             ###
#############################################


def add_materials_to_library():
    wm = bpy.context.window_manager
    library_path = os.path.dirname(os.path.abspath(__file__))
    addon_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    blendfile = join(library_path, 'BML_temp.blend')
    material = bpy.context.object.active_material.name

    bpy.ops.wm.save_as_mainfile(filepath = blendfile, copy = True)

    BML_shader_library = bpy.context.user_preferences.addons[addon_dir].preferences.library_blend_path_ui
    BML_import_script = join(library_path, 'add_in_library_from_external_file.py')

    print("[BML] Import - ", "File:", blendfile, "Material:", material, "Library:", BML_shader_library, "Script:", BML_import_script)

    sub = subprocess.Popen([bpy.app.binary_path, BML_shader_library, '-b', '--python', BML_import_script, blendfile, material, wm.preview_type[1:]])
    sub.wait()


def add_in_bml():

    add_materials_to_library()

    wm = bpy.context.window_manager

    material = bpy.context.object.active_material.name
    addon_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    library_path = os.path.dirname(os.path.abspath(__file__))
    BML_thumbnails_directory = join(library_path, 'Thumbnails', wm.preview_type[1:])
    BML_shader_library = bpy.context.user_preferences.addons[addon_dir].preferences.library_blend_path_ui
    BML_generate_script = join(library_path, 'generate_thumbnails.py')

    print("[BML] Generate Thumbnails - ", "Directory:", BML_thumbnails_directory, "Material:", [material], "Library:", BML_shader_library, "Script:",BML_generate_script)

    bpy.ops.view3d.bml_render_progression_update('INVOKE_DEFAULT')
    with open( join(library_path,'Render_count.txt') , 'w') as render_count:
        render_count.write('Render Total: %s' % (1)) # Ne marche pas sur meme fichier que la sortie blender - pourquoi ?
    with open( join(library_path,'Render_output.txt') , 'wb') as render_log:
        sub = subprocess.Popen([bpy.app.binary_path, BML_shader_library, '-b', '--python', BML_generate_script, material, wm.preview_type[1:]], stdout=render_log, stderr=render_log)


def rename_mat_in_blm():

    material = bpy.data.window_managers["WinMan"].BML_previews.split(".jpeg")[0]
    library_path = os.path.dirname(os.path.abspath(__file__))
    wm = bpy.context.window_manager
    BML_render_type = wm.preview_type
    new_name = wm.BML_new_name

    list_files = os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Cloth')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Softbox')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Sphere')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Hair'))
    thumbnails_directory_list = [file for file in list_files if file.endswith('.jpeg') or file.endswith('.jpg')]

    BML_thumbnails_directory = join(library_path, 'Thumbnails', BML_render_type[1:])
    BML_shader_library = bpy.context.user_preferences.addons['BML'].preferences.library_blend_path_ui
    BML_rename_script = join(library_path, 'rename_material_in_library.py')

    print('[BML] Renaming material: ', material, 'To: ', new_name, 'With script:', BML_rename_script)

    #os.remove(join(BML_thumbnails_directory, material + ".jpeg")) # Gestion orphelins va le faire tout seul

    sub = subprocess.Popen([bpy.app.binary_path, BML_shader_library, '-b', '--python', BML_rename_script, material, new_name, BML_render_type])
    sub.wait()

    wm.BML_new_name = ""