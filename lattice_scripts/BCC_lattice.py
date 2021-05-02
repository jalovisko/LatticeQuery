import numpy as np
from topologies.fblgen_helper import eachpointAdaptive
from topologies.BCC import unit_cell

# USER INPUT

unit_cell_size = 10
strut_diameter = 1
node_diameter = 2
Nx = 2
Ny = 2
Nz = 2

# END USER INPUT

strut_radius = strut_diameter / 2.0

cq.Workplane.unit_cell = unit_cell.unit_cell

def BCC_lattice(unit_cell_size, strut_radius, Nx, Ny, Nz):
    UC_pnts = []
    for i in range(Nx):
        for j in range(Ny):
            for k in range(Nz):
                UC_pnts.append((i * unit_cell_size, j * unit_cell_size, k * unit_cell_size))
    result = cq.Workplane().tag('base')
    result = result.pushPoints(UC_pnts)
    result = result.unit_cell(unit_cell_size, strut_radius, node_diameter)
    return result
# Register our custom plugin before use.
#cq.Workplane.BCC_lattice = BCC_lattice

#result = unit_cell(unit_cell_size, strut_radius)
result = BCC_lattice(unit_cell_size, strut_radius, Nx, Ny, Nz)