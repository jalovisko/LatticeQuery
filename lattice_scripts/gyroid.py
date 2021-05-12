# Python
import cadquery as cq

from parfunlib.topologies.gyroid import gyroid_homogeneous_lattice

# BEGIN USER INPUT

thickness = 0.1
unit_cell_size = 10
Nx = 3
Ny = 3
Nz = 3

# END USER INPUT

gyroid = gyroid_homogeneous_lattice(thickness,
                                    unit_cell_size,
                                    Nx, Ny, Nz)

