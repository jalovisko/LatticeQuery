# Python
import cadquery as cq

from parfunlib.topologies.gyroid import gyroid_unit_cell

# BEGIN USER INPUT

thickness = 0.1
unit_cell_size = 10
Nx = 3
Ny = 3
Nz = 3

# END USER INPUT

gyroid = gyroid_unit_cell(thickness, unit_cell_size)

