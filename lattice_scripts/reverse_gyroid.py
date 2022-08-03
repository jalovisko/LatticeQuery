# Python
import cadquery as cq

from lq.topologies.gyroid import gyroid_heterogeneous_lattice
from lq.commons import make_support_plate
cq.Workplane.gyroid_heterogeneous_lattice = gyroid_heterogeneous_lattice

# BEGIN USER INPUT

min_thickness = 0.3104 * 10
max_thickness = 0.3104 * 10
unit_cell_size = 4 * 10
Nx = 1
Ny = 1
Nz = 1

# END USER INPUT

gyroid = gyroid_heterogeneous_lattice(unit_cell_size,
                                      min_thickness,
                                      max_thickness,
                                      Nx, Ny, Nz,
                                      direction = 'x')

box = cq.Workplane().transformed(
    offset = tuple([0.5*unit_cell_size]*3)).box(
        unit_cell_size*0.8, unit_cell_size*0.8, unit_cell_size*0.8)
        
cfd = box -gyroid