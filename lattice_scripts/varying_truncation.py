from lq.topologies.tcubic import tcubic_heterogeneous_lattice

# USER INPUT

unit_cell_size = 10
min_strut_diameter = 0.5
max_strut_diameter = 4
min_node_diameter = 0.55
max_node_diameter = 4.4
Nx = 10
Ny = 10
Nz = 10
min_truncation = 0.001
max_truncation = 0.999
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
                                    rule = 'linear',
                                    direction = 'X',
                                    truncation = 'linear')