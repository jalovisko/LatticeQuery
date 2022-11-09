from lq.topologies.rco import rco_heterogeneous_lattice
cq.Workplane.rco_heterogeneous_lattice = rco_heterogeneous_lattice

# USER INPUT

unit_cell_size = 10
min_strut_diameter = 5.
max_strut_diameter = 1
min_node_diameter = 5.5
max_node_diameter = 1.05
Nx = 1
Ny = 10
Nz = 10
min_truncation = 0.001
max_truncation = 0.999

# END USER INPUT

# Register our custom plugin before use.

#result = unit_cell(unit_cell_size, strut_radius)
result = rco_heterogeneous_lattice(unit_cell_size,
                                    min_strut_diameter, 
                                    max_strut_diameter,
                                    min_node_diameter,
                                    max_node_diameter,
                                    Nx, Ny, Nz,
                                    min_truncation,
                                    max_truncation,
                                    'linear_truncation')