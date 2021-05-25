import ifcopenshell
import ifcopenshell.geom as geom
import trimesh
import matplotlib.pyplot as plt
import numpy as np

import time

from ifcfunctions import meshfromshape, getunitfactor

start_time = time.time()


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
combined.show()
combined.export('combined.ply')
for level in levels:


  myslice = combined.section(plane_origin=[0,0,(level/unitfactor)], plane_normal=[0,0,1])


  slice_2D, to_3D = myslice.to_planar()
  #slice_2D.show()

  
  




  plt.axes().set_aspect('equal', 'datalim')
  # hardcode a format for each entity type
  eformat = {'Line0': {'color': 'g', 'linewidth': 1},
         'Line1': {'color': 'y', 'linewidth': 1},
         'Arc0': {'color': 'r', 'linewidth': 1},
         'Arc1': {'color': 'b', 'linewidth': 1},
         'Bezier0': {'color': 'k', 'linewidth': 1},
         'Bezier1': {'color': 'k', 'linewidth': 1},
         'BSpline0': {'color': 'm', 'linewidth': 1},
         'BSpline1': {'color': 'm', 'linewidth': 1}}
  for entity in slice_2D.entities:
      # if the entity has it's own plot method use it
      if hasattr(entity, 'plot'):
          entity.plot(slice_2D.vertices)
          continue
      # otherwise plot the discrete curve
      discrete = entity.discrete(slice_2D.vertices)
      # a unique key for entities
      e_key = entity.__class__.__name__ + str(int(entity.closed))

      fmt = eformat[e_key].copy()
      if hasattr(entity, 'color'):
          # if entity has specified color use it
          fmt['color'] = 'black'
      plt.plot(*discrete.T,0, **fmt)


  plt.show()


