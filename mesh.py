import ifcopenshell
import ifcopenshell.geom as geom
import trimesh
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv

import time

from ifcfunctions import meshfromshape, getunitfactor

arsheight = 0.5


ifc_file = ifcopenshell.open('ifcmodels/institute.ifc')

settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)

meshlist=[]
levels=[]

unitfactor = getunitfactor(ifc_file)

storeys = ifc_file.by_type('IfcBuildingStorey')

elements = ifc_file.by_type('IfcElement')

for storey in storeys:
  levels.append(storey.ObjectPlacement.RelativePlacement.Location[0][2])

print(levels)





for ifc_entity in ifc_file.by_type('IfcElement'): #iterating through every ifcelement
  if ifc_entity.is_a('IfcOpeningElement'):
		  continue #skipping IfcOpeningElement because its not useful to obstacle map?
  if ifc_entity.Representation is None: #skipping elements that have no representation
      continue 

  shape = geom.create_shape(settings, ifc_entity)
    
  if ifc_entity.is_a('IfcDoor'):
      meshcolor = [0,255,0,100]
  elif ifc_entity.is_a('IfcStair'):
      meshcolor = [255,255,0,100]
  else:
      meshcolor = [0,0,0,90]



		
  mesh = meshfromshape(shape,meshcolor) #creating mesh from shape, specifying color
  meshlist.append(mesh) #adding to list of meshes
  


combined = trimesh.util.concatenate(meshlist)

combined.export('combined.ply')


mesh = pv.read('combined.ply')

for level in levels:
  single_slice = mesh.slice(normal=[0, 0, 1],origin=[0,0,(level/unitfactor+0.5)])
  p = pv.Plotter()
  p.set_background("white")
  actor = p.add_mesh(single_slice,show_scalar_bar=False,cmap=['black','green','yellow'])
  p.set_focus(single_slice.center)
  p.camera_set = True
  p.show(screenshot='OMs/{0}.png'.format(level))
  p.remove_actor(actor)

























  

