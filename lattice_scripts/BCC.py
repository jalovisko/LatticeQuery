from math import hypot, acos, degrees
import numpy as np

unit_cell_size = 10
strut_diameter = 1
node_diameter = 2
Nx = 5
Ny = 3
Nz = 4


strut_radius = strut_diameter / 2.

def eachpointAdaptive(
    self,
    callback,
    callback_extra_args = None,
    useLocalCoords = False
):
    """
    Same as each(), except that (1) each item on the stack is converted into a point before it
    is passed into the callback function and (2) it allows to pass in additional arguments, one 
    set for each object to process.

    Conversion of stack items into points means: the resulting stack has a point for each object 
    on the original stack. Vertices and points remain a point. Faces, Wires, Solids, Edges, and 
    Shells are converted to a point by using their center of mass. If the stack has zero length, a 
    single point is returned, which is the center of the current workplane / coordinate system.
    
    This is adapted from here:
    https://github.com/CadQuery/cadquery/issues/628#issuecomment-807493984

    :param callback_extra_args: Array of dicts for keyword arguments that will be 
        provided to the callback in addition to the obligatory location argument. The outer array 
        level is indexed by the objects on the stack to iterate over, in the order they appear in 
        the Workplane.objects attribute. The inner arrays are dicts of keyword arguments, each dict 
        for one call of the callback function each. If a single dict is provided, then this set of 
        keyword arguments is used for every call of the callback.
    :param useLocalCoords: Should points provided to the callback be in local or global coordinates.

    :return: CadQuery object which contains a list of vectors (points) on its stack.

    .. todo:: Implement that callback_extra_args can also be a single dict.
    .. todo:: Implement that empty dicts are used as arguments for calls to the callback if not 
        enough sets are provided for all objects on the stack.
    """

    # Convert the objects on the stack to a list of points.
    pnts = []
    plane = self.plane
    loc = self.plane.location
    if len(self.objects) == 0:
        # When nothing is on the stack, use the workplane origin point.
        pnts.append(cq.Location())
    else:
        for o in self.objects:
            if isinstance(o, (cq.Vector, cq.Shape)):
                pnts.append(loc.inverse * cq.Location(plane, o.Center()))
            else:
                pnts.append(o)

    # If no extra keyword arguments are provided to the callback, provide a list of empty dicts as 
    # structure for the **() deferencing to work below without issues.
    if callback_extra_args is None:
        callback_extra_args = [{} for p in pnts]

    # Call the callback for each point and collect the objects it generates with each call.
    res = []
    for i, p in enumerate(pnts):
        p = (p * loc) if useLocalCoords == False else p
        extra_args = callback_extra_args[i]
        p_res = callback(p, **extra_args)
        p_res = p_res.move(loc) if useLocalCoords == True else p_res
        res.append(p_res)

    # For result objects that are wires, make them pending if necessary.
    for r in res:
        if isinstance(r, cq.Wire) and not r.forConstruction:
            self._addPendingWire(r)

    return self.newObject(res)
# Register our custom plugin before use.
cq.Workplane.eachpointAdaptive = eachpointAdaptive

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

def unit_cell(unit_cell_size, strut_radius):
    result = cq.Workplane("XY").transformed(offset = location)
    result = (result
              .union(BCC_diagonals(unit_cell_size, strut_radius))
              .union(BCC_vertical_struts(unit_cell_size, strut_radius))
              .union(BCC_bottom_horizontal_struts(unit_cell_size, strut_radius))
              .union(BCC_top_horizontal_struts(unit_cell_size, strut_radius))
              .union(createNodes(node_diameter, unit_cell_size))
              )
    return result
cq.Workplane.unit_cell = unit_cell

def BCC_lattice(unit_cell_size, strut_radius, Nx, Ny, Nz):
    result = cq.Workplane("XY")
    for i in range(Nx):
        result = result.union(
            unit_cell(unit_cell_size,
                      strut_radius,
                      cq.Vector(i*unit_cell_size,
                                0,
                                0)))
    return result
# Register our custom plugin before use.
cq.Workplane.BCC_lattice = BCC_lattice

result = BCC_lattice(unit_cell_size, strut_radius, Nx, Ny, Nz)