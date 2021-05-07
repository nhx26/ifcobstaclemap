import ifcopenshell
import ifcopenshell.geom as geom
import trimesh
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing
from ifcfunctions import meshfromshape, getunitfactor


meshlist=[]
levels=[]


ifc_file = ifcopenshell.open('ifcmodels/ac20.ifc')

unitfactor = getunitfactor(ifc_file)

storeys = ifc_file.by_type('IfcBuildingStorey')

elements = ifc_file.by_type('IfcElement')







for storey in storeys:

    levels.append(storey.ObjectPlacement.RelativePlacement.Location[0][2])


print (levels)

settings = geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)
iterator = geom.iterator(settings, ifc_file, multiprocessing.cpu_count())
valid_file = iterator.initialize()
if valid_file:
    while True:
        shape = iterator.get()
        product = iterator.get().product
        if product.is_a('IfcOpeningElement'):
            iterator.next()
            continue

        if product.is_a('IfcElement') and not product.is_a('IfcDoor') and not product.is_a('IfcStair'):
            
            mesh = meshfromshape(shape,[0,0,0,50])
            meshlist.append(mesh)

        if product.is_a('IfcDoor'):

            mesh = meshfromshape(shape,[0,255,0,100])
            meshlist.append(mesh)

        if product.is_a('IfcStair'):

            mesh = meshfromshape(shape,[255,255,0,100])
            meshlist.append(mesh)


        
        if not iterator.next():
            break



combined = trimesh.util.concatenate(meshlist)

#combined.show()

for level in levels:

    myslice = combined.section(plane_origin=[0,0,(level/unitfactor)], plane_normal=[0,0,1])

    slice_2D, to_3D = myslice.to_planar()

    slice_2D.show()
