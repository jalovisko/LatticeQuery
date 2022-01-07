#import cadquery as cq
from parfunlib.commons import eachpointAdaptive
from parfunlib.topologies.fcc import unit_cell
#from parfunlib.topologies.martensite import fcc_martensite

# USER INPUT

unit_cell_size = 10
strut_diameter = 1
node_diameter = 1.1
# Nx = 2
Ny = 1
Nz = 7
uc_break = 3

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
        self.node_diameter = node_diameter
        self.Ny = Ny
        self.Nz = Nz
        self.uc_break =uc_break
        
    def __fcc_martensite(self):
        if self.uc_break < 1:
            raise ValueError('The value of the beginning of the break should larger than 1')
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
        self.result = cq.Workplane().tag('base')
        self.result = self.result.pushPoints(UC_pnts)
        unit_cell_params = []
        for i in range(self.Nx * self.Ny):
            for j in range(self.Nz):
                unit_cell_params.append({"unit_cell_size": self.unit_cell_size,
                    "strut_radius": self.strut_diameter * 0.5,
                    "node_diameter": self.node_diameter,
                    "type": 'fcc'})
        self.result = self.result.eachpointAdaptive(unit_cell,
                                            callback_extra_args = unit_cell_params,
                                            useLocalCoords = True)
        print("The lattice is generated")
        
    def build(self):
        self.__fcc_martensite()
        return self.result

lattice = martensite(unit_cell_size,
                    strut_diameter,
                    node_diameter,
                    Ny, Nz, uc_break)

result = lattice.build()