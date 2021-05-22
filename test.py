import ifcopenshell

ifc_file = ifcopenshell.open('ifcmodels/simplehouse.ifc')

#print(ifc_file())

project = ifc_file.by_type('IfcProject')

print(project[0].IsDefinedBy)