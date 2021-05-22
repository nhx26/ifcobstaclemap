import ifcopenshell
import ifcopenshell.geom as geom
import trimesh
import matplotlib.pyplot as plt
import numpy as np

import time

from ifcfunctions import meshfromshape, getunitfactor

start_time = time.time()


ifc_file = ifcopenshell.open('ifcmodels/smileywest.ifc')

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
	if ifc_entity.is_a('IfcDoor'):

		shape = geom.create_shape(settings, ifc_entity) #creating shape of element
		mesh = meshfromshape(shape, [0,255,0,100]) #creating mesh from shape, specifying color
		meshlist.append(mesh) #adding to list of meshes


	if ifc_entity.Representation is None: #skipping elements that have no rep
		continue 
	else:
		shape = geom.create_shape(settings, ifc_entity)
		mesh = meshfromshape(shape,[0,0,0,5])
		meshlist.append(mesh)


combined = trimesh.util.concatenate(meshlist)

#combined.show()

for level in levels:


  myslice = combined.section(plane_origin=[0,0,(level/unitfactor)], plane_normal=[0,0,1])


  slice_2D, to_3D = myslice.to_planar()
  #slice_2D.show()

  print("--- %s seconds ---" % (time.time() - start_time))
  
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
          fmt['color'] = 'black'#entity.color
      plt.plot(*discrete.T,0, **fmt)


  plt.show()
  plt.clear()

