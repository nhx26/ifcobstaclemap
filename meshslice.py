import pyvista as pv


mesh = pv.read('combined.ply')
#cpos=mesh.plot()
single_slice = mesh.slice(normal=[0, 0, 1],origin=[0,0,0.001])
#single_slice.plot(cmap=['black','green','yellow'],parallel_projection = True, background='white')

p = pv.Plotter()
p.set_background("white")
actor = p.add_mesh(single_slice,show_scalar_bar=False,cmap=['black','green','yellow'])

p.set_focus(single_slice.center)
p.camera_set = True
#p.remove_actor(actor)
p.show(screenshot='OM.png')
