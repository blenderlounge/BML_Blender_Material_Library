# -*- coding: utf-8 -*-

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
            layout.template_icon_view(wm, "BML_previews")
            layout.operator("object.select_linked", icon='RESTRICT_SELECT_OFF').type='MATERIAL'
        else:
            layout.label("No mesh selected", icon='ERROR')


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
            layout.template_icon_view(wm, "BML_previews")
            layout.operator("object.select_linked", icon='RESTRICT_SELECT_OFF').type='MATERIAL'
        else:
            layout.label("No mesh selected", icon='ERROR')


class view3d_header_preview_bml(bpy.types.Menu):
    bl_idname = "material.view3d_header_preview"
    bl_label = "BML preview"
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        if bpy.context.selected_objects:
            layout.template_icon_view(wm, "BML_previews")
        else:
            layout.label("No mesh selected", icon='ERROR')

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
                row.operator("material.init_import_into_bml", text="Add / Replace", icon='APPEND_BLEND')
                row.operator("material.remove_material_from_bml", text="Remove", icon='X')
                row.operator("material.update_thumbnails", text="", icon='FILE_REFRESH')
            layout.template_icon_view(wm, "BML_previews")
        else:
            layout.label("No mesh selected", icon='ERROR')


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
                row.operator("material.init_import_into_bml", text="Add / Replace", icon='APPEND_BLEND')
                row.operator("material.remove_material_from_bml", text="Remove", icon='X')
                row.operator("material.update_thumbnails", text="", icon='FILE_REFRESH')
            layout.template_icon_view(wm, "BML_previews")
        else:
            layout.label("No mesh selected", icon='ERROR')


class node_header_preview_bml(bpy.types.Menu):
    bl_idname = "material.node_header_preview"
    bl_label = "BML preview"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        if bpy.context.selected_objects:
            layout.template_icon_view(wm, "BML_previews")
        else:
            layout.label("No mesh selected", icon='ERROR')

def NODE_HT_header_bml_preview(self, context):
    layout = self.layout
    wm = context.window_manager

    if bpy.context.selected_objects:
        layout.menu("material.node_header_preview", text=" BML", icon='MATERIAL')
        layout.prop(wm, "preview_type", text="Preview type ")
    else:
        layout.label("No mesh selected", icon='ERROR')


#####################################################
# PROPERTIES_MATERIAL
#####################################################

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
            if bpy.data.objects[object].active_material:
                row = layout.row(align=True)
                # row.operator("material.add_in_bml_container", text="Add", icon='APPEND_BLEND')
                row.operator("material.init_import_into_bml", text="Add / Replace", icon='APPEND_BLEND')
                row.operator("material.remove_material_from_bml", text="Remove", icon='X')
                row.operator("material.update_thumbnails", text="", icon='FILE_REFRESH')
            layout.template_icon_view(wm, "BML_previews")
            row = layout.row(align=True)
            row.label("Rename BML's material")
            row.prop(wm, "new_name")
            if wm.new_name + ".jpeg" in thumbnails_directory_list:
                layout.label('" ' + wm.new_name + ' " already exist', icon='ERROR')
            else:
                row.operator("material.change_name_in_blm", text="", icon='FILE_TICK')
            layout.operator("material.delete_unused_materials",text="Delete unused materials")
            layout.operator("object.select_linked", icon='RESTRICT_SELECT_OFF').type='MATERIAL'
        else:
            layout.label("No mesh selected", icon='ERROR')