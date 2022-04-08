# Python
import cadquery as cq

from parfunlib.topologies.gyroid import gyroid_heterogeneous_lattice
cq.Workplane.gyroid_heterogeneous_lattice = gyroid_heterogeneous_lattice

# BEGIN USER INPUT

min_thickness = 0.3104 * 2
max_thickness = 0.3104 * 2
unit_cell_size = 5 * 2
Nx = 5
Ny = 5
Nz = 5

# END USER INPUT

gyroid = gyroid_heterogeneous_lattice(unit_cell_size,
                                      min_thickness,
                                      max_thickness,
                                      Nx, Ny, Nz,
                                      direction = 'x')
