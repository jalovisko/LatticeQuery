# Python
import cadquery as cq

# BEGIN USER INPUT

thickness = 0.1
unit_cell_size = 7

# END USER INPUT

# Gyroïd, all edges are splines on different workplanes.
def createGyroid(self, thickness, unit_cell_size):
    half_unit_cell_size = unit_cell_size / 2.0
    quarter_unit_cell_size = unit_cell_size / 4.0
    edge_points = [
        [[half_unit_cell_size, half_unit_cell_size],
         [quarter_unit_cell_size, 0.0],
         [half_unit_cell_size, - half_unit_cell_size]],
        [[- half_unit_cell_size, - half_unit_cell_size],
         [0.0, - quarter_unit_cell_size],
         [half_unit_cell_size, - half_unit_cell_size]],
        [[- half_unit_cell_size, - half_unit_cell_size],
         [0.0, - quarter_unit_cell_size],
         [half_unit_cell_size, - half_unit_cell_size]],
        [[- half_unit_cell_size, - half_unit_cell_size],
         [- quarter_unit_cell_size, 0.0],
         [- half_unit_cell_size, half_unit_cell_size]],
        [[half_unit_cell_size, half_unit_cell_size],
         [0.0, quarter_unit_cell_size],
         [- half_unit_cell_size, half_unit_cell_size]],
        [[half_unit_cell_size, half_unit_cell_size],
         [0.0, quarter_unit_cell_size],
         [- half_unit_cell_size, half_unit_cell_size]],
    ]
    plane_list = ["XZ", "XY", "YZ", "XZ", "YZ", "XY"]
    offset_list = [- half_unit_cell_size,
                   half_unit_cell_size,
                   half_unit_cell_size,
                   half_unit_cell_size,
                   - half_unit_cell_size,
                   - half_unit_cell_size]
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
