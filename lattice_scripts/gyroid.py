# Python
import cadquery as cq
import numpy as np

# BEGIN USER INPUT

thickness = 0.1
unit_cell_size = 10
Nx = 3
Ny = 3
Nz = 3

# END USER INPUT

# Gyroïd, all edges are splines on different workplanes.
def createGyroid(self, thickness, unit_cell_size):
    half_unit_cell_size = unit_cell_size / 2.0
    quarter_unit_cell_size = unit_cell_size / 4.0
    edge_points = [
        [[0.5, 0.5],
         [0.25, 0.0],
         [0.5, - 0.5]],
        [[- 0.5, - 0.5],
         [0.0, - 0.25],
         [0.5, - 0.5]],
        [[- 0.5, - 0.5],
         [0.0, - 0.25],
         [0.5, - 0.5]],
        [[- 0.5, - 0.5],
         [- 0.25, 0.0],
         [- 0.5, 0.5]],
        [[0.5, 0.5],
         [0.0, 0.25],
         [- 0.5, 0.5]],
        [[0.5, 0.5],
         [0.0, 0.25],
         [- 0.5, 0.5]],
    ]
    edge_points = np.array(edge_points) * unit_cell_size
    
    plane_list = ["XZ", "XY", "YZ", "XZ", "YZ", "XY"]
    offset_list = [- 1, 1, 1, 1, - 1, - 1]
    offset_list = np.array(offset_list) * unit_cell_size * 0.5
    edge_wire = (
        cq.Workplane(plane_list[0])
        .workplane(offset = - offset_list[0])
        .spline(edge_points[0])
    )
    for i in range(len(edge_points) - 1):
        edge_wire = edge_wire.add(
            cq.Workplane(plane_list[i + 1])
            .workplane(offset = - offset_list[i + 1])
            .spline(edge_points[i + 1])
        )
    surface_points = [[0, 0, 0]]
    plate_4 = (cq.Workplane("XY").interpPlate(edge_wire, surface_points, thickness))
    return self.union(self.eachpoint(lambda loc: plate_4.val().located(loc), True))
cq.Workplane.createGyroid = createGyroid

pnts = [(0, 0)]
gyroid = (cq.Workplane("XY")
          .pushPoints(pnts)
          .createGyroid(thickness, unit_cell_size))

"""
UC_pnts = [(i * unit_cell_size, 0) for i in range(Nx)]
UC = cq.Workplane().tag('base')
for pnt in UC_pnts:
    # Generating the positions for each homogeneous layer
    layer_pnts = []
    nodes_pnts = []
    for i in range(Ny):
        for j in range(Nz):
            layer_pnts.append((0, i * unit_cell_size, j *unit_cell_size))
    for i in range(Ny):
        for j in range(Nz + 1):
            nodes_pnts.append((0, i * unit_cell_size, j *unit_cell_size))
    UC = (UC
          .workplaneFromTagged('base')
          .center(*pnt)
          .pushPoints(layer_pnts)
          .createGyroid(thickness, unit_cell_size))

"""
