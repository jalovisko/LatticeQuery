import cadquery as cq

uc_size = 5
Nx = 15
Ny = 15
thickness = 5
allowance = 1

x = Nx * uc_size + (allowance * 2)
y = Ny * uc_size + (allowance * 2)

support_plane = cq.Workplane().box(x, y, thickness)