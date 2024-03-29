import cadquery as cq

# User input begins here

Ds = 1.0       # strut diameter
UCsize = 10.0  # unit cell size
Dn = 2.0       # node diameter
Nx = 10        # N of cells in X direction
Ny = 10        # N of cells in Y direction
Nz = 10        # N of cells in Z direction

# User input ends here

def createUnitCells(self,
                    strut_diameeter,
                    unit_cell_size):
    strut_radius = strut_diameeter / 2.0
    half_unit_cell_size = unit_cell_size / 2.0
    # Defining the struts
    unit_cell = (cq.Workplane("front")
              # 1) 4 Z struts
              .rarray(unit_cell_size, unit_cell_size, 2, 2, True)
              .circle(strut_radius).extrude(unit_cell_size) # make a cylinder
              # 2) 4 X struts
              # We want to make a second cylinder perpendicular to the first,
              # but we have no face to base the workplane off
              .copyWorkplane(
                  # create a temporary object with the required workplane
                  cq.Workplane("right",
                               origin = (-half_unit_cell_size, 0, half_unit_cell_size))
              )
              .rarray(unit_cell_size, unit_cell_size, 2, 2, True)
              .circle(strut_radius).extrude(unit_cell_size)
              # 3) 4 Y struts
              .copyWorkplane(
                  # create a temporary object with the required workplane
                  cq.Workplane("top",
                               origin = (0, - half_unit_cell_size, half_unit_cell_size))
              )
              .rarray(unit_cell_size, unit_cell_size, 2, 2, True)
              .circle(strut_radius).extrude(unit_cell_size))
    return self.eachpoint(lambda loc: unit_cell.val().located(loc), True)
cq.Workplane.createUnitCells = createUnitCells

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
# Could it be done better? Yes. Too bad.
k += 1
for i in range(Nx):
    for j in range(Ny):
        pts.append((i * UCsize, j * UCsize, k * UCsize))
        
pts.append((i * UCsize, j * UCsize, k * UCsize))
nodes = (cq.Workplane("XY")
         .pushPoints(pts)
         .createNodes(Dn, UCsize))
