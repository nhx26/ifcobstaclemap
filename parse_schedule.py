import ifcopenshell
import ifcopenshell.geom as geom
import trimesh

from ifcfunctions import meshfromshape
from datetime import datetime



ifc_file = ifcopenshell.open('testfile.ifc')

settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)

work_schedules = ifc_file.by_type('IfcWorkSchedule')
rels = ifc_file.by_type('IfcRelAssignsToProcess')

#current_date = datetime.strptime(input('Enter current date of construction: '),"%Y-%m-%d")
current_date = datetime.strptime('2024-06-09',"%Y-%m-%d")
#print(current_date)

built = []

for item in rels:
	start = datetime.strptime(item.RelatingProcess.StartTime,"%Y-%m-%dT%H:%M:%S")
	finish = datetime.strptime(item.RelatingProcess.FinishTime,"%Y-%m-%dT%H:%M:%S")
	if current_date>finish:
		for element in item.RelatedObjects:
			built.append(element)
		

meshlist=[]
for ifc_entity in built:
	shape = geom.create_shape(settings, ifc_entity)
	meshcolor = [0,0,0,100]
	mesh = meshfromshape(shape,meshcolor) #creating mesh from shape, specifying color
	meshlist.append(mesh)

combined = trimesh.util.concatenate(meshlist)

combined.export("phase3.stl")