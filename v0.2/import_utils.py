# -*- coding: utf-8 -*-

import bpy
import bmesh
import os
import subprocess
from os import listdir
from os.path import isdir, isfile, join
from bpy.types import Operator

        #########################
        ####    FONCTIONS    ####
        #########################

def apply_material(mat_name, assign_mat):
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

def import_materials_from_files(self, context):

    library_path = os.path.dirname(__file__)

    SECTION   = "Material" # on importe un materiau
    mat_name = bpy.data.window_managers["WinMan"].BML_previews.split(".jpeg")[0]
    obj_list = []
    obj_name = bpy.context.active_object.name

    if context.object.mode == 'EDIT':
        selected_face = 0
        obj = bpy.context.object
        bm = bmesh.from_edit_mesh(obj.data)

        for f in bm.faces:
            if f.select:
                selected_face += 1
                
        assign_mat = False
        if selected_face != 0:
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

        for item in bpy.context.selected_objects:
            name = item.name
            obj_list.append(name)

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


def import_materials_in_library():
    library_path = os.path.dirname(os.path.abspath(__file__))

    blendfile = join(library_path, "BML_temp.blend")
    material = bpy.context.object.active_material.name

    bpy.ops.wm.save_as_mainfile(filepath = blendfile, copy=True)

    BML_shader_library = join(library_path, 'Shader_Library.blend') # ou bpy.utils.resource_path('USER') + "scripts/addons/material_library"
    BML_import_script = join(library_path, 'import_in_library_from_external_file.py')

    print('[BML] Import - ', 'File:', blendfile, 'Material:', material, 'Library:', BML_shader_library, 'Script:', BML_import_script)

    sub = subprocess.Popen([bpy.app.binary_path, BML_shader_library, '-b', '--python', BML_import_script, blendfile, material])
    sub.wait()

class ImportIntoBML(Operator):
    bl_idname = "material.import_into_bml"
    bl_label = "Add Material into BML"
    bl_description = "Import the current material into BML"
    bl_options = {"REGISTER","INTERNAL"}

    def execute(self, context): # on attends un changement dans le dossier des miniatures
        
        import_materials_in_library()
        
        material = bpy.context.object.active_material.name                    
        library_path = os.path.dirname(os.path.abspath(__file__))
        wm = bpy.context.window_manager  
        BML_render_type = wm.preview_type  
    
        if BML_render_type == "_Sphere":
            thumbnail_directory = "Sphere"
        elif BML_render_type == "_Cloth":
            thumbnail_directory = "Cloth" 
        elif BML_render_type == "_Softbox":
            thumbnail_directory = "Softbox"
        elif BML_render_type == "_Hair":
            thumbnail_directory = "Hair"
        else:
            thumbnail_directory = "Sphere"

        
        BML_thumbnails_directory = join(library_path, 'Thumbnails', thumbnail_directory)
        BML_shader_library = join(library_path, 'Shader_Library.blend') # ou bpy.utils.resource_path('USER') + "scripts/addons/material_library"
        BML_generate_script = join(library_path, 'generate_thumbnails.py')

        print('[BSL] Generate Thumbnails - ', 'Directory:', BML_thumbnails_directory, 'Material:',material, 'Library:', BML_shader_library, 'Script:',BML_generate_script)

        sub = subprocess.Popen([bpy.app.binary_path, BML_shader_library, '-b', '--python', BML_generate_script, material, BML_thumbnails_directory, BML_render_type])

        return {'FINISHED'}

class ImportIntoBMLcontainer(Operator):
    bl_idname = "material.import_into_bml_container"
    bl_label = "Add Material to BML"
    bl_description = "Import active material into BML"
    bl_options = {"REGISTER"}
    
    def is_thumbnails_updated(self):
        list_files = os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Cloth')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Softbox')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Sphere')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Hair'))
        self.thumbs_list = [file for file in list_files if file.endswith('.jpeg') or file.endswith('.jpg')]
        
        return self.thumbs_list != self.thumbnails_directory_list

    def modal(self, context, event):
        
        if self.is_thumbnails_updated(): # on attends un changement dans le dossier des miniatures
            self.report({'INFO'}, 'Thumbnails render done - Updating preview...') # Pas visible normalement, car update très rapide
            
            bpy.ops.material.update_thumbnails()
            
            self.report(
                {'INFO'}, 'Thumbnails updated. Created: {0} - Orphaned: {1}'.format(
                len(self.thumbs_list) - len(self.thumbnails_directory_list), # attention plus valable en cas de suppression antérieure au calcul
                'TODO')
            )
            
            context.window_manager.is_generating_preview = False
            return {'FINISHED'}
        
        else:
            return {'PASS_THROUGH'}

    def invoke(self, context, event):
        
        # génération de la liste des miniatures
        list_files = os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Cloth')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Softbox')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Sphere')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Hair'))
        self.thumbnails_directory_list = [file for file in list_files if file.endswith('.jpeg') or file.endswith('.jpg')] # il faut la réinitialiser à chaque lancement, en cas de mofication # filtrage idem précédent
        
        
        #print('LIST:', self.thumbnails_directory_list, 'Length:', len(thumbnails_directory_list))

        self.report({'INFO'}, 'Thumbnails Rendering started...')
        bpy.ops.material.import_into_bml() # executé la première fois uniquement

        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}

class DeleteUnusedMaterials(Operator): 
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


class RemoveMaterialFromBML(Operator):
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
        
        bpy.ops.material.update_thumbnails()
        self.report({'INFO'}, 'Thumbnails updated. Removed: 1') # nombre à changer en cas de nettoyage multiple

    def draw(self, context):
        wm = context.window_manager        
        layout = self.layout
        material = bpy.data.window_managers["WinMan"].BML_previews.split(".jpeg")[0]
        
        col = layout.column()
        col.label("Remove " + '" ' + material + ' "', icon='ERROR')
        col.label("     It will not longer exist in BML")
        
    def invoke(self, context, event):
        dpi_value = bpy.context.user_preferences.system.dpi
        return context.window_manager.invoke_props_dialog(self, width=dpi_value*3, height=100) 

        return{"FINISHED"}

def remove_material_from_library():
    wm = bpy.context.window_manager
    thumbnail_type = wm.preview_type

    library_path = os.path.dirname(os.path.abspath(__file__))
    material = bpy.data.window_managers["WinMan"].BML_previews.split(".jpeg")[0]
    
    BML_shader_library = join(library_path, 'Shader_Library.blend')
    BML_generate_script = join(library_path, 'remove_material_from_library.py')    
                     
    thumbnail_folder = [f for f in listdir(join(library_path, 'Thumbnails')) if isfile(join(library_path, 'Thumbnails', f, material + ".jpeg"))] 
    
    BML_thumbnails_directory = join(library_path, 'Thumbnails', ''.join(thumbnail_folder))
    thumbnail_remove = join(BML_thumbnails_directory, material + '.jpeg')
    
    os.remove(thumbnail_remove)
    
    sub = subprocess.Popen([bpy.app.binary_path, BML_shader_library, '-b', '--python', BML_generate_script, material])
    sub.wait()

    