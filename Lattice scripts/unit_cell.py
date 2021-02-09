import cadquery as cq

strut_diameeter = 1.0
unit_cell_size = 10.0
node_diameter = 2.0

strut_radius = strut_diameeter / 2.0

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
                           origin=(- unit_cell_size / 2.0, 0, unit_cell_size / 2.0))
          )
          .rarray(unit_cell_size, unit_cell_size, 2, 2, True)
          .circle(strut_radius).extrude(unit_cell_size)
          # 3) 4 Y struts
          .copyWorkplane(
              # create a temporary object with the required workplane
              cq.Workplane("top",
                           origin=(0, - unit_cell_size / 2.0, unit_cell_size / 2.0))
          )
          .rarray(unit_cell_size, unit_cell_size, 2, 2, True)
          .circle(strut_radius).extrude(unit_cell_size))

# Defining the nodes
#sphere = cq.Workplane("XY").threePointArc((1.0, 1.0), (0.0, 2.0)).close().revolve()
#nodes = cd