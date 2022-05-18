# Python
import cadquery as cq

from parfunlib.topologies.gyroid import gyroid_homogeneous_lattice
cq.Workplane.gyroid_homogeneous_lattice = gyroid_homogeneous_lattice

# BEGIN USER INPUT

thickness = 0.1
unit_cell_size = 10
Nx = 1
Ny = 1
Nz = 1

# END USER INPUT

gyroid = gyroid_homogeneous_lattice(unit_cell_size, thickness,
                                    Nx, Ny, Nz)

box = cq.Workplane().transformed(
    tuple([0.5 * unit_cell_size] * 3)).box(
        unit_cell_size, unit_cell_size, unit_cell_size)