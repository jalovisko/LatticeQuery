from parfunlib.commons import eachpointAdaptive
from parfunlib.topologies.fcc import fcc_heterogeneous_lattice
from parfunlib.topologies.cubic import cubic_heterogeneous_lattice
# USER INPUT

unit_cell_size = 6
min_strut_diameter = 0.8
max_strut_diameter = 0.8
min_node_diameter = 0.85
max_node_diameter = 0.85
Nx = 10
Ny = 1
Nz = 10

# END USER INPUT

# Register our custom plugin before use.
cq.Workplane.fcc_heterogeneous_lattice = fcc_heterogeneous_lattice

#result = unit_cell(unit_cell_size, strut_radius)
fcc = fcc_heterogeneous_lattice(unit_cell_size,
                                    min_strut_diameter, 
                                    max_strut_diameter,
                                    min_node_diameter,
                                    max_node_diameter,
                                    Nx, Ny, Nz
                                    #type = 'sfccz'
                                    #rule = 'sin'
                                    )

cubic = cubic_heterogeneous_lattice(
        unit_cell_size,
        min_strut_diameter,
        max_strut_diameter,
        min_node_diameter,
        max_node_diameter,
        Nx, Ny, Nz
        )