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
import sys
from os.path import join, dirname

library_path = dirname(__file__)

mat_list = sys.argv[5].split(';') #### ATTENTION doit etre une liste
rdr_type_list = sys.argv[6].split(';')
#print(mat_list)
#print(rdr_type_list)

for idx , material in enumerate(mat_list):
    with open( join(library_path,'Render_count.txt') , 'a') as render_count: # append pour ne pas detruire l'historique
        render_count.write('\nRender Number: %d - Material: %s' % (idx+1,material)) # idx commence a 0 > idx+1

    render_type = '_' + rdr_type_list[idx] # recupere le type de miniature
    thumbnails_directory = join(library_path, 'Thumbnails', rdr_type_list[idx])

    if render_type == '_Sphere':
        bpy.context.scene.layers[0] = True
        bpy.context.scene.layers[1] = True
        bpy.context.scene.layers[2] = False
        bpy.context.scene.layers[3] = False
        bpy.context.scene.layers[4] = False
    elif render_type == '_Cloth':
        bpy.context.scene.layers[0] = True
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[2] = True
        bpy.context.scene.layers[3] = False
        bpy.context.scene.layers[4] = False
    elif render_type == '_Softbox':
        bpy.context.scene.layers[0] = True
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[2] = False
        bpy.context.scene.layers[3] = True
        bpy.context.scene.layers[4] = False
    elif render_type == '_Hair':
        bpy.context.scene.layers[0] = True
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[2] = False
        bpy.context.scene.layers[3] = False
        bpy.context.scene.layers[4] = True

    bpy.data.objects[render_type].active_material = bpy.data.materials[material]

    bpy.ops.object.select_all(action='DESELECT')
    # Selection du texte
    bpy.data.objects["Text"].select = True
    # Le mettre en Actif
    bpy.context.scene.objects.active = bpy.data.objects["Text"]

    bpy.ops.object.mode_set(mode='EDIT')

    # suppression des lettres
    for item in bpy.context.object.data.body:
        bpy.ops.font.delete()

    # insert le nom du materiau de l'objet a rendre
    bpy.ops.font.text_insert(text=material)

    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.select_all(action='DESELECT')
    # Selection de l'objet a rendre
    bpy.data.objects[render_type].select = True
    # passage de _render_Model en objet actif
    bpy.context.scene.objects.active = bpy.data.objects[render_type]

    bpy.ops.render.render()

    bpy.data.images['Render Result'].save_render(filepath=join(thumbnails_directory, material + '.jpeg'))

    print("[BML] - Preview Created:", join(thumbnails_directory, material + '.jpeg'))

bpy.ops.wm.quit_blender()
