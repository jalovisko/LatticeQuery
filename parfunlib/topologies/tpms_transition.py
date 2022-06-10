from difflib import restore
import cadquery as cq

from math import sqrt

from ..commons import eachpointAdaptive
from .gyroid import gyroid_000
from .schwartz import schwartz_p_000

# Register our custom plugins before use.
cq.Workplane.eachpointAdaptive = eachpointAdaptive

def gyroid_half_x(thickness: float,
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
    #result = result.union(g_100)
    # Octante 110
    g_000_inverse = (cq.Workplane("XY")
                        .pushPoints(pnts)
                        .gyroid_000(- thickness, unit_cell_size))
    mirXZ_pos = g_000_inverse.mirror(mirrorPlane = "XZ",
                                     basePointVector = (0, unit_cell_size, 0))
    g_110 = mirXZ_pos.translate((unit_cell_size, 0, 0))
    #result = result.union(g_110)
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
    #g_101 = g_010.translate((unit_cell_size,
    #                         -unit_cell_size,
    #                         unit_cell_size))
    #result = result.union(g_101)
    # Octante 011
    g_011 = g_100.translate((- (1 + delta) * unit_cell_size,
                             (1 + delta) * unit_cell_size,
                             (1 + delta) * unit_cell_size))
    result = result.union(g_011)
    # Octante 111
    #g_111 = g_000.translate(((1 + delta) * unit_cell_size,
    #                        (1 + delta) * unit_cell_size,
    #                        (1 + delta) * unit_cell_size))
    #result = result.union(g_111)
    return result
cq.Workplane.gyroid_half_x = gyroid_half_x

def p_half(self,
    thickness: float,
    unit_cell_size: float
    ) -> cq.cq.Workplane:
    """
    Create a unit cell of a Schwartian P surface by creating a unit cell of a
    Schwartz P, then mirroring it in three directions
    
    :param location: the location of the object
    :param thickness: the thickness of the material
    :param unit_cell_size: the size of the unit cell
    :return: A CQ object.
    """
    result = cq.Workplane("XY")
    # Octante 000
    pnts = [tuple(unit_cell_size / 2 for _ in range(3))]
    cq.Workplane.schwartz_p_000 = schwartz_p_000
    s_000 = (cq.Workplane("XY").pushPoints(pnts)
             .schwartz_p_000(thickness, unit_cell_size))
    
    #result = result.union(s_000)
    # Octante 100
    s_100 = s_000.mirror(mirrorPlane = "ZY",
                              basePointVector = (unit_cell_size, 0, 0))
    result = result.union(s_100)
    # Octante 110
    #s_000_inverse = (cq.Workplane("XY").pushPoints(pnts)
    #                 .schwartz_p_000(- thickness, unit_cell_size))
    s_110 = s_100.mirror(mirrorPlane = "XZ",
                            basePointVector = (0, unit_cell_size, 0))
    #s_110 = mirXZ_pos.translate((unit_cell_size, 0, 0))
    result = result.union(s_110)
    # Octante 010
    #s_010 = s_000.mirror(mirrorPlane = "XZ",
    #                        basePointVector = (0, unit_cell_size, 0))
    #result = result.union(s_010)
    # The top side is just a mirror of the bottom one
    s_top = result.mirror(mirrorPlane = "XY",
                            basePointVector = (0, 0, unit_cell_size))
    result = result.union(s_top)
    return self.union(self.eachpoint(lambda loc: result.val().located(loc), True))

cq.Workplane.p_half = p_half

def transition(location,
        thickness: float,
        unit_cell_size: float
        ) -> cq.cq.Workplane:
    half_uc = 0.5 * unit_cell_size
    quarter_uc = 0.25 * unit_cell_size
    delta_radius = half_uc - half_uc/sqrt(2)
    # transition 1
    gyroid_pnts = [
        (half_uc, half_uc),
        (0.0, quarter_uc),
        (- half_uc, half_uc)
    ]
    transition_negative_pnts = [
        (- half_uc, half_uc),
        (0.0, quarter_uc),
        (half_uc, 0.0)
    ]
    schwarz_p_pnts = [
        [half_uc, - half_uc, 0.0],
        [half_uc, - delta_radius, - delta_radius],
        [half_uc, 0.0, - half_uc]
    ]
    edge_wire = (
        cq.Workplane('YZ')
        .workplane(offset = - 0.5 * unit_cell_size)
        .spline(gyroid_pnts)
    )
    edge_wire = edge_wire.add(
        cq.Workplane('XZ')
            .workplane(offset = 0.5 * unit_cell_size)
            .spline(transition_negative_pnts)
    )
    edge_wire = edge_wire.add(
        cq.Workplane()
            .workplane()
            .moveTo(schwarz_p_pnts[0][0],
                schwarz_p_pnts[0][1]
                )
            .threePointArc(tuple(schwarz_p_pnts[1]),
                tuple(schwarz_p_pnts[2])
                )
    )
    edge_wire = edge_wire.add(edge_wire.close())
    surface_points = [[0, 0, 0]]
    plate_0 = cq.Workplane("XY")
    plate_0 = plate_0.interpPlate(edge_wire, surface_points, 0.5 * thickness)
    plate_0 = plate_0.union(
        cq.Workplane("XY").interpPlate(edge_wire, surface_points, - 0.5 * thickness)
    )
    # transition 2
    gyroid_pnts = [
        (- half_uc, - half_uc),
        (0.0, - quarter_uc),
        (half_uc, - half_uc)
    ]
    transition_negative_pnts = [
        (- half_uc, - half_uc),
        (0.0, - quarter_uc),
        (half_uc, 0.0)
    ]
    schwarz_p_pnts = [
        [half_uc, half_uc, 0.0],
        [half_uc, delta_radius, - delta_radius],
        [half_uc, 0.0, - half_uc]
    ]
    edge_wire = (
        cq.Workplane('YZ')
        .workplane(offset = - 0.5 * unit_cell_size)
        .spline(gyroid_pnts)
    )
    edge_wire = edge_wire.add(
        cq.Workplane('XZ')
            .workplane(offset = - 0.5 * unit_cell_size)
            .spline(transition_negative_pnts)
    )
    edge_wire = edge_wire.add(
        cq.Workplane()
            .workplane()
            .moveTo(schwarz_p_pnts[0][0],
                schwarz_p_pnts[0][1]
                )
            .threePointArc(tuple(schwarz_p_pnts[1]),
                tuple(schwarz_p_pnts[2])
                )
    )
    edge_wire = edge_wire.add(edge_wire.close())
    surface_points = [[0, 0, 0]]
    plate_1 = cq.Workplane("XY").transformed(offset = (0, unit_cell_size, 0))
    plate_1 = plate_1.interpPlate(edge_wire, surface_points, 0.5 * thickness)
    plate_1 = plate_1.union(
        cq.Workplane("XY")
        .transformed(offset = (0, unit_cell_size, 0))
        .interpPlate(edge_wire, surface_points, - 0.5 * thickness)
    )
    result = plate_0.union(plate_1)
    # transition 3
    gyroid_pnts = [
        (half_uc, half_uc),
        (0.0, quarter_uc),
        (- half_uc, half_uc)
    ]
    transition_negative_pnts = [
        (- half_uc, half_uc),
        (0.0, quarter_uc),
        (half_uc, 0.0)
    ]
    schwarz_p_pnts = [
        [half_uc, - half_uc, 0.0],
        [half_uc, - delta_radius, delta_radius],
        [half_uc, 0.0, half_uc]
    ]
    edge_wire = (
        cq.Workplane('YZ')
        .workplane(offset = - 0.5 * unit_cell_size)
        .spline(gyroid_pnts)
    )
    edge_wire = edge_wire.add(
        cq.Workplane('XZ')
            .workplane(offset = 0.5 * unit_cell_size)
            .spline(transition_negative_pnts)
    )
    edge_wire = edge_wire.add(
        cq.Workplane()
            .workplane()
            .moveTo(schwarz_p_pnts[0][0],
                schwarz_p_pnts[0][1]
                )
            .threePointArc(tuple(schwarz_p_pnts[1]),
                tuple(schwarz_p_pnts[2])
                )
    )
    edge_wire = edge_wire.add(edge_wire.close())
    surface_points = [[0, 0, 0]]
    plate_2 = cq.Workplane("XY").transformed(offset = (0, 0, unit_cell_size))
    plate_2 = plate_2.interpPlate(edge_wire, surface_points, 0.5 * thickness)
    plate_2 = plate_2.union(
        cq.Workplane("XY")
        .transformed(offset = (0, 0, unit_cell_size))
        .interpPlate(edge_wire, surface_points, - 0.5 * thickness)
    )
    result = result.union(plate_2)
    # transition 4
    gyroid_pnts = [
        (- half_uc, - half_uc),
        (0.0, - quarter_uc),
        (half_uc, - half_uc)
    ]
    transition_negative_pnts = [
        (- half_uc, - half_uc),
        (0.0, - quarter_uc),
        (half_uc, 0.0)
    ]
    schwarz_p_pnts = [
        [half_uc, half_uc, 0.0],
        [half_uc, delta_radius, delta_radius],
        [half_uc, 0.0, half_uc]
    ]
    edge_wire = (
        cq.Workplane('YZ')
        .workplane(offset = - 0.5 * unit_cell_size)
        .spline(gyroid_pnts)
    )
    edge_wire = edge_wire.add(
        cq.Workplane('XZ')
            .workplane(offset = - 0.5 * unit_cell_size)
            .spline(transition_negative_pnts)
    )
    edge_wire = edge_wire.add(
        cq.Workplane()
            .workplane()
            .moveTo(schwarz_p_pnts[0][0],
                schwarz_p_pnts[0][1]
                )
            .threePointArc(tuple(schwarz_p_pnts[1]),
                tuple(schwarz_p_pnts[2])
                )
    )
    edge_wire = edge_wire.add(edge_wire.close())
    surface_points = [[0, 0, 0]]
    plate_3 = cq.Workplane("XY").transformed(offset = (0, unit_cell_size, unit_cell_size))
    plate_3 = plate_3.interpPlate(edge_wire, surface_points, 0.5 * thickness)
    plate_3 = plate_3.union(
        cq.Workplane("XY")
        .transformed(offset = (0, unit_cell_size, unit_cell_size))
        .interpPlate(edge_wire, surface_points, - 0.5 * thickness)
    )
    result = result.union(plate_3)
    return result.val().located(location)
cq.Workplane.transition = transition

def transition_layer(
    thickness: float,
    unit_cell_size: float,
    size_1: int,
    size_2: int,
    direction: str = 'X'
    ):
    result = cq.Workplane()
    transition_pnts = []
    for i in range(size_1):
        for j in range(size_2):
            transition_pnts.append((0, i * unit_cell_size, j * unit_cell_size))
    unit_cell_size *= 0.5 # because the unit cell is made of 8 smaller ones
    unit_cell_params = []
    for i in range(size_1):
        for j in range(size_2):
            unit_cell_params.append(
                {
                    "thickness": thickness,
                    "unit_cell_size": unit_cell_size
                })
    result = result.pushPoints(transition_pnts)
    result = result.eachpointAdaptive(transition,
									  callback_extra_args = unit_cell_params,
									  useLocalCoords = True)
    """
    for i in range(size_1):
        for j in range(size_2):
            result = result.union(
                cq.Workplane().transformed(
                    offset = (0, i * unit_cell_size, j * unit_cell_size)
                ).gyroid_half_x(thickness, unit_cell_size)
            )
            result = result.union(
                cq.Workplane().transformed(
                    offset = (0, i * unit_cell_size, j * unit_cell_size)
                ).p_half(thickness, unit_cell_size)
            )
            result = result.union(
                cq.Workplane().transformed(
                    offset = (0, i * unit_cell_size, j * unit_cell_size)
                ).transition(thickness, unit_cell_size)
            )
    """
    return result
cq.Workplane.transition_layer = transition_layer
