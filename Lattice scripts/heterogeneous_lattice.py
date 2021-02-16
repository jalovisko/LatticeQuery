import cadquery as cq
import numpy as np


min_strut_diameter = 1.0
max_strut_diameter = 2.0
unit_cell_size = 10.0
Nx = 3 # N of cells in X direction
Ny = 3 # N of cells in Y direction
Nz = 3 # N of cells in Z direction

Dn = 2.0 # node diameter

def createUnitCell(self,
                   strut_diameter,
                   unit_cell_size):
    # TODO:
    # This is not optimal because struts of neoghbouring cells
    # intersect and up to 50% more resources are used. Too bad.
    strut_radius = strut_diameter / 2.0
    half_unit_cell_size = unit_cell_size / 2.0
    # The following lines of code weren't particulary easy to write.
    # They are not going to be easy to read either.
    unit_cell = (cq.Workplane("front")
                 # (1) 4 Z struts
                 .rarray(unit_cell_size, unit_cell_size, 2, 2, True)
                  .circle(strut_radius).extrude(unit_cell_size) # make a cylinder
                  # (2) 4 X struts
                  # We want to make a second cylinder perpendicular to the first,
                  # but we have no face to base the workplane off
                  .copyWorkplane(
                      # create a temporary object with the required workplane
                      cq.Workplane("right",
                                   origin = (-half_unit_cell_size, 0, half_unit_cell_size))
                  )
                  .rarray(unit_cell_size, unit_cell_size, 2, 2, True)
                  .circle(strut_radius).extrude(unit_cell_size)
                  # (3) 4 Y struts
                  .copyWorkplane(
                      # create a temporary object with the required workplane
                      cq.Workplane("top",
                                   origin = (0, - half_unit_cell_size, half_unit_cell_size))
                  )
                  .rarray(unit_cell_size, unit_cell_size, 2, 2, True)
                  .circle(strut_radius).extrude(unit_cell_size))
    return self.union(self.eachpoint(lambda loc: unit_cell.val().located(loc), True))
cq.Workplane.createUnitCell = createUnitCell

def createNodes(self,
                node_diameter,
                unit_cell_size,
                delta = 0.01 # a small coefficient is needed because CQ thinks that it cuts through emptiness
                ):
    added_node_diameter = node_diameter + delta
    node_radius = node_diameter / 2.0
    bottom_nodes = (cq.Workplane("XY")
                    .rarray(unit_cell_size, unit_cell_size, 2, 2, True) # bottom plane, 4 nodes
                    .box(added_node_diameter, added_node_diameter, added_node_diameter)
                    .edges("|Z")
                    .fillet(node_radius)
                    .edges("|X")
                    .fillet(node_radius))
    return self.eachpoint(lambda loc: bottom_nodes.val().located(loc), True)
cq.Workplane.createNodes = createNodes

diams = np.linspace(min_strut_diameter, max_strut_diameter, Nx)
pnts = [(i * unit_cell_size, 0) for i in range(Nx)]

UC = cq.Workplane().tag('base')
for pnt, diam in zip(pnts, diams):
    # Generating the positions for each homogeneous layer
    layer_pnts = []
    for i in range(Ny):
        for j in range(Nz):
            layer_pnts.append((0, i * unit_cell_size, j *unit_cell_size))
    UC = (UC
          .workplaneFromTagged('base')
          .center(*pnt)
          .pushPoints(layer_pnts)
          .createUnitCell(diam, unit_cell_size))



#pnts = [(0, 0), (100, 0), (200, 0)]

#UC = cq.Workplane().tag('base')
#for pnt in pnts:
#    UC = UC.workplaneFromTagged('base').center(*pnt).createUnitCell(Ds, UCsize)

"""
# Generating the positions for each unit cell
pts = []
for i in range(Nx):
    for j in range(Ny):
        for k in range(Nz):
            pts.append((i * UCsize, j * UCsize, k * UCsize))


lattice = (cq.Workplane("XY")
           .pushPoints(pts)
           .createUnitCells(Ds, UCsize))

# This monstrosity is needed because createNodes creates
# nodes only at the bottom of each unit cell
# We simply add an 'empty' unit cell layer on top
# and put nodes at the bottom of it.
# Could it be done better? Yes.
k += 1
for i in range(Nx):
    for j in range(Ny):
        pts.append((i * UCsize, j * UCsize, k * UCsize))
        
pts.append((i * UCsize, j * UCsize, k * UCsize))
nodes = (cq.Workplane("XY")
         .pushPoints(pts)
         .createNodes(Dn, UCsize))
"""