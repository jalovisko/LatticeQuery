import cadquery as cq

from parfunlib.topologies.tpms_transition import gyroid_half_x, p_half
from parfunlib.topologies.gyroid import gyroid_heterogeneous_lattice

cq.Workplane.gyroid_half_x = gyroid_half_x
cq.Workplane.p_half = p_half
cq.Workplane.gyroid_heterogeneous_lattice = gyroid_heterogeneous_lattice

# BEGIN USER INPUT

min_thickness = 10.
max_thickness = 10.
unit_cell_size = 100.
Nx = 5
Ny = 5
Nz = 1

# END USER INPUT

thickness = min_thickness

g = gyroid_half_x(thickness, unit_cell_size)
p = p_half(thickness, unit_cell_size)