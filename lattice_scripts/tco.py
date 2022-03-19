from parfunlib.topologies.tco import tco_heterogeneous_lattice
cq.Workplane.tco_heterogeneous_lattice = tco_heterogeneous_lattice

# USER INPUT

unit_cell_size = 10
min_strut_diameter = 1.00000001
max_strut_diameter = 1
min_node_diameter = 1.1
max_node_diameter = 1.1
Nx = 1
Ny = 1
Nz = 1

# END USER INPUT

# Register our custom plugin before use.


result = tco_heterogeneous_lattice(unit_cell_size,
                                    min_strut_diameter, 
                                    max_strut_diameter,
                                    min_node_diameter,
                                    max_node_diameter,
                                    Nx, Ny, Nz)
