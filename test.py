import ifcopenshell

ifc_file = ifcopenshell.open('ifcmodels/simplehouse.ifc')

#print(ifc_file())

project = ifc_file.by_type('IfcProject')

walls = ifc_file.by_type('IfcWall')

wall = walls[0]

spaces = ifc_file.by_type('IfcSpace')

space = spaces[0]

for item in ifc_file.get_inverse(space):
	if item.is_a('IfcRelSpaceBoundary'):
		#print(item.RelatedBuildingElement)