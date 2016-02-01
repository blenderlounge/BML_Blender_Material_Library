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
import os
from os.path import join
from os import remove

if __name__ == '__main__':
    material = sys.argv[5] # recupere le nom du materiau ### TODO a convertir en liste
    #thumbnails_directory = sys.argv[6] # recupere le dossier de stockage des miniatures

    bpy.data.objects["_Sphere"].active_material = bpy.data.materials[material]

    bpy.data.materials[material].use_fake_user = False
    bpy.data.materials[material].user_clear()

    for line in bpy.data.texts["BML_material_list"].lines:
        if line.body.split(';')[0] == material:
            line.body = ''

    bpy.ops.wm.save_mainfile()
    bpy.ops.wm.quit_blender()