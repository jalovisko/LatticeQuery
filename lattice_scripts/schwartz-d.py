# Python
import cadquery as cq
from math import cos, sqrt
import numpy as np
import time
from lq.topologies.schwartz import schwartz_d_heterogeneous_lattice
cq.Workplane.schwartz_d_heterogeneous_lattice = schwartz_d_heterogeneous_lattice

# BEGIN USER INPUT

unit_cell_size = 20
Nx = 1
Ny = 1
Nz = 20
min_thickness = 0.2
max_thickness = 3
# END USER INPUT

#timing performance
start_time = time.time()

result = schwartz_d_heterogeneous_lattice(unit_cell_size, min_thickness, max_thickness,
                                      Nx, Ny, Nz,
                                      rule = 'sin'
                                      )

print('The excecution time is:  %s seconds'  % (time.time() - start_time))
