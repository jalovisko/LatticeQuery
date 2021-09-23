# Python
import cadquery as cq

from math import cos, sqrt
import numpy as np

from parfunlib.topologies.schwartz import schwartz_heterogeneous_lattice
cq.Workplane.schwartz_heterogeneous_lattice = schwartz_heterogeneous_lattice

# BEGIN USER INPUT

unit_cell_size = 10
Nx = 1
Ny = 1
Nz = 1
min_thickness = 1
max_thickness = 1
# END USER INPUT

schwartz = schwartz_heterogeneous_lattice(unit_cell_size, min_thickness, max_thickness,
                                      Nx, Ny, Nz)
