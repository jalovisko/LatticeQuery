import cadquery as cq

from lq.topologies.tpms_transition import transition_unit_cell#, gyroid_half_x, p_half, transition
from lq.topologies.tpms_transition import transition_layer
#cq.Workplane.gyroid_half_x = gyroid_half_x
#cq.Workplane.p_half = p_half
#cq.Workplane.transition = transition
cq.Workplane.transition_unit_cell = transition_unit_cell

from lq.commons import eachpointAdaptive

# BEGIN USER INPUT

min_thickness = 2.
max_thickness = 2.
unit_cell_size = 100.
Nx = 1
Ny = 1
Nz = 1

# END USER INPUT

#lattice, tr = cq.Workplane().transition_unit_cell(thickness, unit_cell_size)

g, p, tr = transition_layer(
    min_thickness, max_thickness, unit_cell_size, Ny, Nz, 'Z+')

