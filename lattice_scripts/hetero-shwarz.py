# Python
import cadquery as cq
import time
from lq.topologies.schwartz import schwartz_p_heterogeneous_lattice
cq.Workplane.schwartz_p_heterogeneous_lattice = schwartz_p_heterogeneous_lattice
# import schwartz_d_heterogeneous_lattice instead for
# the Schwarz D surface

# BEGIN USER INPUT

unit_cell_size = 3.98
Nx = 1
Ny = 1
Nz = 1
min_thickness = 0.9
max_thickness = 2.1
# END USER INPUT

#timing performance
start_time = time.time()
schwartz = schwartz_p_heterogeneous_lattice(unit_cell_size,min_thickness,
                                            max_thickness,
                                            Nx, Ny, Nz
                                            #rule = 'sin'
                                            #rule = 'parabola'
                                      )
print('The excecution time is:  %s seconds'  % (time.time() - start_time))
