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
def gyroid_OCT(self, thickness, unit_cell_size):
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
cq.Workplane.gyroid_OCT = gyroid_OCT


def gyroid_unit_cell(thickness, unit_cell_size):
    pnts = [tuple(unit_cell_size / 2 for i in range(3))]
    result = (cq.Workplane("XY")
              .pushPoints(pnts)
              .gyroid_OCT(thickness, unit_cell_size))
    mirZY_pos = result.mirror(mirrorPlane="ZY",basePointVector = (unit_cell_size, 0, 0))
    mirXZ_pos_moved = mirZY_pos.mirror(mirrorPlane="XZ",basePointVector=(0, unit_cell_size, 0))
    
    result = result.union(mirXZ_pos)
    return result

gyroid = gyroid_unit_cell(thickness, unit_cell_size)