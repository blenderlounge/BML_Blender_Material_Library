# -*- coding: utf-8 -*-

import bpy
import sys
import os
from os.path import join

if __name__ == '__main__':
    material = sys.argv[5] # récupère le nom du matériau
    thumbnails_directory = sys.argv[6] # récupère le dossier de stockage des miniatures
    
    bpy.data.objects["render_material"].active_material = bpy.data.materials[material]

    bpy.ops.render.render()
    
    print('[BSL] - Preview Created:', join(thumbnails_directory, material + '.jpeg'))
    
    bpy.data.images['Render Result'].save_render(filepath=join(thumbnails_directory, material + '.jpeg'))
    
    bpy.ops.wm.quit_blender()
