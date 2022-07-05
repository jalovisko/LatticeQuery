from ..commons import eachpointAdaptive

import numpy as np

import cadquery as cq

# Register our custom plugins before use.
cq.Workplane.eachpointAdaptive = eachpointAdaptive

# Gyroïd, all edges are splines on different workplanes.
def gyroid_000(self, thickness: float, unit_cell_size: float
    ) -> cq.cq.Workplane:
    """
    Create a plate with a gyroid spline edge in the first
    (000) octant
    
    Args:
      thickness (float): the thickness of the plate
      unit_cell_size (float): The size of the unit cell.
    
    Returns:
      The result of the function.
    """
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
    # Multiplying the edge points by the unit cell size.
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
        # Adding the spline to the wire.
        edge_wire = edge_wire.add(
            cq.Workplane(plane_list[i + 1])
            .workplane(offset = - offset_list[i + 1])
            .spline(edge_points[i + 1])
        )
    surface_points = [[0, 0, 0]]
    plate_4 = cq.Workplane("XY")
    # `interpPlate` is a function that interpolates a surface from a wire.
    plate_4 = plate_4.interpPlate(edge_wire, surface_points, thickness * 0.5)
    plate_4 = plate_4.union(
        cq.Workplane("XY").interpPlate(edge_wire, surface_points, - 0.5 * thickness)
    )
    return self.union(self.eachpoint(lambda loc: plate_4.val().located(loc), True))
cq.Workplane.gyroid_000 = gyroid_000

def unit_cell(location: cq.occ_impl.geom.Location,
                thickness: float,
                unit_cell_size: float,
				delta: float = 1e-8 # a small tolerance (1e-10 is too small)
				) -> cq.cq.Workplane:
    """
    Create a unit cell of gyroid, with a given thickness, and a given unit cell size
    in all 8 octants
    
    Args:
      location (cq.occ_impl.geom.Location): the location of the unit cell
      thickness (float): the thickness of the unit cell
      unit_cell_size (float): the size of the unit cell
      delta (float): a small tolerance (1e-10 is too small)
    
    Returns:
      A CQ object.
    """

    half_unit_cell_size = unit_cell_size / 2.0
    # Octante 000
    pnts = [tuple(unit_cell_size / 2 for i in range(3))]
    cq.Workplane.gyroid_000 = gyroid_000
    g_000 = (cq.Workplane("XY")
                .pushPoints(pnts)
                .gyroid_000(thickness, unit_cell_size)
            )
    result = g_000
    # Octante 100
    mirZY_pos = g_000.mirror(mirrorPlane = "ZY",
                              basePointVector = (unit_cell_size, 0, 0))
    g_100 = mirZY_pos.mirror(mirrorPlane = "XZ",
                             basePointVector = (0, half_unit_cell_size, 0))
    result = result.union(g_100)
    # Octante 110
    g_000_inverse = (cq.Workplane("XY")
                        .pushPoints(pnts)
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
    return result.val().located(location)
cq.Workplane.unit_cell = unit_cell

def gyroid_homogeneous_lattice(unit_cell_size: float,
							  thickness: float,
							  Nx: int, Ny: int, Nz: int
                ) -> cq.cq.Workplane:
    """
    Create a unit cell of gyroid, and repeat it Nx, Ny, Nz times
    
    Args:
      unit_cell_size (float): The size of the unit cell.
      thickness (float): the thickness of the unit cell
      Nx (int): number of unit cells in x direction
      Ny (int): number of unit cells in the y direction
      Nz (int): Number of unit cells in the z direction
    
    Returns:
      A CQ object.
    """

    # Register our custom plugins before use.
    cq.Workplane.eachpointAdaptive = eachpointAdaptive
    UC_pnts = []
    for i in range(Nx):
        for j in range(Ny):
            for k in range(Nz):
                UC_pnts.append((2 * i * unit_cell_size, 2 * j * unit_cell_size, 2 * k * unit_cell_size))
    result = cq.Workplane().tag('base')
    result = result.pushPoints(UC_pnts)
    unit_cell_params = []
    for i in range(Nx * Ny):
        for j in range(Nz):
            unit_cell_params.append({"thickness": thickness,
                "unit_cell_size": unit_cell_size})
    result = result.eachpointAdaptive(unit_cell,
									  callback_extra_args = unit_cell_params,
									  useLocalCoords = True)
    return result

def gyroid_heterogeneous_lattice(unit_cell_size: float,
                                min_thickness: float,
                                max_thickness: float,
                                Nx: int, Ny: int, Nz: int,
                                direction: str = 'z'
                                ) -> cq.cq.Workplane:
    """
    Create a linearly heterogeneous lattice of gyroid unit cells by creating a base workplane, 
    then pushing a list of points to it.
    
    Args:
      unit_cell_size (float): The size of the unit cell in the x, y, and z directions.
      min_thickness (float): the minimum thickness of the unit cell
      max_thickness (float): The maximum thickness of the unit cell.
      Nx (int): Number of unit cells in the x direction
      Ny (int): Number of unit cells in the y direction
      Nz (int): Number of unit cells in the z direction
      direction (str): direction of thickness variation (x, y, z)
    Returns:
      A CQ object.
    """
    coordinates_3d = ['x', 'y', 'z']
    if direction not in coordinates_3d:
        raise ValueError(f'Direction {direction} does not exist. The acceptable directions are {coordinates_3d}')
    # Register the custrom plugin 
    cq.Workplane.eachpointAdaptive = eachpointAdaptive
    ns = {'x': Nx,'y': Ny, 'z': Nz}
    thicknesses = np.linspace(min_thickness, max_thickness, ns[direction])
    UC_pnts = []
    unit_cell_size = 0.5 * unit_cell_size # because unit cell is made of 8 mirrored features
    for i in range(Nx):
        for j in range(Ny):
            for k in range(Nz):
                UC_pnts.append((2 * i * unit_cell_size, 2 * j * unit_cell_size, 2 * k * unit_cell_size))
    result = cq.Workplane().tag('base')
    result = result.pushPoints(UC_pnts)
    unit_cell_params = []
    for i in range(Nx):
        for j in range(Ny):
            for k in range(Nz):
                n_coordinates = {
                    'x': i,
                    'y': j,
                    'z': k
                }
                unit_cell_params.append({"thickness": thicknesses[n_coordinates[direction]],
                    "unit_cell_size": unit_cell_size})
    result = result.eachpointAdaptive(unit_cell,
									  callback_extra_args = unit_cell_params,
									  useLocalCoords = True)
    return result

