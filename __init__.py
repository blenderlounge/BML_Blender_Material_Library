# -*- coding: utf-8 -*-

'''
Copyright (C) 2015 YOUR NAME
YOUR@MAIL.com

Created by Lapineige, Pitiwazou, Pistiwique, Matpi

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

bl_info = {
    "name": "Blender Material Library (BML)",
    "description": "Create your own material library, with thumbnail preview and a simple import",
    "author": "Lapineige, Pitiwazou, Pistiwique, Matpi",
    "version": (0, 2, 1),
    "blender": (2, 75, 0),
    "location": "3D View / Material Properties",
    "warning": "This addon is still in development - quite stable, but keep a copy of your materials",
    "wiki_url": "",
    "category": "Material" }

    
    
import bpy 
from bpy.types import AddonPreferences
from bpy.props import StringProperty, BoolProperty   
from . draw import *


#----VIEW_3D----#
def update_VIEW3D_PT_view_3d_bml(self, context):
    try:
        bpy.utils.unregister_class(VIEW3D_PT_view_3d_bml)
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.ui_panel:
        bpy.utils.register_class(VIEW3D_PT_view_3d_bml)

def update_VIEW3D_PT_tools_bml(self, context):
    try:
        bpy.utils.unregister_class(VIEW3D_PT_tools_bml)
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tools_panel:
        VIEW3D_PT_tools_bml.bl_category = context.user_preferences.addons[__name__].preferences.tools_category
        bpy.utils.register_class(VIEW3D_PT_tools_bml)
        
def update_VIEW3D_HT_header_bml_preview(self, context):
    try:
        bpy.types.VIEW3D_HT_header.remove(VIEW3D_HT_header_bml_preview) 
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.header_view3d:
        bpy.types.VIEW3D_HT_header.append(VIEW3D_HT_header_bml_preview) 


#----NODE_EDITOR----#
def update_NODE_PT_tools_bml(self, context):
    try:
        bpy.utils.unregister_class(NODE_PT_tools_bml)
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.ne_tools_panel:
        NODE_PT_tools_bml.bl_category = context.user_preferences.addons[__name__].preferences.ne_tools_category
        bpy.utils.register_class(NODE_PT_tools_bml)
        
def update_NODE_PT_ui_bml(self, context):
    try:
        bpy.utils.unregister_class(NODE_PT_ui_bml)
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.ne_ui_panel:
        bpy.utils.register_class(NODE_PT_ui_bml) 

def update_NODE_HT_header_bml_preview(self, context):
    try:
        bpy.types.NODE_HT_header.remove(NODE_HT_header_bml_preview) 
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.header_node_editor:
        bpy.types.NODE_HT_header.append(NODE_HT_header_bml_preview)        
                
#----MATERIAL----#            
def update_Cycles_PT_bml_panel(self, context):
    try:
        bpy.utils.unregister_class(Cycles_PT_bml_panel)
    except:
        pass
    
    # VIEW_3D
    if context.user_preferences.addons[__name__].preferences.material_panel:
        bpy.utils.register_class(Cycles_PT_bml_panel)        
        
        
     
class BlenderMaterialLibraryAddonPreferences(AddonPreferences):
    bl_idname = __name__

    #3DVIEW
    ui_panel = BoolProperty(
            default=True,
            update=update_VIEW3D_PT_view_3d_bml
            )
    tools_panel = BoolProperty(
            default=True,
            update=update_VIEW3D_PT_tools_bml
            )
    tools_category = StringProperty(
               name="Category",
               description="Choose a name for the category panel",
               default="BML",
               update=update_VIEW3D_PT_tools_bml
               )
    header_view3d = BoolProperty(
            default=True,
            update=update_VIEW3D_HT_header_bml_preview
            )
    
    #NodeEditor
    ne_ui_panel = BoolProperty(
            default=True,
            update=update_NODE_PT_ui_bml
            )
    ne_tools_panel = BoolProperty(
            default=True,
            update=update_NODE_PT_tools_bml
            )
    ne_tools_category = StringProperty(
            name="Node Editor Category",
            description="Choose a name for the category panel",
            default="BML",
            update=update_NODE_PT_tools_bml
            )
    header_node_editor = BoolProperty(
            default=True,
            update=update_NODE_HT_header_bml_preview
            )
    
    #Material Panel
    material_panel = BoolProperty(
            default=True,
            update=update_Cycles_PT_bml_panel
            )
    
    
    enable_tab_info = BoolProperty(default=False)
    enable_tab_options = BoolProperty(default=False)
    enable_tab_urls = BoolProperty(default=False)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "enable_tab_info", text="Info", icon="QUESTION")  
        if self.enable_tab_info:
            row = layout.row()
            layout.label(text="Blender Shader Library is a simple and powerfull library for Blender")
            layout.label(text="You just have to Add your own shaders to the library with the Add Material To Library button")
            layout.label(text="Your material will be automatically added to the library with his own thumbnail")
            layout.label(text="You can delete materials as well with the remove material from library button")
            layout.separator()
            layout.label(text="This Addon is still in development and will have more options in the near future")
            layout.label(text="Have fun and don't hesitate to tell us what do you think avout the addon on the blenderlounge forum")
            
        layout.prop(self, "enable_tab_options", text="Options", icon="SCRIPTWIN")  
        if self.enable_tab_options:
            # VIEW_3D
            box = layout.box()
            row = box.row()
            row.label(text="3D View :", icon='MESH_CUBE')
            row = box.row()
            row.prop(self, "tools_panel", text="T Panel")
            if self.tools_panel:
                row.prop(self, "tools_category")
            row = box.row()
            row.prop(self, "ui_panel", text="N Panel")
            row = box.row()
            row.prop(self, "header_view3d", text="Header 3DView")
            
            # NODE_EDITOR
            box = layout.box()
            row = box.row()
            row.label(text="Node Editor :", icon='NODETREE')
            row = box.row()
            row.prop(self, "ne_tools_panel", text="T Panel")
            if self.ne_tools_panel:
                row.prop(self, "ne_tools_category")
            row = box.row()
            row.prop(self, "ne_ui_panel", text="N Panel")
            row = box.row()
            row.prop(self, "header_node_editor", text="Header Node Editor")
            
            # MATERIAL
            box = layout.box()
            row = box.row()
            row.label(text="Material Panel :", icon='MATERIAL')
            row = box.row()
            row.prop(self, "material_panel", text="Material Panel")
            
            
        layout.prop(self, "enable_tab_urls", text="URL's", icon="URL") 
        if self.enable_tab_urls:
            row = layout.row()    
            row.operator("wm.url_open", text="Pistiwique").url = "https://github.com/pistiwique"
            row.operator("wm.url_open", text="Pitiwazou").url = "http://www.pitiwazou.com/"
            row.operator("wm.url_open", text="Lapineige").url = "http://le-terrier-de-lapineige.over-blog.com/"
            row.operator("wm.url_open", text="BlenderLounge").url = "http://blenderlounge.fr/"
            
            
# register
################################## 
    
def register():
    bpy.utils.register_module(__name__) 
    register_BML_pcoll_preview()
    update_VIEW3D_PT_view_3d_bml(None, bpy.context)
    update_VIEW3D_PT_tools_bml(None, bpy.context)
    update_VIEW3D_HT_header_bml_preview(None, bpy.context)
    update_NODE_PT_tools_bml(None, bpy.context)
    update_Cycles_PT_bml_panel(None, bpy.context)
    update_NODE_PT_ui_bml(None, bpy.context)
    update_NODE_HT_header_bml_preview(None, bpy.context)
        
    bpy.types.WindowManager.is_generating_preview = bpy.props.BoolProperty(default=False)
    bpy.types.WindowManager.preview_type = bpy.props.EnumProperty(
            items=(('_Sphere', "Sphere", ''),
                   ('_Cloth', "Cloth", ''),
                   ('_Softbox', "Softbox", ''),
                   ('_Hair', "Hair", "")),
                   default='_Sphere',
                   name='',
                   update=update_preview_type)

def unregister():
    unregister_BML_pcoll_preview()
    bpy.types.VIEW3D_HT_header.remove(VIEW3D_HT_header_bml_preview)  
    bpy.types.VIEW3D_HT_header.remove(NODE_HT_header_bml_preview)   
    bpy.utils.unregister_module(__name__)   
