# -*- coding: utf-8 -*-

import bpy
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
        
        row = layout.row(align=True)
        if bpy.data.objects[object].active_material:
            row.menu("material.import_into_bml_container")# , icon='APPEND_BLEND') # icone à changer
            row.operator("material.import_into_bml_container", text="Add", icon='APPEND_BLEND')
            row.operator("object.material_slot_remove",text="Remove", icon='X')
            row.operator("material.update_thumbnails", text="", icon='FILE_REFRESH')
        if bpy.context.selected_objects:
            layout.prop(wm, "preview_type")         
            layout.template_icon_view(wm, "BML_previews")
        else:
            layout.label("No mesh selected", icon='ERROR')
        layout.operator("material.delete_unused_materials", icon='X')


class NODE_PT_ui_bml(Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "Blender Material Library"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        object = bpy.context.active_object.name
        
        row = layout.row(align=True)
        if bpy.data.objects[object].active_material:
            row.prop(wm, "preview_type", text="")
            row.operator("material.import_into_bml_container", text="Add", icon='APPEND_BLEND')
            row.operator("object.material_slot_remove",text="Remove", icon='X')
            row.operator("material.update_thumbnails", text="", icon='FILE_REFRESH')
        if bpy.context.selected_objects:
            layout.template_icon_view(wm, "BML_previews")
        else:
            layout.label("No mesh selected", icon='ERROR')
        layout.operator("material.delete_unused_materials",text="Delete unused materials", icon='X')


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
            
        if bpy.context.selected_objects:
            layout.prop(wm, "preview_type", text="Preview type")
            if bpy.data.objects[object].active_material:
                row = layout.row(align=True)
                row.operator("material.add_in_bml_container", text="Add", icon='APPEND_BLEND')
                row.operator("material.remove_material_from_bml", text="Remove", icon='X')
                row.operator("material.update_thumbnails", text="", icon='FILE_REFRESH')         
            layout.template_icon_view(wm, "BML_previews")
            layout.operator("material.delete_unused_materials",text="Delete unused materials")
            layout.operator("object.select_linked", icon='RESTRICT_SELECT_OFF').type='MATERIAL' 
        else:
            layout.label("No mesh selected", icon='ERROR')               