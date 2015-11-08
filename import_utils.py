# -*- coding: utf-8 -*-

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
        

def import_materials_from_BML(self, context):
    library_path = os.path.dirname(__file__)
    SECTION   = "Material" # on importe un materiau
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


def add_materials_to_library():
    library_path = os.path.dirname(os.path.abspath(__file__))
    blendfile = join(library_path, 'BML_temp.blend')
    material = bpy.context.object.active_material.name
    
    bpy.ops.wm.save_mainfile(filepath = blendfile)

    BML_shader_library = join(library_path, 'Shader_Library.blend') # ou bpy.utils.resource_path('USER') + "scripts/addons/material_library"
    BML_import_script = join(library_path, 'add_in_library_from_external_file.py')

    print("[BML] Import - ", "File:", blendfile, "Material:", material, "Library:", BML_shader_library, "Script:", BML_import_script)    
        
    sub = subprocess.Popen([bpy.app.binary_path, BML_shader_library, '-b', '--python', BML_import_script, blendfile, material])
    sub.wait()


def add_in_bml():
        
    add_materials_to_library()
    
    material = bpy.context.object.active_material.name                    
    library_path = os.path.dirname(os.path.abspath(__file__))
    wm = bpy.context.window_manager  
    BML_render_type = wm.preview_type  
    
    BML_thumbnails_directory = join(library_path, 'Thumbnails', BML_render_type[1:])
    BML_shader_library = join(library_path, 'Shader_Library.blend') 
    BML_generate_script = join(library_path, 'generate_thumbnails.py')

    print("[BSL] Generate Thumbnails - ", "Directory:", BML_thumbnails_directory, "Material:",material, "Library:", BML_shader_library, "Script:",BML_generate_script)

    sub = subprocess.Popen([bpy.app.binary_path, BML_shader_library, '-b', '--python', BML_generate_script, material, BML_thumbnails_directory, BML_render_type])


def rename_mat_in_blm():
        
    material = bpy.data.window_managers["WinMan"].BML_previews.split(".jpeg")[0]                   
    library_path = os.path.dirname(os.path.abspath(__file__))
    wm = bpy.context.window_manager  
    BML_render_type = wm.preview_type 
    new_name = wm.new_name 
    
    list_files = os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Cloth')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Softbox')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Sphere')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Hair'))
    thumbnails_directory_list = [file for file in list_files if file.endswith('.jpeg') or file.endswith('.jpg')] 
      
    BML_thumbnails_directory = join(library_path, 'Thumbnails', BML_render_type[1:])
    BML_shader_library = join(library_path, 'Shader_Library.blend') # ou bpy.utils.resource_path('USER') + "scripts/addons/material_library"
    BML_generate_script = join(library_path, 'rename_material_in_library.py')

    print('[BSL] Generate Thumbnails - ', 'Directory:', BML_thumbnails_directory, 'Material:',material, 'Library:', BML_shader_library, 'Script:',BML_generate_script)
    
    os.remove(join(BML_thumbnails_directory, material + ".jpeg"))
    
    sub = subprocess.Popen([bpy.app.binary_path, BML_shader_library, '-b', '--python', BML_generate_script, material, BML_thumbnails_directory, BML_render_type, new_name])
    sub.wait()
    
    wm.new_name = ""