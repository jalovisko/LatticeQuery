# Python
import cadquery as cq
from math import cos, sqrt
import numpy as np
import time
from lq.topologies.schwartz import schwartz_d_heterogeneous_lattice
cq.Workplane.schwartz_d_heterogeneous_lattice = schwartz_d_heterogeneous_lattice
# import schwartz_p_heterogeneous_lattice instead for
# the P surface

# BEGIN USER INPUT

unit_cell_size = 100.*1000
Nx = 1
Ny = 1
Nz = 10
min_thickness = 0.9*1000
max_thickness = 9.*1000
# END USER INPUT

#timing performance
start_time = time.time()
schwartz = schwartz_d_heterogeneous_lattice(unit_cell_size, min_thickness, max_thickness,
                                      Nx, Ny, Nz#,
                                      #rule = 'sin'
                                      )
print('The excecution time is:  %s seconds'  % (time.time() - start_time))
