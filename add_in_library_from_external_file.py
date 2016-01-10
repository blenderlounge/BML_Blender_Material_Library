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
from os import remove
from os.path import join

if __name__ == '__main__':
    blendfile = sys.argv[5] # recupère le chemin du fichier où se trouve le matériau
    material = sys.argv[6] # recupère le nom du matériau
    render_type = sys.argv[7] # recupère le type de preview

    with bpy.data.libraries.load(blendfile) as (data_from, data_to):
        if data_from.materials:
            directory = join(blendfile,"Material")
            bpy.ops.wm.append(filename=material, directory=directory)
            bpy.data.materials[material].use_fake_user = True

            if not material in [line.body.split(';')[0] for line in bpy.data.texts['BML_material_list'].lines]:

                BML_material_list = [ligne.body for ligne in bpy.data.texts['BML_material_list'].lines if ligne]                # stockage sous forme de liste + nettoyage automatique des lignes de fin vides

                if BML_material_list[-1] == '':
                    BML_material_list[-1]= material + ';' + render_type
                else:
                    BML_material_list.append(material + ';' + render_type)

                    bpy.data.texts['BML_material_list'].clear()

                text = ''
                for line in BML_material_list:
                    text = text + line + '\n'

                bpy.data.texts['BML_material_list'].write(text)

    bpy.ops.wm.save_mainfile()
    remove(blendfile) # détruit le fichier temporaire contenant le matériau
    bpy.ops.wm.quit_blender()
