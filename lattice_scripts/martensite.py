import cadquery as cq

from lq.commons import eachpointAdaptive
from lq.topologies.bcc import unit_cell as bcc_unit_cell
from lq.topologies.bcc import create_diagonal_strut as create_bcc_diagonal_strut
from lq.topologies.fcc import unit_cell as fcc_unit_cell
from lq.topologies.fcc import create_diagonal_strut as create_fcc_diagonal_strut


from math import acos, atan, degrees, hypot, sqrt
import numpy as np
#from parfunlib.topologies.martensite import fcc_martensite

# USER INPUT

unit_cell_size = 6
strut_diameter = 1
node_diameter = 1.1
# Nx = 2
Ny = 1
Nz = 3
uc_break = 0

# END USER INPUT

# Register our custom plugins before use.
cq.Workplane.eachpointAdaptive = eachpointAdaptive
cq.Workplane.fcc_unit_cell = fcc_unit_cell

class martensite:
    def __init__(self,
                 unit_cell_size: float,
                 strut_diameter: float,
                 node_diameter: float,
                 Ny: int,
                 Nz: int,
                 uc_break: int):
        self.unit_cell_size = unit_cell_size
        self.bcc_unit_cell_size = 0.5 * sqrt(2) *unit_cell_size
        self.strut_diameter = strut_diameter
        self.strut_radius = 0.5 * strut_diameter
        self.node_diameter = node_diameter
        self.node_radius = 0.5 * node_diameter
        self.Ny = Ny
        self.Nz = Nz
        self.uc_break = uc_break
        if self.uc_break < 0:
            raise ValueError('The value of the beginning of the break should larger than 0')

    ################################################################
    # FCC
    ################################################################
    
    def __fcc_martensite(self):
        UC_pnts = []
        self.Nx = self.Nz + self.uc_break - 1
        for i in range(self.Nx):
            for j in range(self.Ny):
                for k in range(self.Nz):
                    if k - 1 < i:
                        UC_pnts.append(
                            (i * self.unit_cell_size,
                            j * self.unit_cell_size,
                            k * self.unit_cell_size))
        print("FCC datapoints generated")
        result = cq.Workplane().tag('base')
        result = result.pushPoints(UC_pnts)
        unit_cell_params = []
        for i in range(self.Nx * self.Ny):
            for j in range(self.Nz):
                unit_cell_params.append({"unit_cell_size": self.unit_cell_size,
                    "strut_radius": self.strut_diameter * 0.5,
                    "node_diameter": self.node_diameter,
                    "type": 'fcc'})
        print("The FCC lattice section is generated")
        result = result.eachpointAdaptive(fcc_unit_cell,
                                callback_extra_args = unit_cell_params,
                                useLocalCoords = True)
        return result

    
    def __fcc_transition_diagonals(self) -> cq.cq.Workplane:
        """
        Creates a solid model of the diagonals in a FCC unit cell.
    
        Returns
        -------
            result : cq.occ_impl.shapes.Compound
                a solid model of the strut
        """
        corner_points = self.unit_cell_size * np.array(
            [(0, 0),
            (1, 0),
            (1, 0),
            (1, 1),
            (1, 1),
            (0, 1)]
            )
        result = (
            cq.Workplane("XY")
            .pushPoints(corner_points)
            .eachpointAdaptive(
                create_fcc_diagonal_strut,
                callback_extra_args = [
                    {"unit_cell_size": self.unit_cell_size,
                    "radius": self.strut_radius,
                    "angle_x": 0,
                    "angle_y": 45},
                    {"unit_cell_size": self.unit_cell_size * 0.5,
                    "radius": self.strut_radius,
                    "angle_x": 0,
                    "angle_y": - 45},
                    {"unit_cell_size": self.unit_cell_size,
                    "radius": self.strut_radius,
                    "angle_x": -45,
                    "angle_y": 0},
                    {"unit_cell_size": self.unit_cell_size,
                    "radius": self.strut_radius,
                    "angle_x": 45,
                    "angle_y": 0},
                    {"unit_cell_size": self.unit_cell_size * 0.5,
                    "radius": self.strut_radius,
                    "angle_x": 0,
                    "angle_y": - 45},
                    {"unit_cell_size": self.unit_cell_size,
                    "radius": self.strut_radius,
                    "angle_x": 0,
                    "angle_y": 45}
                    ],
                useLocalCoords = True
            )
        )
        return result
    
    def __fcc_transition_horizontal_diagonal_struts(self):
        result = cq.Workplane("XY")
        corner_points = self.unit_cell_size * np.array(
            [(0, 0, 0),
            (1, 0, 0)]
        )
        angle = 135.0
        hypot2D = hypot(self.unit_cell_size, self.unit_cell_size)
        for point in corner_points:
            result = (result
                    .union(
                        cq.Workplane()
                        .transformed(offset = cq.Vector(point[0], point[1], point[2]),
                                    rotate = cq.Vector(90, angle, 0))
                        .circle(self.strut_radius)
                        .extrude(hypot2D)
                        )
                    )
            angle += 90
        return result

    def __fcc_transition_nodes(self,
                    delta = 0.01 # a small coefficient is needed because CQ thinks that it cuts through emptiness
                    ):
        added_node_diameter = self.node_diameter + delta
        node_radius = self.node_diameter / 2.0
        result = cq.Workplane("XY")
        corner_points = self.unit_cell_size * np.array(
            [(0, 0),
            (1, 0),
            (1, 1),
            (0, 1)]
        )
        corner_points = np.vstack([corner_points, self.unit_cell_size * np.array([(0.5, 0.5)])])
        for point in corner_points:
            result = (result
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
        result = (result
                    .union(
                        cq.Workplane()
                        .transformed(offset = cq.Vector(
                            self.unit_cell_size,
                            self.unit_cell_size * 0.5,
                            self.unit_cell_size * 0.5))
                        .box(added_node_diameter, added_node_diameter, added_node_diameter)
                        .edges("|Z")
                        .fillet(node_radius)
                        .edges("|X")
                        .fillet(node_radius)
                        )
                    )
        return result

    def __fcc_transition_unit_cell(self, location):
        result = cq.Workplane("XY")
        result = result.union(self.__fcc_transition_diagonals())
        result = result.union(self.__fcc_transition_horizontal_diagonal_struts())
        result = result.union(self.__fcc_transition_nodes())
        return result.val().located(location)

    def __fcc_transition(self):
        UC_pnts = []
        self.Nx = self.Nz + self.uc_break
        for i in range(-1, self.Nx):
            for j in range(self.Ny):
                for k in range(-1, self.Nz):
                    if k - 1 == i:
                        UC_pnts.append(
                            (i * self.unit_cell_size,
                            j * self.unit_cell_size,
                            k * self.unit_cell_size))
        print("FCC transition datapoints generated")
        result = cq.Workplane().tag('base')
        result = result.pushPoints(UC_pnts)
        unit_cell_params = []
        for i in range(self.Nx * self.Ny):
            for j in range(self.Nz):
                unit_cell_params.append({"unit_cell_size": self.unit_cell_size,
                    "strut_radius": self.strut_diameter * 0.5,
                    "node_diameter": self.node_diameter,
                    "type": 'fcc'})
        print("The FCC transition lattice is generated")
        result = result.eachpointAdaptive(self.__fcc_transition_unit_cell,
                                            useLocalCoords = True)
        return result 

    ################################################################
    # BCC
    ################################################################
    
    def __bcc_diagonals(self) -> cq.cq.Workplane:
        """
        Creates a solid model of the diagonals in a BCC unit cell.

        Returns
        -------
            cq.occ_impl.shapes.Compound
                a solid model of the strut
        """
        # In a cuboid ABCDA1B1C1D1 this is the angle C1AD
        #angle_C1AD = 90 - degrees(acos(2**-.5))
        angle_C1AD = 90 - degrees(acos(0.5))
        angle_CAD = 90 - degrees(acos(sqrt(2/3)))
        pseudo_unit_cell_size = sqrt(2/3)*self.unit_cell_size
        corner_points = np.array(
            [(0, 0),
            (self.bcc_unit_cell_size, 0),
            (self.bcc_unit_cell_size, self.unit_cell_size),
            (0, self.unit_cell_size)]
        )
        result = (
            cq.Workplane("XY")
            .pushPoints(corner_points)
            .eachpointAdaptive(
                    create_bcc_diagonal_strut,
                    callback_extra_args = [
                        {"unit_cell_size": pseudo_unit_cell_size,
                        "radius": self.strut_radius,
                        "angle_x": - angle_CAD,
                        "angle_y": angle_C1AD},
                        {"unit_cell_size": pseudo_unit_cell_size,
                        "radius": self.strut_radius,
                        "angle_x": - angle_CAD,
                        "angle_y": - angle_C1AD},
                        {"unit_cell_size": pseudo_unit_cell_size,
                        "radius": self.strut_radius,
                        "angle_x": angle_CAD,
                        "angle_y": - angle_C1AD},
                        {"unit_cell_size": pseudo_unit_cell_size,
                        "radius": self.strut_radius,
                        "angle_x": angle_CAD,
                        "angle_y": angle_C1AD}
                        ],
                    useLocalCoords = True
                    )
            )
        return result
    
    # Creates 4 nodes at the XY plane of each unit cell
    def __create_bcc_nodes(self,
        delta = 0.01 # a small coefficient is needed because CQ thinks that it cuts through emptiness
        ):
        added_node_diameter = self.node_diameter + delta
        result = cq.Workplane("XY")
        corner_points = np.array(
            [(0, 0),
            (self.bcc_unit_cell_size, 0),
            (self.bcc_unit_cell_size, self.unit_cell_size),
            (0, self.unit_cell_size)]
        )
        for point in corner_points:
            result = (result
                    .union(
                        cq.Workplane()
                        .transformed(offset = cq.Vector(point[0], point[1], 0))
                        .box(added_node_diameter, added_node_diameter, added_node_diameter)
                        .edges("|Z")
                        .fillet(self.node_radius)
                        .edges("|X")
                        .fillet(self.node_radius)
                        )
                    )
            result = (result
                    .union(
                        cq.Workplane()
                        .transformed(offset = cq.Vector(point[0], point[1], self.bcc_unit_cell_size))
                        .box(added_node_diameter, added_node_diameter, added_node_diameter)
                        .edges("|Z")
                        .fillet(self.node_radius)
                        .edges("|X")
                        .fillet(self.node_radius)
                        )
                    )
        result = (result
                .union(
                    cq.Workplane()
                    .transformed(offset = cq.Vector(0.5 * self.bcc_unit_cell_size ,
                                                    0.5 * self.unit_cell_size ,
                                                    0.5 * self.bcc_unit_cell_size ))
                    .box(added_node_diameter, added_node_diameter, added_node_diameter)
                    .edges("|Z")
                    .fillet(self.node_radius)
                    .edges("|X")
                    .fillet(self.node_radius)
                    )
                )
        return result

    def __bcc_unit_cell(self, location):
        result = cq.Workplane("XY")
        result = result.union(self.__bcc_diagonals())
        result = result.union(self.__create_bcc_nodes())
        return result.val().located(location)

    def __bcc_top_diagonals(self) -> cq.cq.Workplane:
        """
        Creates a solid model of the diagonals in a BCC unit cell.

        Returns
        -------
            cq.occ_impl.shapes.Compound
                a solid model of the strut
        """
        # In a cuboid ABCDA1B1C1D1 this is the angle C1AD
        #angle_C1AD = 90 - degrees(acos(2**-.5))
        angle_C1AD = 90 - degrees(acos(0.5))
        angle_CAD = 90 - degrees(acos(sqrt(2/3)))
        pseudo_unit_cell_size = sqrt(2/3)*self.unit_cell_size
        corner_points = np.array(
            [(0, 0),
            (self.bcc_unit_cell_size, 0),
            (self.bcc_unit_cell_size, self.unit_cell_size),
            (0, self.unit_cell_size)]
        )
        result = (
            cq.Workplane("XY")
            .pushPoints(corner_points)
            .eachpointAdaptive(
                    create_bcc_diagonal_strut,
                    callback_extra_args = [
                        {"unit_cell_size": 0.5 * pseudo_unit_cell_size,
                        "radius": self.strut_radius,
                        "angle_x": - angle_CAD,
                        "angle_y": angle_C1AD},
                        {"unit_cell_size": pseudo_unit_cell_size,
                        "radius": self.strut_radius,
                        "angle_x": - angle_CAD,
                        "angle_y": - angle_C1AD},
                        {"unit_cell_size": pseudo_unit_cell_size,
                        "radius": self.strut_radius,
                        "angle_x": angle_CAD,
                        "angle_y": - angle_C1AD},
                        {"unit_cell_size": 0.5 * pseudo_unit_cell_size,
                        "radius": self.strut_radius,
                        "angle_x": angle_CAD,
                        "angle_y": angle_C1AD}
                        ],
                    useLocalCoords = True
                    )
            )
        return result
    
    def __bcc_left_diagonals(self) -> cq.cq.Workplane:
        """
        Creates a solid model of the diagonals in a BCC unit cell on the left.

        Returns
        -------
            cq.occ_impl.shapes.Compound
                a solid model of the strut
        """
        # In a cuboid ABCDA1B1C1D1 this is the angle C1AD
        #angle_C1AD = 90 - degrees(acos(2**-.5))
        angle_C1AD = 90 - degrees(acos(0.5))
        angle_CAD = 90 - degrees(acos(sqrt(2/3)))
        pseudo_unit_cell_size = sqrt(2/3)*self.unit_cell_size
        corner_points = np.array(
            [(0, 0),
            (self.bcc_unit_cell_size, 0),
            (self.bcc_unit_cell_size, self.unit_cell_size),
            (0, self.unit_cell_size)]
        )
        result = (
            cq.Workplane("XY")
            .pushPoints(corner_points)
            .eachpointAdaptive(
                    create_bcc_diagonal_strut,
                    callback_extra_args = [
                        {"unit_cell_size": pseudo_unit_cell_size,
                        "radius": self.strut_radius,
                        "angle_x": - angle_CAD,
                        "angle_y": angle_C1AD},
                        {"unit_cell_size": 0.5 * pseudo_unit_cell_size,
                        "radius": self.strut_radius,
                        "angle_x": - angle_CAD,
                        "angle_y": - angle_C1AD},
                        {"unit_cell_size": 0.5 * pseudo_unit_cell_size,
                        "radius": self.strut_radius,
                        "angle_x": angle_CAD,
                        "angle_y": - angle_C1AD},
                        {"unit_cell_size": pseudo_unit_cell_size,
                        "radius": self.strut_radius,
                        "angle_x": angle_CAD,
                        "angle_y": angle_C1AD}
                        ],
                    useLocalCoords = True
                    )
            )
        return result
    
    # Creates 4 nodes at the XY plane of each unit cell
    def __create_bcc_top_nodes(self,
        delta = 0.01 # a small coefficient is needed because CQ thinks that it cuts through emptiness
        ):
        added_node_diameter = self.node_diameter + delta
        result = cq.Workplane("XY")
        corner_points = np.array(
            [(self.bcc_unit_cell_size, 0),
            (self.bcc_unit_cell_size, self.unit_cell_size),
            (0, self.unit_cell_size)]
        )
        for point in corner_points:
            if point[0] == self.bcc_unit_cell_size:
                result = (result
                        .union(
                            cq.Workplane()
                            .transformed(offset = cq.Vector(point[0], point[1], 0))
                            .box(added_node_diameter, added_node_diameter, added_node_diameter)
                            .edges("|Z")
                            .fillet(self.node_radius)
                            .edges("|X")
                            .fillet(self.node_radius)
                            )
                        )
            if point[0] == 0:
                result = (result
                        .union(
                            cq.Workplane()
                            .transformed(offset = cq.Vector(point[0], point[1], self.bcc_unit_cell_size))
                            .box(added_node_diameter, added_node_diameter, added_node_diameter)
                            .edges("|Z")
                            .fillet(self.node_radius)
                            .edges("|X")
                            .fillet(self.node_radius)
                            )
                        )
        result = (result
                .union(
                    cq.Workplane()
                    .transformed(offset = cq.Vector(0.5 * self.bcc_unit_cell_size ,
                                                    0.5 * self.unit_cell_size ,
                                                    0.5 * self.bcc_unit_cell_size ))
                    .box(added_node_diameter, added_node_diameter, added_node_diameter)
                    .edges("|Z")
                    .fillet(self.node_radius)
                    .edges("|X")
                    .fillet(self.node_radius)
                    )
                )
        return result
    
    # Creates 4 nodes at the XY plane of each unit cell
    def __create_bcc_left_nodes(self,
        delta = 0.01 # a small coefficient is needed because CQ thinks that it cuts through emptiness
        ):
        added_node_diameter = self.node_diameter + delta
        result = cq.Workplane("XY")
        corner_points = np.array(
            [(self.bcc_unit_cell_size, 0)]
        )
        for point in corner_points:
            result = (result
                      .union(
                          cq.Workplane()
                          .transformed(offset = cq.Vector(point[0], point[1], self.bcc_unit_cell_size))
                          .box(added_node_diameter, added_node_diameter, added_node_diameter)
                          .edges("|Z")
                          .fillet(self.node_radius)
                          .edges("|X")
                          .fillet(self.node_radius)
                          )
                      )
        result = (result
                .union(
                    cq.Workplane()
                    .transformed(offset = cq.Vector(0.5 * self.bcc_unit_cell_size ,
                                                    0.5 * self.unit_cell_size ,
                                                    0.5 * self.bcc_unit_cell_size ))
                    .box(added_node_diameter, added_node_diameter, added_node_diameter)
                    .edges("|Z")
                    .fillet(self.node_radius)
                    .edges("|X")
                    .fillet(self.node_radius)
                    )
                )
        return result
    
    def __bcc_top_edge(self, location):
        result = cq.Workplane("XY")
        result = result.union(self.__bcc_top_diagonals())
        result = result.union(self.__create_bcc_top_nodes())
        return result.val().located(location)
    
    def __bcc_left_edge(self, location):
        result = cq.Workplane("XY")
        result = result.union(self.__bcc_left_diagonals())
        result = result.union(self.__create_bcc_left_nodes())
        return result.val().located(location)
    
    def __bcc_martensite(self):
        UC_pnts = []
        self.Nx = self.Nz + self.uc_break - 1
        for i in range(self.Nz * 2):
            for j in range(self.Ny):
                for k in range(self.Nz):
                    if k - 1 < i and i != k and i < self.Nz * 2 - 1 -k:
                        UC_pnts.append(
                            (i * self.bcc_unit_cell_size,
                            j * self.unit_cell_size,
                            k * self.bcc_unit_cell_size))
        print(UC_pnts)
        print("BCC datapoints generated")
        result = cq.Workplane().tag('base')
        result = result.transformed(offset = cq.Vector(- self.unit_cell_size, 0, 0))
        result = result.transformed(rotate = cq.Vector(0, - 45, 0))
        result = result.pushPoints(UC_pnts)
        unit_cell_params = []
        for i in range(self.Nx * self.Ny):
            for j in range(self.Nz):
                unit_cell_params.append({})
        result = result.eachpointAdaptive(self.__bcc_unit_cell,
                                callback_extra_args = unit_cell_params,
                                useLocalCoords = True)
        # top edge bcc
        bcc_top_edge_uc_pnts = []
        for i in range(self.Nz * 2):
            for j in range(self.Ny):
                for k in range(self.Nz):
                    if k - 1 < i and i != k and i == self.Nz * 2 - 1 -k:
                        bcc_top_edge_uc_pnts.append(
                            (i * self.bcc_unit_cell_size,
                            j * self.unit_cell_size,
                            k * self.bcc_unit_cell_size))
        bcc_top_edge = cq.Workplane().tag('base')
        bcc_top_edge = bcc_top_edge.transformed(offset = cq.Vector(- self.unit_cell_size, 0, 0))
        bcc_top_edge = bcc_top_edge.transformed(rotate = cq.Vector(0, - 45, 0))
        bcc_top_edge = bcc_top_edge.pushPoints(bcc_top_edge_uc_pnts)
        bcc_top_edge = bcc_top_edge.eachpointAdaptive(self.__bcc_top_edge,
                                callback_extra_args = unit_cell_params,
                                useLocalCoords = True)
        # left edge bcc
        bcc_left_edge_uc_pnts = []
        for i in range(self.Nz * 2):
            for j in range(self.Ny):
                for k in range(self.Nz):
                    if k - 1 < i and i == k and i < self.Nz * 2 - 1 -k:
                        bcc_left_edge_uc_pnts.append(
                            (i * self.bcc_unit_cell_size,
                            j * self.unit_cell_size,
                            k * self.bcc_unit_cell_size))
        bcc_left_edge = cq.Workplane().tag('base')
        bcc_left_edge = bcc_left_edge.transformed(offset = cq.Vector(- self.unit_cell_size, 0, 0))
        bcc_left_edge = bcc_left_edge.transformed(rotate = cq.Vector(0, - 45, 0))
        bcc_left_edge = bcc_left_edge.pushPoints(bcc_left_edge_uc_pnts)
        bcc_left_edge = bcc_left_edge.eachpointAdaptive(self.__bcc_left_edge,
                                callback_extra_args = unit_cell_params,
                                useLocalCoords = True)
        result = result.union(bcc_top_edge)
        result = result.union(bcc_left_edge)
        print("The BCC lattice section is generated")
        return result
    

    ################################################################
    # Build
    ################################################################

    def build(self):
        result = cq.Workplane().tag('base')
        result = result.union(self.__fcc_martensite()
                              .union(self.__fcc_transition())
                              .union(self.__bcc_martensite()))
        return result

lattice = martensite(unit_cell_size,
                    strut_diameter,
                    node_diameter,
                    Ny, Nz, uc_break)

result = lattice.build()
