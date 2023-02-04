import ifcopenshell

# Open the IFC file
ifc_file = ifcopenshell.open('simplehouse.ifc')

# Create an IfcWorkschedule entity
phase1 = ifc_file.createIfcWorkSchedule(Name='phase 1',StartTime= '2023-06-01T00:00:00',FinishTime='2023-06-05T00:00:00')
phase2 = ifc_file.createIfcWorkSchedule(Name='phase 2',StartTime= '2023-06-05T00:00:00',FinishTime='2023-06-08T00:00:00')
phase3 = ifc_file.createIfcWorkSchedule(Name='phase 3',StartTime= '2023-06-08T00:00:00',FinishTime='2023-06-10T00:00:00')

# Get a list of the walls in the IFC file and assign to corresponding phases
ifc_walls = ifc_file.by_type('IfcWall')
phase1_elems= [ifc_walls[8],ifc_walls[7],ifc_walls[6],ifc_walls[5]]
phase2_elems= [ifc_walls[4],ifc_walls[3],ifc_walls[1]]
phase3_elems= [ifc_walls[2],ifc_walls[0]]
# Create an IfcRelAssignsToProcess entity to link the walls to the workschedule
ifc_file.createIfcRelAssignsToProcess(
    RelatingProcess=phase1,
    RelatedObjects=phase1_elems
)

ifc_file.createIfcRelAssignsToProcess(
    RelatingProcess=phase2,
    RelatedObjects=phase2_elems
)

ifc_file.createIfcRelAssignsToProcess(
    RelatingProcess=phase3,
    RelatedObjects=phase3_elems
)

# Save the changes to the IFC file
ifc_file.write('testfile.ifc')
