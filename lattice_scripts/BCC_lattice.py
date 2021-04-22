from math import hypot, acos, degrees
import numpy as np
from topologies.fblgen_helper import eachpointAdaptive

unit_cell_size = 10
strut_diameter = 1
node_diameter = 2
Nx = 2
Ny = 3
Nz = 2

strut_radius = strut_diameter / 2.

# The angle is chosen with respect to the positive X direction
def create_diagonal_strut(location, radius, angle_x, angle_y):
    hypot2D = hypot(unit_cell_size, unit_cell_size)
    hypot3D = hypot(hypot2D, unit_cell_size)
    result = (
        cq.Workplane()
        .transformed(rotate = cq.Vector(angle_x, angle_y, 0))
        .circle(radius)
        .extrude(hypot3D)
    )
    return result.val().located(location)

# In a cube ABCDA1B1C1D1 this is the angle C1AD
angle_C1AD = 90 - degrees(acos(3**-.5))

corner_points = unit_cell_size * np.array(
    [(0, 0),
    (1, 0),
    (1, 1),
    (0, 1)]
    )

def BCC_diagonals(unit_cell_size, strut_radius):
    result = (
        cq.Workplane("XY")
        .pushPoints(corner_points)
        .eachpointAdaptive(
            create_diagonal_strut,
            callback_extra_args = [
                {"radius": strut_radius,
                 "angle_x": - 45,
                 "angle_y": angle_C1AD},
                {"radius": strut_radius,
                 "angle_x": - 45,
                 "angle_y": - angle_C1AD},
                {"radius": strut_radius,
                 "angle_x": 45,
                 "angle_y": - angle_C1AD},
                {"radius": strut_radius,
                 "angle_x": 45,
                 "angle_y": angle_C1AD}
                ],
            useLocalCoords = True
        )
    )
    return result
# Register our custom plugin before use.
cq.Workplane.BCC_diagonals = BCC_diagonals

def BCC_vertical_struts(unit_cell_size, strut_radius):
    result = cq.Workplane("XY")
    for point in corner_points:
        result = (result
                  .union(
                      cq.Workplane()
                      .transformed(offset = cq.Vector(point[0], point[1]))
                      .circle(strut_radius)
                      .extrude(unit_cell_size)
                      )
                  )
    return result
# Register our custom plugin before use.
cq.Workplane.BCC_vertical_struts = BCC_vertical_struts

def BCC_bottom_horizontal_struts(unit_cell_size, strut_radius):
    result = cq.Workplane("XY")
    angle = 90
    for point in corner_points:
        result = (result
                  .union(
                      cq.Workplane()
                      .transformed(offset = cq.Vector(point[0], point[1], 0),
                                   rotate = cq.Vector(90, angle, 0))
                      .circle(strut_radius)
                      .extrude(unit_cell_size)
                      )
                  )
        angle += 90
    return result
# Register our custom plugin before use.
cq.Workplane.BCC_bottom_horizontal_struts = BCC_bottom_horizontal_struts

def BCC_top_horizontal_struts(unit_cell_size, strut_radius):
    result = cq.Workplane("XY")
    angle = 90
    for point in corner_points:
        result = (result
                  .union(
                      cq.Workplane()
                      .transformed(offset = cq.Vector(point[0], point[1], unit_cell_size),
                                   rotate = cq.Vector(90, angle, 0))
                      .circle(strut_radius)
                      .extrude(unit_cell_size)
                      )
                  )
        angle += 90
    return result
# Register our custom plugin before use.
cq.Workplane.BCC_top_horizontal_struts = BCC_top_horizontal_struts

# Creates 4 nodes at the XY plane of each unit cell
def createNodes(node_diameter,
                unit_cell_size,
                delta = 0.01 # a small coefficient is needed because CQ thinks that it cuts through emptiness
                ):
    added_node_diameter = node_diameter + delta
    node_radius = node_diameter / 2.0
    result = cq.Workplane("XY")
    for point in corner_points:
        result= (result
                  .union(
                      cq.Workplane()
                      .transformed(offset = cq.Vector(point[0], point[1], 0))
                      .box(added_node_diameter, added_node_diameter, added_node_diameter)
                      .edges("|Z")
                      .fillet(node_radius)
                      .edges("|X")
                      .fillet(node_radius)
                      )
                  )
        result= (result
                  .union(
                      cq.Workplane()
                      .transformed(offset = cq.Vector(point[0], point[1], unit_cell_size))
                      .box(added_node_diameter, added_node_diameter, added_node_diameter)
                      .edges("|Z")
                      .fillet(node_radius)
                      .edges("|X")
                      .fillet(node_radius)
                      )
                  )
    half_unit_cell_size = unit_cell_size / 2
    result= (result
             .union(
                 cq.Workplane()
                 .transformed(offset = cq.Vector(half_unit_cell_size,
                                                 half_unit_cell_size,
                                                 half_unit_cell_size))
                 .box(added_node_diameter, added_node_diameter, added_node_diameter)
                 .edges("|Z")
                 .fillet(node_radius)
                 .edges("|X")
                 .fillet(node_radius)
                 )
             )
    return result
cq.Workplane.createNodes = createNodes

def unit_cell(self, unit_cell_size, strut_radius):
    result = cq.Workplane("XY")
    result = (result
              .union(BCC_diagonals(unit_cell_size, strut_radius))
              .union(BCC_vertical_struts(unit_cell_size, strut_radius))
              .union(BCC_bottom_horizontal_struts(unit_cell_size, strut_radius))
              .union(BCC_top_horizontal_struts(unit_cell_size, strut_radius))
              .union(createNodes(node_diameter, unit_cell_size))
              )
    return self.union(self.eachpoint(lambda loc: result.val().located(loc), True))
cq.Workplane.unit_cell = unit_cell


def BCC_lattice(unit_cell_size, strut_radius, Nx, Ny, Nz):
    UC_pnts = []
    for i in range(Nx):
        for j in range(Ny):
            for k in range(Nz):
                UC_pnts.append((i * unit_cell_size, j * unit_cell_size, k * unit_cell_size))
    result = cq.Workplane().tag('base')
    result = result.pushPoints(UC_pnts)
    result = result.unit_cell(unit_cell_size, strut_radius)
    return result
# Register our custom plugin before use.
#cq.Workplane.BCC_lattice = BCC_lattice

#result = unit_cell(unit_cell_size, strut_radius)
result = BCC_lattice(unit_cell_size, strut_radius, Nx, Ny, Nz)