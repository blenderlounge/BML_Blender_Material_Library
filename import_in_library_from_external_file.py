import bpy
import sys
import os
from os.path import join

if __name__ == '__main__':
    blendfile = sys.argv[5] # récupère le chemin du fichier ou se trouve le matériau
    material = sys.argv[6] # récupère le nom du matériau
    
    with bpy.data.libraries.load(blendfile) as (data_from, data_to):
        if data_from.materials:                 
            directory = join(blendfile,"Material")
            bpy.ops.wm.append(filename=material, directory=directory)
            bpy.data.materials[material].use_fake_user = True
    
    bpy.ops.wm.save_mainfile()
    os.remove(blendfile)
    bpy.ops.wm.quit_blender()
    
