from parfunlib.topologies.cubic import cubic_heterogeneous_lattice

# USER INPUT

unit_cell_size = 10
min_strut_diameter = 1
max_strut_diameter = 1
min_node_diameter = 1.1
max_node_diameter = 1.1
Nx = 1
Ny = 1
Nz = 1
min_truncation = 0.01
max_truncation = 0.99
# END USER INPUT

# Register our custom plugin before use.
cq.Workplane.cubic_heterogeneous_lattice = cubic_heterogeneous_lattice

result = cubic_heterogeneous_lattice(unit_cell_size,
                                    min_strut_diameter, 
                                    max_strut_diameter,
                                    min_node_diameter,
                                    max_node_diameter,
                                    Nx, Ny, Nz)
                                    #min_truncation,
                                    #max_truncation,