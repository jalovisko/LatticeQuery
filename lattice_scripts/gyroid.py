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
def gyroid_000(self, thickness, unit_cell_size):
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
    plate_4 = cq.Workplane("XY")
    plate_4 = plate_4.interpPlate(edge_wire, surface_points, thickness)
    return self.union(self.eachpoint(lambda loc: plate_4.val().located(loc), True))
cq.Workplane.gyroid_000 = gyroid_000

def gyroid_unit_cell(thickness,
                     unit_cell_size,
                     delta = 1e-5 # a small tolerance (1e-10 too small)
                     ):
    half_unit_cell_size = unit_cell_size / 2.0
    # Octante 000
    pnts = [tuple(unit_cell_size / 2 for i in range(3))]
    g_000 = (cq.Workplane("XY").pushPoints(pnts)
             .gyroid_000(thickness, unit_cell_size))
    result = g_000
    # Octante 100
    mirZY_pos = g_000.mirror(mirrorPlane = "ZY",
                              basePointVector = (unit_cell_size, 0, 0))
    g_100 = mirZY_pos.mirror(mirrorPlane = "XZ",
                             basePointVector = (0, half_unit_cell_size, 0))
    result = result.union(g_100)
    # Octante 110
    g_000_inverse = (cq.Workplane("XY").pushPoints(pnts)
                     .gyroid_000(- thickness, unit_cell_size))
    mirXZ_pos = g_000_inverse.mirror(mirrorPlane = "XZ",
                                     basePointVector = (0, unit_cell_size, 0))
    g_110 = mirXZ_pos.translate((unit_cell_size, 0, 0))
    result = result.union(g_110)
    # Octante 010
    mirYZ_neg = g_110.mirror(mirrorPlane = "YZ",
                             basePointVector = (unit_cell_size, 0, 0))
    g_010 = mirYZ_neg.mirror(mirrorPlane = "XZ",
                             basePointVector = (0, 1.5 * unit_cell_size, 0))
    result = result.union(g_010)
    # Octante 001
    g_001 = g_110.translate((-unit_cell_size,
                             -unit_cell_size,
                             unit_cell_size))
    result = result.union(g_001)
    # Octante 101
    g_101 = g_010.translate((unit_cell_size,
                             -unit_cell_size,
                             unit_cell_size))
    result = result.union(g_101)
    # Octante 011
    g_011 = g_100.translate((- (1 + delta) * unit_cell_size,
                             (1 + delta) * unit_cell_size,
                             (1 + delta) * unit_cell_size))
    result = result.union(g_011)
    # Octante 111
    g_111 = g_000.translate(((1 + delta) * unit_cell_size,
                            (1 + delta) * unit_cell_size,
                            (1 + delta) * unit_cell_size))
    result = result.union(g_111)
    return result

gyroid = gyroid_unit_cell(thickness, unit_cell_size)