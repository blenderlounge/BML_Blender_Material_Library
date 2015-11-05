# -*- coding: utf-8 -*-

import bpy
import sys
import os
from os.path import join

if __name__ == '__main__':
    material = sys.argv[5] # récupère le nom du matériau
    thumbnails_directory = sys.argv[6] # récupère le dossier de stockage des miniatures
    render_type = sys.argv[7]
    new_name = sys.argv[8]

    if render_type == "_Sphere":
        bpy.context.scene.layers[0] = True
        bpy.context.scene.layers[1] = True
        bpy.context.scene.layers[2] = False
        bpy.context.scene.layers[3] = False
        bpy.context.scene.layers[4] = False
    elif render_type == "_Cloth":
        bpy.context.scene.layers[0] = True
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[2] = True
        bpy.context.scene.layers[3] = False
        bpy.context.scene.layers[4] = False
    elif render_type == "_Softbox":
        bpy.context.scene.layers[0] = True
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[2] = False
        bpy.context.scene.layers[3] = True
        bpy.context.scene.layers[4] = False
    elif render_type == "_Hair":
        bpy.context.scene.layers[0] = True
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[2] = False
        bpy.context.scene.layers[3] = False
        bpy.context.scene.layers[4] = True

    bpy.data.objects[render_type].active_material = bpy.data.materials[material]  

    bpy.data.materials[material].name = new_name
        
    bpy.ops.object.select_all(action='DESELECT')
    # Selection du texte
    bpy.data.objects["Text"].select = True
    # Le mettre en Actif
    bpy.context.scene.objects.active = bpy.data.objects["Text"]

    bpy.ops.object.mode_set(mode='EDIT')

    # suppression des lettres
    for item in bpy.context.object.data.body:
        bpy.ops.font.delete()

    # insert le nom du matériau de l'objet à rendre
    bpy.ops.font.text_insert(text=new_name)

    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.select_all(action='DESELECT')
    # Selection de l'objet à rendre
    bpy.data.objects[render_type].select = True
    # passage de _render_Model en objet actif
    bpy.context.scene.objects.active = bpy.data.objects[render_type]
    
    bpy.ops.render.render()
        
    bpy.data.images['Render Result'].save_render(filepath=join(thumbnails_directory, new_name + '.jpeg'))

    print('[BML] - Preview Created:', join(thumbnails_directory, material + '.jpeg'))
    bpy.ops.wm.save_mainfile()
    bpy.ops.wm.quit_blender()