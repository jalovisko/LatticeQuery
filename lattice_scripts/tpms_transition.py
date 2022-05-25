import cadquery as cq

from parfunlib.topologies.tpms_transition import gyroid_half_x, p_half, transition
from parfunlib.topologies.gyroid import gyroid_heterogeneous_lattice

cq.Workplane.gyroid_half_x = gyroid_half_x
cq.Workplane.p_half = p_half
cq.Workplane.transition = transition
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
p = cq.Workplane().transformed(
    offset = (unit_cell_size, 0, 0)
    ).p_half(thickness, unit_cell_size)

tr = cq.Workplane().transformed(
    offset = (0.5 * unit_cell_size, 0, 0)
    ).transition(thickness, unit_cell_size)

spline_cq = cq.Workplane("XY")
spline_cq.objects = [spline_edge]

