import bpy
import sys
import os
from os.path import join

if __name__ == '__main__':
    material = sys.argv[5] # recupere le nom du materiau
    thumbnails_directory = sys.argv[6] # recupere le dossier de stockage des miniatures
    
    bpy.data.objects["_Render_Model"].active_material = bpy.data.materials[material]
    
    bpy.ops.object.select_all(action='DESELECT')
    # Sélection du Texte
    bpy.data.objects["Text"].select = True
    # Le mettre en Actif
    bpy.context.scene.objects.active = bpy.data.objects["Text"]

    bpy.ops.object.mode_set(mode='EDIT')
    
    # suppression des lettres
    for item in bpy.context.object.data.body:
        bpy.ops.font.delete()

    # insert le nom du materiau de l'objet à rendre
    bpy.ops.font.text_insert(text=material)

    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.select_all(action='DESELECT')
    # Sélection de l'objet à rendre
    bpy.data.objects["_Render_Model"].select = True
    # passge de 8render_Model en objet actif
    bpy.context.scene.objects.active = bpy.data.objects["_Render_Model"]
    
    bpy.ops.render.render()
    
    # print('[BSL] - Preview Created:', join(thumbnails_directory, material + '.jpeg'))
    
    bpy.data.images['Render Result'].save_render(filepath=join(thumbnails_directory, material + '.jpeg'))
    
    bpy.ops.wm.quit_blender()
