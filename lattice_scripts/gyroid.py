# Python
import cadquery as cq

# Gyroïd, all edges are splines on different workplanes.

thickness = 0.1
edge_points = [
    [[3.54, 3.54], [1.77, 0.0], [3.54, -3.54]],
    [[-3.54, -3.54], [0.0, -1.77], [3.54, -3.54]],
    [[-3.54, -3.54], [0.0, -1.77], [3.54, -3.54]],
    [[-3.54, -3.54], [-1.77, 0.0], [-3.54, 3.54]],
    [[3.54, 3.54], [0.0, 1.77], [-3.54, 3.54]],
    [[3.54, 3.54], [0.0, 1.77], [-3.54, 3.54]],
]
plane_list = ["XZ", "XY", "YZ", "XZ", "YZ", "XY"]
offset_list = [-3.54, 3.54, 3.54, 3.54, -3.54, -3.54]
edge_wire = (
    cq.Workplane(plane_list[0]).workplane(offset=-offset_list[0]).spline(edge_points[0])
)
for i in range(len(edge_points) - 1):
    edge_wire = edge_wire.add(
        cq.Workplane(plane_list[i + 1])
        .workplane(offset=-offset_list[i + 1])
        .spline(edge_points[i + 1])
    )
surface_points = [[0, 0, 0]]
plate_4 = cq.Workplane("XY").interpPlate(edge_wire, surface_points, thickness)
print("plate_4.val().Volume() = ", plate_4.val().Volume())
#plate_4 = plate_4.translate((0, 5 * 12, 0))

#show_object(fin)
#fin.val().exportStep('Gyroid_Cell.stp')
