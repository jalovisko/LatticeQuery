from parfunlib.topologies.bcc import bcc_heterogeneous_lattice

# USER INPUT

unit_cell_size = 10
min_strut_diameter = 0.1
max_strut_diameter = 3
min_node_diameter = 0.11
max_node_diameter = 3.3
Nx = 2
Ny = 2
Nz = 12

# END USER INPUT

# Register our custom plugin before use.
cq.Workplane.bcc_heterogeneous_lattice = bcc_heterogeneous_lattice

#result = unit_cell(unit_cell_size, strut_radius)
result = bcc_heterogeneous_lattice(unit_cell_size,
                                    min_strut_diameter, 
                                    max_strut_diameter,
                                    min_node_diameter,
                                    max_node_diameter,
                                    Nx, Ny, Nz,
                                    rule = 'parabola')