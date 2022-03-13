from parfunlib.topologies.tcubic import tcubic_heterogeneous_lattice

# USER INPUT

unit_cell_size = 10
min_strut_diameter = 1
max_strut_diameter = 1
min_node_diameter = 1.1
max_node_diameter = 1.1
Nx = 1
Ny = 1
Nz = 1
min_truncation = 0.4
max_truncation = 0.4
# END USER INPUT

# Register our custom plugin before use.
cq.Workplane.tcubic_heterogeneous_lattice = tcubic_heterogeneous_lattice

result = tcubic_heterogeneous_lattice(unit_cell_size,
                                    min_strut_diameter, 
                                    max_strut_diameter,
                                    min_node_diameter,
                                    max_node_diameter,
                                    Nx, Ny, Nz,
                                    min_truncation,
                                    max_truncation,
                                    rule = 'linear_truncation')