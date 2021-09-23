# Python
import cadquery as cq

from math import cos, sqrt
import numpy as np

from parfunlib.topologies.schwartz import schwartz_heterogeneous_lattice
cq.Workplane.schwartz_heterogeneous_lattice = schwartz_heterogeneous_lattice

# BEGIN USER INPUT

unit_cell_size = 10
Nx = 1
Ny = 1
Nz = 1
thickness = 1

# END USER INPUT
"""
schwartz = schwartz_heterogeneous_lattice(unit_cell_size, min_thickness, max_thickness,
                                      Nx, Ny, Nz)
"""

half_unit_cell_size = unit_cell_size / 2.0
quarter_unit_cell_size = unit_cell_size / 4.0
delta_radius = 0.5 - 0.5/sqrt(2)
edge_points = [
    [[0.0, 0.5],
     [delta_radius, delta_radius],
     [0.5, 0.0]],
    [[0.0, 0.5],
     [delta_radius, delta_radius],
     [0.5, 0.0]],
    [[0.0, 0.5],
     [delta_radius, delta_radius],
     [0.5, 0.0]],
    [[-0.5, 0.0],
     [-delta_radius,-delta_radius],
     [0.0, -0.5]],
    [[-0.5, 0.0],
     [-delta_radius,-delta_radius],
     [0.0, -0.5]],
    [[-0.5, 0.0],
     [-delta_radius,-delta_radius],
     [0.0, -0.5]]
]
edge_points = np.array(edge_points) * unit_cell_size

plane_list = ["XZ", "XY", "YZ", "XZ", "YZ", "XY"]
offset_list = [- 1, 1, 1, 1, - 1, - 1]
offset_list = np.array(offset_list) * unit_cell_size * 0.5

edge_wire = (
    cq.Workplane(plane_list[0])
    .workplane(offset = - offset_list[0])
    .moveTo(edge_points[0][0][0],
            edge_points[0][0][1])
    .threePointArc(tuple(edge_points[0][1]),
                   tuple(edge_points[0][2]))
)
edge_wire = edge_wire.add(cq.Workplane(plane_list[5])
                          .workplane(offset = - offset_list[5])
                          .moveTo(edge_points[5][0][0],
                                  edge_points[5][0][1])
                          .threePointArc(tuple(edge_points[5][1]),
                                         tuple(edge_points[5][2]))
                          )
#edge_wire = edge_wire.add(cq.Workplane(plane_list[1])
#             .workplane(offset = - offset_list[1]),
#             .moveTo(edge_points[1][0][0],
#                     edge_points[1][0][1])
#             .threePointArc(tuple(edge_points[1][1]),
#                   tuple(edge_points[1][2]))
#             )
#for i in range(len(edge_points) - 1):
#    edge_wire = edge_wire.add(
#        cq.Workplane(plane_list[i + 1])
#        .workplane(offset = - offset_list[i + 1])
#        .spline(edge_points[i + 1])
#    )

#surface_points = [[0, 0, 0]]
#plate_4 = cq.Workplane("XY")
#plate_4 = plate_4.interpPlate(edge_wire, surface_points, thickness)