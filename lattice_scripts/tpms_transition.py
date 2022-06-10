import cadquery as cq

from parfunlib.topologies.tpms_transition import transition_layer#, gyroid_half_x, p_half, transition

#cq.Workplane.gyroid_half_x = gyroid_half_x
#cq.Workplane.p_half = p_half
#cq.Workplane.transition = transition
cq.Workplane.transition_layer = transition_layer


# BEGIN USER INPUT

min_thickness = 10.
max_thickness = 10.
unit_cell_size = 100.
Nx = 2
Ny = 2
Nz = 2

# END USER INPUT

thickness = min_thickness

tr = transition_layer(thickness, unit_cell_size, Ny, Nz)
"""
g = gyroid_half_x(thickness, unit_cell_size)
p = cq.Workplane().transformed(
    offset = (unit_cell_size, 0, 0)
    ).p_half(thickness, unit_cell_size)

tr = cq.Workplane().transformed(
    offset = (1.5 * unit_cell_size, 0.5 * unit_cell_size, 0.5 * unit_cell_size)
    ).transition(thickness, unit_cell_size)
"""