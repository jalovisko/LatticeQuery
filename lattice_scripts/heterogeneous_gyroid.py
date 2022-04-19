# Python
import cadquery as cq

from parfunlib.topologies.gyroid import gyroid_heterogeneous_lattice
from parfunlib.commons import make_support_plate
cq.Workplane.gyroid_heterogeneous_lattice = gyroid_heterogeneous_lattice

# BEGIN USER INPUT

min_thickness = 0.3104 * 10
max_thickness = 0.3104 * 10
unit_cell_size = 4 * 10
Nx = 2
Ny = 2
Nz = 2

# END USER INPUT

gyroid = gyroid_heterogeneous_lattice(unit_cell_size,
                                      min_thickness,
                                      max_thickness,
                                      Nx, Ny, Nz,
                                      direction = 'x')

plate = make_support_plate(
    Nx, Ny, Nz,
    unit_cell_size,
    5,
    10
    )