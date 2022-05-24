# Python
import cadquery as cq
from math import cos, sqrt
import numpy as np
import time
from parfunlib.topologies.schwartz import schwartz_d_heterogeneous_lattice
cq.Workplane.schwartz_d_heterogeneous_lattice = schwartz_d_heterogeneous_lattice

# BEGIN USER INPUT

unit_cell_size = 10
Nx = 5
Ny = 5
Nz = 1
min_thickness = 1.
max_thickness = 1.
# END USER INPUT

#timing performance
start_time = time.time()
schwartz = schwartz_d_heterogeneous_lattice(unit_cell_size, min_thickness, max_thickness,
                                      Nx, Ny, Nz#,
                                      #rule = 'sin'
                                      )
print('The excecution time is:  %s seconds'  % (time.time() - start_time))
