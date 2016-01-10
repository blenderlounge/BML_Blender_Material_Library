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
import os
import subprocess
import blf
from os import listdir
from os.path import isdir, isfile, join, dirname
from bpy.types import Operator
from . preview_utils import register_BML_pcoll_preview
from . import_utils import add_in_bml, rename_mat_in_blm
from time import time

#############################################
##  Ajout de matériau dans la librairie   ###
#############################################

class AddInBMLcontainer(Operator):
    ''' Conteneur qui gère les ajouts de matériau, les conflits (renommage) '''
    bl_idname = "material.add_in_bml_container"
    bl_label = "Import active material into BML"
    bl_description = "Import active material into BML"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return context.object.active_material or not context.window_manager.BML.is_generating_preview

    def is_thumbnails_updated(self):
        list_files = os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Cloth')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Softbox')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Sphere')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Hair'))
        self.thumbs_list = [file for file in list_files if file.endswith('.jpeg') or file.endswith('.jpg')]

        return self.thumbs_list != self.thumbnails_directory_list

    def modal(self, context, event):
        wm = context.window_manager

        #### Popup
        if wm.BML_popup_alive: # tant que la popup est active, on attends
            return {'PASS_THROUGH'}
        elif not self.popup_down and not wm.BML_popup_alive:
            self.popup_down = True
            if wm.BML_replace_rename == 'replace':
                bpy.ops.material.remove_material_from_bml()
            elif wm.BML_replace_rename == 'rename' and wm.BML_new_name:
                context.object.active_material.name = wm.BML_new_name #### Pas top, il ne faudrait pas changer le nom du matériau courant > changement au niveau de la gestion du nom lors de l'ajout ? ### quoique c'est cohérent en cas d'ajout...

            self.report({'INFO'}, "Thumbnails Rendering started...") # Non affiché dans l'UI
            add_in_bml() # executé la première fois uniquement
            return {'PASS_THROUGH'}

        #### Update
        if self.is_thumbnails_updated(): # on attends un changement dans le dossier des miniatures
            self.report({'INFO'}, "Thumbnails render done - Updating preview...") # Pas visible normalement, car update très rapide

            bpy.ops.material.update_thumbnails('INVOKE_DEFAULT')

            self.report( {'INFO'}, "Thumbnails updated. Created: %d" % (len(self.thumbs_list) - len(self.thumbnails_directory_list)) )# attention plus valable en cas de suppression antérieure au calcul
            wm.BML_new_name = '' # remets le nom à '' pour éviter le changement dans l'UI
            wm.BML.is_generating_preview = False
            return {'FINISHED'}
        else:
            return {'PASS_THROUGH'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.BML.is_generating_preview = True

        # génération de la liste des miniatures depuis tout les dossiers Thumbnails
        # [join( join(os.path.dirname(__file__), 'Thumbnails') , path) for path in os.listdir(join(os.path.dirname(__file__), 'Thumbnails'))] # > liste des dossiers dans lequel fouiller # ! au .directory (évité en test startwith('.') et éventuel autres fichiers (icône en cas de manque, etc))
        list_files = os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Cloth')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Softbox')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Sphere')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Hair'))
        self.thumbnails_directory_list = [file for file in list_files if file.endswith('.jpeg')] # il faut la réinitialiser à chaque lancement, en cas de mofication # filtrage idem précédent

        #print('LIST:', self.thumbnails_directory_list, 'Length:', len(thumbnails_directory_list))

        wm.BML_popup_alive = False # utile si on n'a pas besoin de la popup
        self.popup_down = False # vérifie que la popup vient d'être fermée
        if context.object.active_material.name + ".jpeg" in self.thumbnails_directory_list:
            bpy.ops.material.bml_rename_popup('INVOKE_DEFAULT')
        else:
            wm.BML_new_name = ''

        wm.modal_handler_add(self)

        return {'RUNNING_MODAL'}


###################
# Handler Rendu ###
###################


def draw_callback_px(self, context):
    blf.position(0, context.user_preferences.system.dpi/3.54, context.area.height-context.user_preferences.system.dpi*.84, 0) # 92/26 ~ 3.54 et 50/92 ~ 0.84 >>> aligne sous User Persp
    blf.size(0, 11, context.user_preferences.system.dpi)

    BML = context.window_manager.BML
    progress = BML.render_progression
    render_nb = BML.render_nb
    max_render_nb = BML.max_render_nb
    render_status = BML.render_status
    if render_status:
        blf.draw(0, 'Render %s/%s - Progression: %s' % (render_nb, max_render_nb, render_status) )
    elif progress:
        blf.draw(0, 'Render %s/%s - Progression: %s%%' % (render_nb, max_render_nb, progress*10))
        #blf.draw(0, 'Render %s/%s - Progression: %s%% [%s>%s]' % (render_nb, max_render_nb, progress*10, '='*progress, ' '*(10-progress) ) ) # ATTENTION nombre de blanc incorrect
    elif render_nb < max_render_nb:
        blf.draw(0, 'Render %s/%s' % (render_nb , max_render_nb))
    elif BML.debug_ui:
        blf.draw(0,'DEBUG - Progress: %d | Status: %s' % (progress*10, render_status))

class RenderProgressionHandler(bpy.types.Operator):
    """ TODO """
    bl_idname = "view3d.bml_render_progression_handler"
    bl_label = "Render Progression Handler"
    bl_options = {'INTERNAL'}

    previous = -1

    def modal(self, context, event):
        wm =context.window_manager
        context.area.tag_redraw()# TODO delete
        if wm.BML.render_progression and wm.BML.render_progression != self.previous:
            self.previous = wm.BML.render_progression
            context.area.tag_redraw()
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, (self, context), 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

class RenderProgressionUpdate(bpy.types.Operator): #### TODO penser mécanisme de coupure auto à la fin du rendu > handler ?
    """ TODO """
    bl_idname = "view3d.bml_render_progression_update"
    bl_label = "Render Progression Update"
    bl_options = {'INTERNAL'}

    def modal(self, context, event):
        wm = context.window_manager

        if not isfile(join(dirname(__file__),'Render_output.txt')): # Vérification trop rapide, fichier texte pas encore créé au moment du lancement.
            return {'PASS_THROUGH'}

        if isfile(join(dirname(__file__), 'Render_count.txt')): # TODO à placer dans le isfile précédent > une seule occurence
                with open( join(dirname(__file__), 'Render_count.txt'), 'r') as log:
                    line = log.readlines()[0]
                    if 'Render Total: ' in line: # détecté seulement au premier coup
                        wm.BML.max_render_nb = int(line.split('Render Total: ')[1])

        self.inspect_render_log(context)

        if wm.BML.render_progression == 10: # TODO fusionner avec is file précédent, afin d'éviter deux lectures.
            if isfile(join(dirname(__file__), 'Render_count.txt')):
                with open( join(dirname(__file__), 'Render_count.txt'), 'r') as log:
                        line = log.readlines()[-1] # ATTENTION ligne vide
                        new_rdr_nb = int(line[14:].split(' -')[0]) # len('Render number: ')-1 = 15
                        if wm.BML.render_nb != new_rdr_nb:
                            #wm.BML.render_material = line.split(' - ')[1].split('Material: ')[0] TODO afficher nom matériau
                            wm.BML.render_nb = new_rdr_nb
                            wm.BML.render_progression = 0
                            wm.BML.render_status = ''
                            if wm.BML.render_nb == wm.BML.max_render_nb:
                                wm.BML.render_nb = 1
                                wm.BML.max_render_nb = 1
                                wm.BML.handler_active = False
                                return {'FINISHED'}
            #else: ### y'a des cas ou on l'utilise pas ?
                #wm.BML.render_progression,wm.BML.render_nb,wm.BML.max_render_nb = 0,1,1
                #wm.BML.render_status = ''
                #wm.BML.handler_active = False
                #return {'FINISHED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        wm = context.window_manager

        # Handler pour la progression du rendu
        if not wm.BML.handler_active:
            wm.BML.handler_active = True
            bpy.ops.view3d.bml_render_progression_handler('INVOKE_DEFAULT')

        wm.BML.render_progression,wm.BML.render_nb,wm.BML.max_render_nb = 0,1,1
        wm.BML.render_status = ''

        self.finish_time = 0

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def inspect_render_log(self, context):
        wm = context.window_manager
        with open( join(dirname(__file__),'Render_output.txt'), 'r') as log:
            lines = log.readlines()
            lines.reverse()
            if not lines: # Si rendu pas encore lancé (création du fichier texte)
                return
            for line in lines:
                if 'Finished' in line:
                    wm.BML.render_progression = 10
                    break
                elif 'Path Tracing Tile 1/1' in line and not '0/' in line: # not 0/ pour éviter la ligne sans samples calculés, et le progression à 0% ### TODO adapter au nombre de tile
                    wm.BML.render_progression = round(
                        (
                            int(line.split('Sample ')[1].split('/')[0]) /
                            int(line.split('Sample ')[1].split('/')[1])
                         )*10
                        , 0) # Nombre de samples calculés / total > rapporté à un entier de 0 à 10
                    break
                elif 'Synchronizing' in line:
                    wm.BML.render_progression = 1 # valide les conditions pour éviter une coupure # 10% car petite partie du temps > valeur arbitraire TODO trouver meilleure estimation
                    wm.BML.render_status = 'Initializing' # Si besoin du détail plus tard # 'Updating' + line.split('Updating')[1].split('/')[1] # Coupure avec 'Updating' sans espace final, espace intégré dans la partie [1]
                    break
                elif 'Updating' in line:
                    wm.BML.render_progression = 2 # valide les conditions pour éviter une coupure #  20% car partie du temps significative > valeur arbitraire TODO trouver meilleure estimation
                    wm.BML.render_status = 'Computing BVH' # Si besoin du détail plus tard # 'Updating' + line.split('Updating')[1].split('/')[1] # Coupure avec 'Updating' sans espace final, espace intégré dans la partie [1]
                    break

#############################################
##           Changement de nom            ###
#############################################

class BML_RenamePopup(Operator):
    ''' Popup de gestion de conflits de nom: renommage / remplacement '''
    bl_idname = "material.bml_rename_popup"
    bl_label = "Import active material into BML"
    bl_options = {"INTERNAL"}

    bpy.types.WindowManager.BML_new_name = bpy.props.StringProperty(default="")
    bpy.types.WindowManager.BML_popup_alive = bpy.props.BoolProperty(default=False)

    def execute(self, context):
        wm = context.window_manager

        list_files = os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Cloth')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Softbox')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Sphere')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Hair'))

        self.thumbnails_directory_list = [file for file in list_files if file.endswith('.jpeg')]

        if wm.BML_replace_rename == 'rename' and (not wm.BML_new_name or wm.BML_new_name + ".jpeg" in self.thumbnails_directory_list):
            bpy.ops.material.bml_rename_popup('INVOKE_DEFAULT')
        else:
            wm.BML_popup_alive = False
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.BML_popup_alive = True

        list_files = os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Cloth')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Softbox')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Sphere')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Hair'))
        self.thumbnails_directory_list = [file for file in list_files if file.endswith('.jpeg')]

        if context.object.active_material.name + ".jpeg" in self.thumbnails_directory_list:
            context.window_manager.BML_new_name = context.material.name + '.001' # TODO gérer numéro
            context.window_manager.BML_replace_rename = 'rename'
            dpi_value = bpy.context.user_preferences.system.dpi
            return context.window_manager.invoke_props_dialog(self, width=dpi_value*5, height=100)
        else:
            context.window_manager.BML_popup_alive = False
            return {'FINISHED'}

    def draw(self, context):
        wm = context.window_manager
        library_path = os.path.dirname(os.path.abspath(__file__))
        material = bpy.context.object.active_material.name
        thumbnail_folder = [f for f in listdir(join(library_path, 'Thumbnails')) if isfile(join(library_path, 'Thumbnails', f, material + ".jpeg"))][0]

        layout = self.layout

        layout.label('" ' + context.object.active_material.name + ' " already exist as a " ' + ''.join(thumbnail_folder) + ' " preview type' , icon='ERROR')

        row = layout.row(align=True)
        row.prop(wm, "BML_replace_rename", text=" ", expand=True)


        if wm.BML_replace_rename == 'rename':
            row = layout.row()
            row.active = wm.BML_replace_rename == 'rename' #### Ne fonctionne pas ?
            row.prop(wm, "BML_new_name", text="New name")

class ChangeNameInBLM(Operator):
    bl_idname = "material.change_name_in_blm"
    bl_label = "Rename BML's material"
    bl_description = "Change the active preview's material's name in the BLM'"
    bl_options = {"REGISTER","INTERNAL"}

    def is_thumbnails_updated(self):
        list_files = os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Cloth')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Softbox')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Sphere')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Hair'))
        self.thumbs_list = [file for file in list_files if file.endswith('.jpeg') or file.endswith('.jpg')]

        return self.thumbs_list != self.thumbnails_directory_list

    def modal(self, context, event):

        if self.is_thumbnails_updated(): # on attends un changement dans le dossier des miniatures

            self.report(
                {'INFO'}, 'Thumbnails updated. Created: {0} - Orphaned: {1}'.format(
                len(self.thumbs_list) - len(self.thumbnails_directory_list), # attention plus valable en cas de suppression antérieure au calcul
                'TODO')
            )

            context.window_manager.BML.is_generating_preview = False
            return {'FINISHED'}

        else:
            return {'PASS_THROUGH'}

    def invoke(self, context, event):

        # génération de la liste des miniatures
        list_files = os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Cloth')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Softbox')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Sphere')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Hair'))
        self.thumbnails_directory_list = [file for file in list_files if file.endswith('.jpeg') or file.endswith('.jpg')] # il faut la réinitialiser é chaque lancement, en cas de mofication # filtrage idem précédent


        #print('LIST:', self.thumbnails_directory_list, 'Length:', len(thumbnails_directory_list))

        rename_mat_in_blm() # executé la première fois uniquement
        bpy.ops.view3d.bml_render_progression_update('INVOKE_DEFAULT') # Mets à jour le handler
        bpy.ops.material.update_thumbnails('INVOKE_DEFAULT')

        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}

#############################################
##               Mise à jour              ###
#############################################

class UpdateThumbnails(Operator): ####### ATTENTION Bloquer le rendu en cas d'ajout en cours (context.window_manager.BML.is_generating_preview = True), sans bloquer l'update de la preview TODO
    bl_idname = "material.update_thumbnails"
    bl_label = "Update Thumbnails"
    bl_description = "(Re)generate thumbnails images. May take a while"
    bl_options = {'REGISTER', 'INTERNAL'}

    def is_thumbnails_updated(self):
        self.thumbs_dir_list = [file for file in os.listdir(join(os.path.dirname(__file__), 'Thumbnails'))] # liste tout les fichiers du dossier
        return 'generate_thumbs_placeholder.txt' not in self.thumbs_dir_list

    def modal(self, context, event):
        ##### AFFICHER REPORT avec génération thumbnails - 2 propriétés pour éa

        if self.is_thumbnails_updated(): # on attends un changement dans le dossier des miniatures
            register_BML_pcoll_preview()
            self.report({'INFO'}, "Thumbnails and preview updated") # marche que si appel depuis l'UI
            return {'FINISHED'}
        else:
            return {'PASS_THROUGH'}

    def invoke(self, context, event):

        #print('LIST:', self.thumbnails_directory_list, 'Length:', len(thumbnails_directory_list))

        library_path = os.path.dirname(os.path.abspath(__file__))
        BML_shader_library = context.user_preferences.addons['BML'].preferences.library_blend_path
        update_script = join(library_path, 'update_thumbnails.py')

        bpy.ops.view3d.bml_render_progression_update('INVOKE_DEFAULT') # Mets à jour le handler
        with open(join(os.path.dirname(os.path.abspath(__file__)),'Thumbnails', 'generate_thumbs_placeholder.txt'), 'w'): # fichier existant pendant toute la mise à jour, on détectera sa suppression
            sub = subprocess.Popen([bpy.app.binary_path, BML_shader_library, '-b', '--python', update_script]) #### Attention, un seul changement et ça coupe... TODO vérifier réponse du process

        self.report({'INFO'}, "Thumbnails Rendering started...")

        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}

#############################################
##              Suppression               ###
#############################################

class RemoveMaterialFromBML(Operator):
    ''' Supprimer un matériau de la librairie '''
    bl_idname = "material.remove_material_from_bml"
    bl_label = "Remove material from BML"
    bl_description = "Remove selected material from your library"
    bl_options = {'REGISTER', 'INTERNAL'}

    is_invoke_call = False

    @classmethod
    def poll(cls, context):
        return context.object.active_material or not context.window_manager.BML.is_generating_preview

    def execute(self, context):
        wm = bpy.context.window_manager

        wm.BML.is_generating_preview = True

        if self.is_invoke_call:
            material = wm.BML_previews.split('.jpeg')[0] #### ATTENTION '.jpeg' déjà inclut dans le nom du matériau
        else:
            material = context.material.name
        self.is_invoke_call = False # à remettre à la valeur par défaut de suite, en cas de nouvel appel

        thumbnail_type = wm.preview_type

        library_path = os.path.dirname(os.path.abspath(__file__))

        BML_shader_library = context.user_preferences.addons['BML'].preferences.library_blend_path
        BML_remove_script = join(library_path, 'remove_material_from_library.py')
        thumbnail_folder = [f for f in listdir(join(library_path, 'Thumbnails')) if isfile(join(library_path, 'Thumbnails', f, material + ".jpeg"))][0]
        BML_thumbnails_directory = join(library_path, 'Thumbnails', thumbnail_folder)
        thumbnail_remove = join(BML_thumbnails_directory, material + '.jpeg')

        print('[BML] REMOVE from:' , thumbnail_folder, 'Material:', material + '.jpeg')

        os.remove(thumbnail_remove)

        sub = subprocess.Popen([bpy.app.binary_path, BML_shader_library, '-b', '--python', BML_remove_script, material])
        sub.wait() # important avant update, sinon pas de changement

        bpy.ops.material.update_thumbnails('INVOKE_DEFAULT')
        self.report({'INFO'}, "Thumbnails updated. Removed: 1") # nombre à changer en cas de nettoyage multiple # report inefficace si opérateur enfant
        #wm.BML.preview_block_update = True
        register_BML_pcoll_preview()
        wm.BML.preview_block_update = False

        wm.BML.is_generating_preview = False
        return {'FINISHED'}

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout
        material = bpy.data.window_managers["WinMan"].BML_previews.split(".jpeg")[0]

        col = layout.column()
        col.label("Remove " + '" ' + material + ' "', icon='ERROR')
        col.label("     It will not longer exist in BML")

    def invoke(self, context, event):
        self.is_invoke_call = True
        dpi_value = bpy.context.user_preferences.system.dpi
        return context.window_manager.invoke_props_dialog(self, width=dpi_value*3, height=100)

class DeleteUnusedMaterials(Operator):
    ''' Détruire les matériaux inutilisés dans le fichier (0 users) '''
    bl_idname = "material.delete_unused_materials"
    bl_label = "Delete Unused Materials"
    bl_description = ""
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        materials = bpy.data.materials

        for material in bpy.data.materials:
            if not material.users:
                materials.remove(material)

        return {'FINISHED'}