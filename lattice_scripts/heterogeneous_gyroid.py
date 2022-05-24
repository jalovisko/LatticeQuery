# Python
import cadquery as cq

from parfunlib.topologies.gyroid import gyroid_heterogeneous_lattice
from parfunlib.commons import make_support_plate
cq.Workplane.gyroid_heterogeneous_lattice = gyroid_heterogeneous_lattice

# BEGIN USER INPUT

min_thickness = 10.
max_thickness = 10.
unit_cell_size = 100.
Nx = 5
Ny = 5
Nz = 1

# END USER INPUT

gyroid = gyroid_heterogeneous_lattice(unit_cell_size,
                                      min_thickness,
                                      max_thickness,
                                      Nx, Ny, Nz,
                                      direction = 'x')
