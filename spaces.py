import ifcopenshell
import ifcopenshell.geom as geom
import multiprocessing
from ifcfunctions import meshfromshape
from pandas import DataFrame

space1bounded=[]
ifc_file = ifcopenshell.open('ifcmodels/institute.ifc')

spaces = ifc_file.by_type('IfcSpace')
products = ifc_file.by_type('IfcElement')

spaces = [spaces[1]]

for space in spaces:

	for item in space.BoundedBy:
		
		space1bounded.append(item.RelatedBuildingElement)
	print("####################################")
	for item in space.ContainsElements:
		print (item)
		#print(item.RelatedBuildingElement)

	#print("####################################")









df = DataFrame (space1bounded[0],columns=['0','1','2','3','4','5','6','7','8','9','10','11','12'])
print (df)


#df = DataFrame (space1bounded,columns=['Column_Name','alain'])

#print(df)

# for space in spaces:



# 	try:
# 	    if True:
# 	    	for item in space.BoundedBy:
# 	    		print(item)
	        
# 	except IndexError:
# 	    pass