# Python
import cadquery as cq

from parfunlib.topologies.gyroid import gyroid_heterogeneous_lattice
cq.Workplane.gyroid_heterogeneous_lattice = gyroid_heterogeneous_lattice

# BEGIN USER INPUT

min_thickness = 0.4
max_thickness = 1.0
unit_cell_size = 10
Nx = 4
Ny = 3
Nz = 8

# END USER INPUT

gyroid = gyroid_heterogeneous_lattice(unit_cell_size, min_thickness, max_thickness,
                                      Nx, Ny, Nz)
