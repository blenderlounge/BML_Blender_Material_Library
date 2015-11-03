# -*- coding: utf-8 -*-

import bpy
import os
import subprocess
from os.path import join
from os import listdir
from bpy.types import Operator
from . bml_preview_utils import register_BML_pcoll_preview
from . bml_import_utils import add_in_bml



class AddInBMLcontainer(Operator):
    bl_idname = "material.add_in_bml_container"
    bl_label = "Add material in the BML"
    bl_description = "Add the current material in the BML"
    bl_options = {'REGISTER'}
    
    def is_thumbnails_updated(self):
        list_files = os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Cloth')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Softbox')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Sphere')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Hair'))
        self.thumbs_list = [file for file in list_files if file.endswith('.jpeg') or file.endswith('.jpg')]
        
        return self.thumbs_list != self.thumbnails_directory_list

    def modal(self, context, event):
        
        if self.is_thumbnails_updated(): # on attends un changement dans le dossier des miniatures
            self.report({'INFO'}, "Thumbnails render done - Updating preview...") # Pas visible normalement, car update très rapide
            
            bpy.ops.material.update_thumbnails()
            
            self.report(
                {'INFO'}, "Thumbnails updated. Created: {0} - Orphaned: {1}".format(
                len(self.thumbs_list) - len(self.thumbnails_directory_list), # attention plus valable en cas de suppression antérieure au calcul
                'TODO')
                       )
            
            context.window_manager.is_generating_preview = False
            return {'FINISHED'}
        
        else:
            return {'PASS_THROUGH'}

    def invoke(self, context, event):
        
        # génération de la liste des miniatures depuis tout les dossiers Thumbnails
        list_files = os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Cloth')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Softbox')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Sphere')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Hair'))
        self.thumbnails_directory_list = [file for file in list_files if file.endswith('.jpeg') or file.endswith('.jpg')] # il faut la réinitialiser à chaque lancement, en cas de mofication # filtrage idem précédent
        
        
        #print('LIST:', self.thumbnails_directory_list, 'Length:', len(thumbnails_directory_list))

        self.report({'INFO'}, "Thumbnails Rendering started...")
        add_in_bml() # executé la première fois uniquement

        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}
    
    
class UpdateThumbnails(bpy.types.Operator):
    bl_idname = "material.update_thumbnails"
    bl_label = "Update Thumbnails"
    bl_description = "(Re)generate thumbnails images. May take a while"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        
        register_BML_pcoll_preview()
        self.report({'INFO'}, "Thumbnails and preview updated") # marche que si appel depuis l'UI

        return {'FINISHED'}
    
    
class DeleteUnusedMaterials(Operator): 
    bl_idname = "material.delete_unused_materials"
    bl_label = "Delete Unused Materials"
    bl_description = ""
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        materials = bpy.data.materials

        for material in bpy.data.materials:
            if not material.users:
                materials.remove(material)

        return {'FINISHED'}
    
    
class RemoveMaterialFromBML(Operator):
    bl_idname = "material.remove_material_from_bml"
    bl_label = "Remove material from BML"
    bl_description = "Remove selected material from your library"
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        object = bpy.context.active_object.name
        return bpy.data.objects[object].active_material

    def execute(self, context):        
        wm = bpy.context.window_manager

        if wm.preview_type == '_Sphere':
            thumbnail_type = 'Sphere'
        elif wm.preview_type == '_Cloth':
            thumbnail_type= 'Cloth'
        elif wm.preview_type == '_Softbox':
            thumbnail_type= 'Softbox'
        elif wm.preview_type == '_Hair':
            thumbnail_type= 'Hair'

        library_path = os.path.dirname(os.path.abspath(__file__))
        material = bpy.context.object.active_material.name
        
        BML_shader_library = join(library_path, 'Shader_Library.blend')
        BML_generate_script = join(library_path, 'remove_material_from_library.py')
        BML_thumbnails_directory = join(library_path, 'Thumbnails', thumbnail_type)
        thumbnail_remove = join(BML_thumbnails_directory, material + '.jpeg')

        sub = subprocess.Popen([bpy.app.binary_path, BML_shader_library, '-b', '--python', BML_generate_script, material])
        sub.wait()

        os.remove(thumbnail_remove)
        
        bpy.ops.material.update_thumbnails()
        self.report({'INFO'}, "Thumbnails updated. Removed: 1") # nombre à changer en cas de nettoyage multiple

        return {'FINISHED'}