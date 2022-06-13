import cadquery as cq

from parfunlib.topologies.tpms_transition import transition_unit_cell#, gyroid_half_x, p_half, transition
from parfunlib.topologies.tpms_transition import transition_layer
#cq.Workplane.gyroid_half_x = gyroid_half_x
#cq.Workplane.p_half = p_half
#cq.Workplane.transition = transition
cq.Workplane.transition_unit_cell = transition_unit_cell


# BEGIN USER INPUT

min_thickness = 10.
max_thickness = 10.
unit_cell_size = 100.
Nx = 2
Ny = 2
Nz = 2

# END USER INPUT

thickness = min_thickness

#lattice, tr = cq.Workplane().transition_unit_cell(thickness, unit_cell_size)

g, p, tr = transition_layer(thickness, unit_cell_size, Ny, Nz)

