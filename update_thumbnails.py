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
import sys.argv
from os.path import join
import subprocess

library_path = os.path.dirname(__file__)
BML_shader_library = sys.argv[1]
BML_generate_script = join(library_path, 'generate_thumbnails.py')


list_files = os.listdir(join(library_path, 'Thumbnails', 'Cloth')) + os.listdir(join(library_path, 'Thumbnails', 'Softbox')) + os.listdir(join(library_path, 'Thumbnails', 'Sphere')) + os.listdir(join(library_path, 'Thumbnails', 'Hair')) # à convertir par une liste des dossiers, puis liste matériaux > récursif

mat_list = []
thumbs_dir_list = []

for ligne in bpy.data.texts["BML_material_list"].lines:
    if ligne.body == '\n' or not ligne.body:
        continue

    if ligne.body.split(';')[0] in [file.split('.jpeg')[0] for file in list_files if file.endswith('.jpeg')]: #### ajouter option pour forcer le recalcul
        continue

    mat_list.append(ligne.body.split(';')[0])
    thumbs_dir_list.append(ligne.body.split(';')[1])

#### matériau et miniatures doivent être des str (subprocess n'accepte que ça). Ils seront redécoupés ensuite
mat_list = ';'.join(mat_list) # 'matériau1;matériau2'...
thumbs_dir_list = ';'.join(thumbs_dir_list)

with open( join(library_path,'Render_output.txt') , 'wb') as render_log:
    sub = subprocess.Popen([bpy.app.binary_path, BML_shader_library, '-b', '--python', BML_generate_script, mat_list, thumbs_dir_list], stdout=render_log, stderr=render_log)
    sub.wait() # à désactiver (option ?) pour tout rendre en même temps

os.remove( join(os.path.dirname(os.path.abspath(__file__)), 'Thumbnails', 'generate_thumbs_placeholder.txt') ) #### ATTENTION non présent ?