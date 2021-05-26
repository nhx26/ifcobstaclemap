import json
import ifcopenshell
import ifcopenshell.geom as geom
from ifcfunctions import rawmeshfromshape, meshfromshape



ifc_file = ifcopenshell.open('ifcmodels/institute.ifc')

settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)

mesh_dict={}

for ifc_entity in ifc_file.by_type('IfcElement'): #iterating through every ifcelement

	if ifc_entity.Representation is None: #skipping elements that have no rep
		continue 

	else:
		shape = geom.create_shape(settings, ifc_entity)
		verts,edges,faces = rawmeshfromshape(shape)
		mesh_dict[ifc_entity.GlobalId]={
								'verts':verts,
								'edges':edges,
								'faces':faces,
								'type':ifc_entity.is_a(),

								
		}
		if ifc_entity.is_a('IfcDoor'):
			mesh_dict[ifc_entity.GlobalId].update({

				'operationtype':ifc_entity.IsTypedBy[0].RelatingType.OperationType,
				'width':ifc_entity.OverallWidth,
				'height':ifc_entity.OverallHeight,


				})


json_object = json.dumps(mesh_dict, indent = 4)  
print(json_object)

with open('ifc.json', 'w') as outfile:
    json.dump(mesh_dict, outfile)
