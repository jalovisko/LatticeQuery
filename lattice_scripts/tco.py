from parfunlib.topologies.tco import tco_heterogeneous_lattice
cq.Workplane.tco_heterogeneous_lattice = tco_heterogeneous_lattice

# USER INPUT

unit_cell_size = 10
min_strut_diameter = 0.5
max_strut_diameter = 0.5
min_node_diameter = 1.1
max_node_diameter = 1.1
Nx = 1
Ny = 1
Nz = 1
truncation = 0.5

# END USER INPUT

# Register our custom plugin before use.

#result = unit_cell(unit_cell_size, strut_radius)

result = tco_heterogeneous_lattice(unit_cell_size,
                                    min_strut_diameter, 
                                    max_strut_diameter,
                                    min_node_diameter,
                                    max_node_diameter,
                                    Nx, Ny, Nz,
                                    truncation)
