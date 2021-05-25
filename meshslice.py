import pyvista as pv

mesh = pv.read('combined.ply')
#cpos=mesh.plot()
single_slice = mesh.slice(normal=[0, 0, 1],origin=[0,0,0.001])
single_slice.plot(cmap=['black','green','yellow'],parallel_projection = True, background='white')