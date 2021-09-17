from parfunlib.topologies.fcc import fcc_heterogeneous_lattice

# USER INPUT

unit_cell_size = 10
min_strut_diameter = 2.5
max_strut_diameter = 2.5
min_node_diameter = 3.7
max_node_diameter = 3.7
Nx = 1
Ny = 1
Nz = 1

# END USER INPUT

# Register our custom plugin before use.
cq.Workplane.fcc_heterogeneous_lattice = fcc_heterogeneous_lattice

#result = unit_cell(unit_cell_size, strut_radius)
result = fcc_heterogeneous_lattice(unit_cell_size,
                                    min_strut_diameter, 
                                    max_strut_diameter,
                                    min_node_diameter,
                                    max_node_diameter,
                                    Nx, Ny, Nz,
                                    type = 'fcc'
                                    #rule = 'sin'
                                    )