import ifcopenshell
import ifcopenshell.geom as geom
from ifcfunctions import rawmeshfromshape
from pandas import DataFrame

ifc_file = ifcopenshell.open('ifcmodels/simplehouse.ifc')

settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)

storeys = ifc_file.by_type('IfcBuildingStorey')

#spaces = ifc_file.by_type('IfcSpace')




storey = storeys[0]

spaces=[]

for space in ifc_file.traverse(storey.IsDecomposedBy[0]):
	if space.is_a('IfcSpace'):
		spaces.append(space)

for space in spaces[:1]:

	for item in ifc_file.get_inverse(space):
		if item.is_a('IfcRelSpaceBoundary'):
			
			element = item.RelatedBuildingElement
			print(element)
			if element.Representation is not None:
				shape = geom.create_shape(settings, element)
				verts,edges,faces = rawmeshfromshape(shape)




#print (spaces)


#df = DataFrame (space1bounded,columns=['Column_Name','alain'])

#print(df)

# for space in spaces:



# 	try:
# 	    if True:
# 	    	for item in space.BoundedBy:
# 	    		print(item)
	        
# 	except IndexError:
# 	    pass