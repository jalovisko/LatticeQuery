# Python
import cadquery as cq

from lq.topologies.gyroid import gyroid_homogeneous_lattice
cq.Workplane.gyroid_homogeneous_lattice = gyroid_homogeneous_lattice

# BEGIN USER INPUT

thickness = 0.1
unit_cell_size = 10
Nx = 2
Ny = 2
Nz = 2

# END USER INPUT

gyroid = gyroid_homogeneous_lattice(unit_cell_size, thickness,
                                    Nx, Ny, Nz)
