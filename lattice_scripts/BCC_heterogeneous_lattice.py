from lq.topologies.bcc import bcc_heterogeneous_lattice
import time

# USER INPUT

unit_cell_size = 10
min_strut_diameter = 0.8
max_strut_diameter = 5.
min_node_diameter = 0.88
max_node_diameter = 5.5
Nx = 4
Ny = 4
Nz = 20

# END USER INPUT

# Register our custom plugin before use.
cq.Workplane.bcc_heterogeneous_lattice = bcc_heterogeneous_lattice

#result = unit_cell(unit_cell_size, strut_radius)
#timing performance
start_time = time.time()
result = bcc_heterogeneous_lattice(unit_cell_size,
                                    min_strut_diameter, 
                                    max_strut_diameter,
                                    min_node_diameter,
                                    max_node_diameter,
                                    Nx, Ny, Nz,
                                    topology = 'bcc',
                                    rule = 'parabola'
                                    )
print('The excecution time is:  %s seconds'  % (time.time() - start_time))
