import cadquery as cq
from parfunlib.commons import eachpointAdaptive
from parfunlib.topologies.bcc import bcc_heterogeneous_lattice
import time

# USER INPUT

unit_cell_size = 10
min_strut_diameter = 1
max_strut_diameter = 1
min_node_diameter = 1
max_node_diameter = 1
Nx = 1
Ny = 1
Nz = 1

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
                                    topology = 'bcc'
                                    #rule = 'parabola'
                                    )
print('The excecution time is:  %s seconds'  % (time.time() - start_time))
