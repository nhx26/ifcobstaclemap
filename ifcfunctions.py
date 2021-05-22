
import ifcopenshell
import matplotlib.pyplot as plt
from matplotlib import collections as  mc
import numpy as np
import math
import trimesh



def getunitfactor(ifc_file):

    project = ifc_file.by_type('IfcProject')

    units = project[0].UnitsInContext.Units

    length_unit = next(filter(lambda u: u.UnitType == "LENGTHUNIT", units))

    prefix = length_unit[2]

    if prefix == None:
        return 1
    if prefix == 'MILLI':
        return 1000




def meshfromshape(shape, color):

	verts = shape.geometry.verts
	edges = shape.geometry.edges 
	faces = shape.geometry.faces




	procverts = [verts[i:i+3] for i in range(0,len(verts), 3)]

	procedges = [edges[i : i + 2] for i in range(0, len(edges), 2)]

	procfaces = [tuple(faces[i : i + 3]) for i in range(0, len(faces), 3)]



	mesh = trimesh.Trimesh(vertices=procverts,faces=procfaces, edges=procedges, process = True)

	for facet in mesh.facets:
		mesh.visual.face_colors[facet] = color 

	return mesh

def rawmeshfromshape(shape):

	verts = shape.geometry.verts
	edges = shape.geometry.edges 
	faces = shape.geometry.faces




	procverts = [verts[i:i+3] for i in range(0,len(verts), 3)]

	procedges = [edges[i : i + 2] for i in range(0, len(edges), 2)]

	procfaces = [tuple(faces[i : i + 3]) for i in range(0, len(faces), 3)]


	return procverts,procedges,procfaces


def findanchor(item):
	item = item.ObjectPlacement
	myanchor = [0,0,0]
	while item.PlacementRelTo != None:
		relanchor = item.RelativePlacement.Location[0]
		myanchor[0] = myanchor[0]+relanchor[0]
		myanchor[1] = myanchor[1]+relanchor[1]
		myanchor[2] = myanchor[2]+relanchor[2]
		item = item.PlacementRelTo
	return myanchor

def findabsangle(item):
	item = item.ObjectPlacement
	myangle  = 0
	while item.PlacementRelTo != None:
		reldirection = item.RelativePlacement.RefDirection[0]
		print(reldirection)
		angle = (math.atan2(reldirection[1],reldirection[0])) * (180 /math.pi)
		myangle = myangle + angle
		item = item.PlacementRelTo
	return myangle

def findwidth(element_quantity):

	for quantity in element_quantity.Quantities:
			if quantity.is_a('IfcQuantityLength'):
				if quantity.Name == 'Width':
					width = quantity.LengthValue
					return width

def get_width(item):
	for definition in item.IsDefinedBy:
		related_data = definition.RelatingPropertyDefinition
		if related_data.is_a('IfcElementQuantity'):
			
			data = findwidth(related_data)
			if data != None:
				width = data
				return width


def findheight(element_quantity):

	for quantity in element_quantity.Quantities:
			if quantity.is_a('IfcQuantityLength'):
				if quantity.Name == 'Height':
					height = quantity.LengthValue
					return height

def get_height(item):
	for definition in item.IsDefinedBy:
		related_data = definition.RelatingPropertyDefinition
		if related_data.is_a('IfcElementQuantity'):
			
			data = findheight(related_data)
			if data != None:
				height = data
				return height






def finddepth(element_quantity):

	for quantity in element_quantity.Quantities:
			if quantity.is_a('IfcQuantityLength'):
				if quantity.Name == 'Depth':
					length = quantity.LengthValue
					return length

def get_depth(item):
	for definition in item.IsDefinedBy:
		related_data = definition.RelatingPropertyDefinition
		if related_data.is_a('IfcElementQuantity'):
			
			data = finddepth(related_data)
			if data != None:
				length = data
				return length


def findtrueanchor(item):
	absanchor = [0,0]
	item = item.ObjectPlacement.PlacementRelTo
	while item.PlacementRelTo != None:
		relanchor = item.RelativePlacement.Location[0]
		
		reldirection = item.PlacementRelTo.RelativePlacement.RefDirection[0]

		

		relanchor = [relanchor[:2]]

		myanchor=[]

		theta = (math.atan2(reldirection[1],reldirection[0]))
	
		myanchor = [ (x * math.cos(theta) - y * math.sin(theta), x * math.sin(theta) + y * math.cos(theta)) for x,y in relanchor]
		absanchor[0] = absanchor[0] + myanchor[0][0]
		absanchor[1] = absanchor[1] + myanchor[0][1]
		# print('anchor:'+str(relanchor))
		# print('myanchor:'+str(myanchor))
		# print('direction'+str(reldirection))
		# print('######')
		item = item.PlacementRelTo
	return absanchor

def findabscoords(item):
	item = item.ObjectPlacement
	myanchor = [0,0]
	while item.PlacementRelTo != None:
		print ("ok")
		relanchor = item.RelativePlacement.Location[0]
		myanchor[0] = myanchor[0]+relanchor[0]
		myanchor[1] = myanchor[1]+relanchor[1]
		item = item.PlacementRelTo
	return myanchor



def countitems(items):

    counted = []
    itemlist = []
    index = 0
    itemcounter = []

    for i in range(len(items)):
        itemcounter.append(0)

        
    for item in items:
        if item not in counted:
            itemlist.append(item)
            counted.append(item)
            index = index + 1
            for item2 in items:
                if item2 == item:
                    itemcounter[index-1] = itemcounter[index-1]+1


    for x in range(len(itemlist)):

        print (str(itemlist[x])+'::::'+str(itemcounter[x]))