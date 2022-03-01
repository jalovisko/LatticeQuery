from parfunlib.topologies.fbcc import fbcc_heterogeneous_lattice
from parfunlib.commons import eachpointAdaptive
# USER INPUT

unit_cell_size = 10
min_strut_diameter = 1
max_strut_diameter = 1
min_node_diameter = 1.1
max_node_diameter = 1.1
Nx = 1
Ny = 1
Nz = 1

# END USER INPUT

# Register our custom plugin before use.
cq.Workplane.fbcc_heterogeneous_lattice = fbcc_heterogeneous_lattice

#result = unit_cell(unit_cell_size, strut_radius)
result = fbcc_heterogeneous_lattice(unit_cell_size,
                                    min_strut_diameter, 
                                    max_strut_diameter,
                                    min_node_diameter,
                                    max_node_diameter,
                                    Nx, Ny, Nz)