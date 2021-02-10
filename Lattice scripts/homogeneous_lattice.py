import cadquery as cq

strut_diameeter = 1.0
unit_cell_size = 10.0
node_diameter = 2.0
delta = 0.01 # a small coefficient is needed because CQ thinks that it cuts through emptiness
strut_radius = strut_diameeter / 2.0
half_unit_cell_size = unit_cell_size / 2.0

def createUnitCells(self):
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

UC = cq.Workplane("XY").pushPoints([(0, 0), (unit_cell_size, 0)]).createUnitCells()

"""
# Defining the nodes
added_node_diameter = node_diameter + delta
node_radius = node_diameter / 2.0
bottom_nodes = (cq.Workplane("XY")
                .rarray(unit_cell_size, unit_cell_size, 2, 2, True) # bottom plane, 4 nodes
                .box(added_node_diameter, added_node_diameter, added_node_diameter)
                .edges("|Z")
                .fillet(node_radius)
                .edges("|X")
                .fillet(node_radius))
top_nodes = (cq.Workplane("XY",
                          origin = (0, 0, unit_cell_size))
             .rarray(unit_cell_size, unit_cell_size, 2, 2, True) # top plane, 4 nodes
             .box(added_node_diameter, added_node_diameter, added_node_diameter)
             .edges("|Z")
             .fillet(node_radius)
             .edges("|X")
             .fillet(node_radius))

"""