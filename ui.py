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
from os import listdir
from os.path import join
from bpy.types import Panel
from . operators import(DeleteUnusedMaterials,
                        RemoveMaterialFromBML)


#####################################################
# VIEW 3D
#####################################################

class VIEW3D_PT_view_3d_bml(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Blender Material Library"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        if bpy.context.selected_objects:
            layout.prop(wm, "preview_type")
            if wm.BML_previews:
                layout.template_icon_view(wm, "BML_previews")
            else:
                layout.label('No thumbnail available', icon='INFO')
                layout.label('Please add a material / update the thumbnails list')
            layout.operator("object.select_linked", icon='RESTRICT_SELECT_OFF').type='MATERIAL'
        else:
            layout.label("No mesh selected", icon='Info')


class VIEW3D_PT_tools_bml(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "BML"
    bl_label = "Blender Material Library"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        if bpy.context.selected_objects:
            layout.prop(wm, "preview_type")
            if wm.BML_previews:
                layout.template_icon_view(wm, "BML_previews")
            else:
                layout.label('No thumbnail available - Please add a material / update', icon='INFO')
            layout.operator("object.select_linked", icon='RESTRICT_SELECT_OFF').type='MATERIAL'
        else:
            layout.label("No mesh selected", icon='Info')


class view3d_header_preview_bml(bpy.types.Menu):
    bl_idname = "material.view3d_header_preview"
    bl_label = "BML preview"
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        if bpy.context.selected_objects:
            if wm.BML_previews:
                layout.template_icon_view(wm, "BML_previews")
            else:
                layout.label('No thumbnail available - Please add a material / update', icon='INFO')
        else:
            layout.label("No mesh selected", icon='Info')

def VIEW3D_HT_header_bml_preview(self, context):
    layout = self.layout
    layout.menu("material.view3d_header_preview", text=" BML", icon='MATERIAL')



#####################################################
# NODE EDITOR
#####################################################

class NODE_PT_tools_bml(Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = "BML"
    bl_label = "Blender Material Library"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        object = bpy.context.active_object.name

        if bpy.context.selected_objects:
            layout.prop(wm, "preview_type", text="Preview type")
            if bpy.data.objects[object].active_material:
                row = layout.row(align=True)
                # row.operator("material.add_in_bml_container", text="Add", icon='APPEND_BLEND')
                row.operator("material.add_in_bml_container", text="Add / Replace", icon='APPEND_BLEND')
                row.operator("material.remove_material_from_bml", text="Remove", icon='X')
                row.operator("material.update_thumbnails", text="", icon='FILE_REFRESH')
                if wm.BML_previews:
                    layout.template_icon_view(wm, "BML_previews")
                else:
                    layout.label('No thumbnail available - Please add a material / update', icon='INFO')
        else:
            layout.label("No mesh selected", icon='Info')


class NODE_PT_ui_bml(Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "Blender Material Library"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        object = bpy.context.active_object.name

        if bpy.context.selected_objects:
            layout.prop(wm, "preview_type", text="Preview type")
            if bpy.data.objects[object].active_material:
                row = layout.row(align=True)
                # row.operator("material.add_in_bml_container", text="Add", icon='APPEND_BLEND')
                row.operator("material.add_in_bml_container", text="Add / Replace", icon='APPEND_BLEND')
                row.operator("material.remove_material_from_bml", text="Remove", icon='X')
                row.operator("material.update_thumbnails", text="", icon='FILE_REFRESH')
                if wm.BML_previews:
                    layout.template_icon_view(wm, "BML_previews")
                else:
                    layout.label('No thumbnail available - Please add a material / update', icon='INFO')
        else:
            layout.label("No mesh selected", icon='Info')


class node_header_preview_bml(bpy.types.Menu):
    bl_idname = "material.node_header_preview"
    bl_label = "BML preview"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        if bpy.context.selected_objects:
            if wm.BML_previews:
                layout.template_icon_view(wm, "BML_previews")
            else:
                layout.label('No thumbnail available - Please add a material / update', icon='INFO')
        else:
            layout.label("No mesh selected", icon='Info')

def NODE_HT_header_bml_preview(self, context):
    layout = self.layout
    wm = context.window_manager

    if bpy.context.selected_objects:
        layout.menu("material.node_header_preview", text=" BML", icon='MATERIAL')
        layout.prop(wm, "preview_type", text="Preview type ")
    else:
        layout.label("No mesh selected", icon='Info')


#####################################################
# PROPERTIES_MATERIAL
#####################################################

class BML_MiscMenu(bpy.types.Menu):
    bl_label = "Other Operations"
    bl_idname = "MATERIAL_MT_bml_misc_menu"

    def draw(self, context):
        layout = self.layout
        #Select Linked
        layout.operator("object.select_linked", icon='RESTRICT_SELECT_OFF').type='MATERIAL'
        #Delete Unused
        layout.operator("material.delete_unused_materials", icon='MATERIAL_DATA')

class Cycles_PT_bml_panel(Panel):
    '''Blender Material Library preview'''
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_label = "Blender Material Library"
    bl_context = "material"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        object = bpy.context.active_object.name

        list_files = os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Cloth')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Softbox')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Sphere')) + os.listdir(join(os.path.dirname(__file__), 'Thumbnails', 'Hair'))
        thumbnails_directory_list = [file for file in list_files if file.endswith('.jpeg') or file.endswith('.jpg')]

        if bpy.context.selected_objects:
            layout.prop(wm, "preview_type", text="Preview type")
#            if bpy.data.objects[object].active_material:
#                row = layout.row(align=True)
#                row.operator("material.add_in_bml_container", text="Add / Replace", icon='APPEND_BLEND')
#                row.operator("material.remove_material_from_bml", text="Remove", icon='X')
#                row.operator("material.update_thumbnails", text="", icon='FILE_REFRESH')


            row = layout.split(percentage=.85)
            col = row.column()
            col.scale_y = 1 # TODO préférence choix scale

            if wm.BML_previews:
                col.template_icon_view(wm, "BML_previews")
            else:
                col.label('No thumbnail available - Please add a material / update', icon='INFO')

            if bpy.data.objects[object].active_material:
                col = row.column(align=True)
                col.operator("material.add_in_bml_container", text='', icon='ZOOMIN')
                col.operator("material.remove_material_from_bml", text='', icon='ZOOMOUT')
                col.operator("material.update_thumbnails", text='', icon='FILE_REFRESH')

                col.prop(wm.BML, "rename_material", text='R', toggle=True)
                #do Not Import
                if wm.BML.preview_block_update:
                    col.prop(wm.BML, "preview_block_update", icon='LOCKED', icon_only=True)
                else:
                    col.prop(wm.BML, "preview_block_update", icon='UNLOCKED', icon_only=True)
                col.menu('MATERIAL_MT_bml_misc_menu', icon='DOWNARROW_HLT')

                # Rename
                if wm.BML.rename_material:
                    row = layout.row(align=True)
                    row.label("Rename Material")
                    row.prop(wm, "BML_new_name", text='')
                    row.enabled = not wm.BML_previews == '' # or [Prop]  TODO en cours d'action

                    if wm.BML_new_name + ".jpeg" in thumbnails_directory_list:
                        layout.label('" ' + wm.BML_new_name + ' " already exist', icon='ERROR')
                    else:
                        row.operator("material.change_name_in_blm", text="", icon='FILE_TICK')

                if wm.BML.render_progression:
                    layout.label(text='Render: %s/%s - Progress: %d%%' %(wm.BML.render_nb, wm.BML.max_render_nb, wm.BML.render_progression*10))
                elif wm.BML.render_nb < wm.BML.max_render_nb:
                    layout.label(text='Render: %s/%s' %(wm.BML.render_nb, wm.BML.max_render_nb))

#            row = layout.row(align=True)
#            row.label("Rename BML's material")
#            row.prop(wm, "BML_new_name", text='')
#            row.enabled = not wm.BML_previews == '' # or [Prop]  TODO en cours d'action

#            if wm.BML_new_name + ".jpeg" in thumbnails_directory_list:
#                layout.label('" ' + wm.BML_new_name + ' " already exist', icon='ERROR')
#            else:
#                row.operator("material.change_name_in_blm", text="", icon='FILE_TICK')
#            layout.operator("material.delete_unused_materials",text="Delete unused materials")
#            layout.operator("object.select_linked", icon='RESTRICT_SELECT_OFF').type='MATERIAL'
        else:
            layout.label("No mesh selected", icon='Info')

        # ### DEBUG
        if wm.BML.debug_ui:
            layout.label(text='Debug Info')
            layout.prop(wm.BML, 'render_progression') # Handler, progression du rendu
            layout.prop(wm.BML, 'render_status') # Handler, statut du rendu
            layout.prop(wm.BML, 'render_nb') # Handler, n° rendu courant
            layout.prop(wm.BML, 'max_render_nb') # Handler, nb de rendu à faire