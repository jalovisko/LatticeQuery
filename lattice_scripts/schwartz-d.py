# Python
import cadquery as cq
from math import cos, sqrt
import numpy as np
import time
from parfunlib.topologies.schwartz import schwartz_heterogeneous_lattice
cq.Workplane.schwartz_heterogeneous_lattice = schwartz_heterogeneous_lattice

# BEGIN USER INPUT

unit_cell_size = 10
Nx = 1
Ny = 1
Nz = 1
min_thickness = 0.1
max_thickness = 7
# END USER INPUT

#timing performance
start_time = time.time()

def schwartz_d_000(self, thickness, unit_cell_size):
    half_unit_cell = unit_cell_size * 0.5
    pts = [
        (0, half_unit_cell, 0),
        (half_unit_cell, half_unit_cell, 0),
        (half_unit_cell, 0, 0),
        (half_unit_cell, 0, half_unit_cell),
        (0, 0, half_unit_cell),
        (0, half_unit_cell, half_unit_cell),
        (0, half_unit_cell, 0)
    ]
    edge_wire = cq.Workplane().polyline(pts)
    surface_points = [[half_unit_cell * 0.5, half_unit_cell * 0.5, half_unit_cell * 0.5]]
    plate_4 = cq.Workplane("XY")
    plate_4 = plate_4.interpPlate(edge_wire, surface_points, 0.5 * thickness)
    plate_4 = plate_4.union(
        cq.Workplane("XY").interpPlate(edge_wire, surface_points, - 0.5 * thickness)
    )
    return self.union(self.eachpoint(lambda loc: plate_4.val().located(loc), True))

cq.Workplane.schwartz_d_000 = schwartz_d_000

half_unit_cell = unit_cell_size * 0.5
pts = [
    (0, half_unit_cell, 0),
    (half_unit_cell, half_unit_cell, 0),
    (half_unit_cell, 0, 0),
    (half_unit_cell, 0, half_unit_cell),
    (0, 0, half_unit_cell),
    (0, half_unit_cell, half_unit_cell),
    (0, half_unit_cell, 0)
]
edge_wire = cq.Workplane().polyline(pts)

result = cq.Workplane().schwartz_d_000(min_thickness, unit_cell_size)
result = result.union(cq.Workplane().transformed(
    offset = cq.Vector(unit_cell_size, unit_cell_size, 0)).transformed(
    rotate = cq.Vector(0, 0, 180))
    .schwartz_d_000(min_thickness, unit_cell_size))

print('The excecution time is:  %s seconds'  % (time.time() - start_time))
