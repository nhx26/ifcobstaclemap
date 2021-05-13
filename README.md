# ifcobstaclemap
IFC parser and semantic obstacle map generator for autonomous applications.

Uses IFCOpenShell on Python.

Prereq: IFCOpenShell, Trimesh

mesh.py takes in an IFC file and generates an obstacle map of the ground floor

mesh_mp.py takes in an IFC file and generates an obstacle map of every floor.

mesh_mp uses multiprocessing and is faster, but less robust as it is currently not working for some IFC files
