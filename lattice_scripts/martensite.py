#import cadquery as cq
from parfunlib.commons import eachpointAdaptive
from parfunlib.topologies.fcc import unit_cell, create_diagonal_strut

from math import hypot
import numpy as np
#from parfunlib.topologies.martensite import fcc_martensite

# USER INPUT

unit_cell_size = 10
strut_diameter = 1
node_diameter = 1.1
# Nx = 2
Ny = 1
Nz = 3
uc_break = 2

# END USER INPUT

# Register our custom plugins before use.
cq.Workplane.eachpointAdaptive = eachpointAdaptive
cq.Workplane.unit_cell = unit_cell

class martensite:
    def __init__(self,
                 unit_cell_size: float,
                 strut_diameter: float,
                 node_diameter: float,
                 Ny: int,
                 Nz: int,
                 uc_break: int):
        self.unit_cell_size = unit_cell_size
        self.strut_diameter = strut_diameter
        self.strut_radius = 0.5 * strut_diameter
        self.node_diameter = node_diameter
        self.Ny = Ny
        self.Nz = Nz
        self.uc_break = uc_break - 1
        if self.uc_break < 1:
            raise ValueError('The value of the beginning of the break should larger than 1')

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
        print("Datapoints generated")
        result = cq.Workplane().tag('base')
        result = result.pushPoints(UC_pnts)
        unit_cell_params = []
        for i in range(self.Nx * self.Ny):
            for j in range(self.Nz):
                unit_cell_params.append({"unit_cell_size": self.unit_cell_size,
                    "strut_radius": self.strut_diameter * 0.5,
                    "node_diameter": self.node_diameter,
                    "type": 'fcc'})
        print("The lattice is generated")
        result = result.eachpointAdaptive(unit_cell,
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
            (1, 1),
            (0, 1)]
            )
        result = (
            cq.Workplane("XY")
            .pushPoints(corner_points)
            .eachpointAdaptive(
                create_diagonal_strut,
                callback_extra_args = [
                    {"unit_cell_size": self.unit_cell_size,
                    "radius": self.strut_radius,
                    "angle_x": 0,
                    "angle_y": 45},
                    {"unit_cell_size": self.unit_cell_size * 0.5,
                    "radius": self.strut_radius,
                    "angle_x": 0,
                    "angle_y": - 45},
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
            if point[0] == 1:
                result = (result
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
        half_unit_cell_size = self.unit_cell_size / 2
        middle_points = self.unit_cell_size * np.array(
            [(0.5, 0),
            (1, 0.5),
            (0.5, 1)]
        )
        for point in middle_points:
            result = (result
                    .union(
                        cq.Workplane()
                        .transformed(offset = cq.Vector(point[0], point[1], half_unit_cell_size))
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
        for i in range(self.Nx):
            for j in range(self.Ny):
                for k in range(self.Nz):
                    if k - 1 == i:
                        UC_pnts.append(
                            (i * self.unit_cell_size,
                            j * self.unit_cell_size,
                            k * self.unit_cell_size))
        print("Datapoints generated")
        result = cq.Workplane().tag('base')
        result = result.pushPoints(UC_pnts)
        unit_cell_params = []
        for i in range(self.Nx * self.Ny):
            for j in range(self.Nz):
                unit_cell_params.append({"unit_cell_size": self.unit_cell_size,
                    "strut_radius": self.strut_diameter * 0.5,
                    "node_diameter": self.node_diameter,
                    "type": 'fcc'})
        print("The lattice is generated")
        result = result.eachpointAdaptive(self.__fcc_transition_unit_cell,
                                            useLocalCoords = True)
        return result 


    def build(self):
        result = cq.Workplane().tag('base')
        result = result.union(self.__fcc_martensite()).union(self.__fcc_transition())
        return result

lattice = martensite(unit_cell_size,
                    strut_diameter,
                    node_diameter,
                    Ny, Nz, uc_break)

result = lattice.build()