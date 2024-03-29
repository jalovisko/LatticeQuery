import cadquery as cq

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
    print('Building an element of an array...')
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
    print(f'Success!\n{"-"*20}')
    return self.newObject(res)
# Register our custom plugin before use.
cq.Workplane.eachpointAdaptive = eachpointAdaptive

def cylinder_tranformation(radius, height,
    rotation = cq.Vector(0, 0, 0),
    transformation = cq.Vector(0, 0, 0)):
    """
    Create a cylinder with a
    circular cross section, and a height
    
    :param radius: The radius of the cylinder
    :param height: the height of the cylinder
    :param rotation: a vector that defines the rotation of the cylinder around its center
    :param transformation: a vector that represents the x, y, and z coordinates of the center of the
    cylinder
    :return: A cylinder with the specified parameters.
    """
    return (cq.Workplane()
		.transformed(offset = transformation,
                    rotate = rotation)
		.circle(radius)
		.extrude(height))

def cylinder_sequential_tranformation(radius, height,
    rotation = cq.Vector(0, 0, 0),
    transformation = cq.Vector(0, 0, 0)):
    """
    Create a cylinder with a
    circular cross section, and a height
    in a position based on linear and angular transformation
    sequentially
    
    :param radius: The radius of the cylinder
    :param height: the height of the cylinder
    :param rotation: a vector that defines the rotation of the cylinder around its center
    :param transformation: a vector that represents the x, y, and z coordinates of the center of the
    cylinder
    :return: A cylinder with the specified parameters.
    """
    return (cq.Workplane()
		.transformed(offset = transformation)
        .transformed(rotate = rotation)
		.circle(radius)
		.extrude(height))

def cuboid_tranformation(side, height, fillet,
    rotation = cq.Vector(0, 0, 0),
    transformation = cq.Vector(0, 0, 0)):
    """
    Create a cylinder with a
    circular cross section, and a height
    
    :param radius: The radius of the cylinder
    :param height: the height of the cylinder
    :param rotation: a vector that defines the rotation of the cylinder around its center
    :param transformation: a vector that represents the x, y, and z coordinates of the center of the
    cylinder
    :return: A cylinder with the specified parameters.
    """
    return (cq.Workplane("XY")
		.transformed(offset = transformation,
                    rotate = rotation)
		.rect(side, side)
        .extrude(height)
        .edges().fillet(fillet)
        )

def cylinder_by_two_points(p1: tuple,
                            p2: tuple,
                            radius: float
                            ) -> cq.cq.Workplane:
    """
    Create a cylinder with a spline (which is in fact a line)
    path and two circles as end caps
    
    Args:
      p1 (tuple): tuple of the form (x, y, z)
      p2 (tuple): tuple of the form (x, y, z)
      radius (float): radius of the cylinder
    
    Returns:
      A CQ object.
    """

    path = cq.Workplane().moveTo(p1[0], p1[1]).spline([p1, p2])

    sweep = (cq.Workplane("XY")
        .pushPoints([path.val().locationAt(0)]).circle(radius)
        .pushPoints([path.val().locationAt(1)]).circle(radius)
        .consolidateWires()
        .sweep(path, multisection = True)
        )
    return sweep

def make_sphere(center: cq.Vector, radius: float) -> cq.cq.Workplane:
    """
    It creates a sphere centered at `center` with radius `radius`
    
    Args:
      center (cq.Vector): The center of the sphere.
      radius (float): the radius of the sphere
    
    Returns:
      A cq.cq.Workplane object
    """
    center = center - cq.Vector(0, radius, 0)
    wire = cq.Workplane('XY').transformed(offset = center)
    wire = wire.threePointArc((radius, radius), (0.0, 2.0 * radius)).close()
    sphere = wire.revolve()
    return sphere

# The unit_cell class is a class that contains a unit cell size
class unit_cell():
    def __init__(self, unit_cell_size):
        self.unit_cell_size = unit_cell_size


def make_support_plate(
        Nx: int,
        Ny: int,
        Nz: int,
        unit_cell_size: float,
        thickness: float,
        margin: float
    ) -> cq.cq.Workplane:
    side_x = Nx * unit_cell_size + 2 * margin
    side_y = Ny * unit_cell_size + 2 * margin
    result = cq.Workplane().transformed(
        offset = (0.5 * side_x - margin,
        0.5 * side_y - margin,
        -0.5 * thickness))
    result = result.box(side_x, side_y, thickness)
    return result
