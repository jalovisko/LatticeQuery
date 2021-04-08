import cadquery as cq
from math import hypot

unit_cell_size = 10
strut_diameter = 1

#sqrt_of_2 = sqrt(2)

hypot2D = hypot(unit_cell_size, unit_cell_size)
hypot3D = hypot(hypot2D, unit_cell_size)
result = cq.Workplane("front") \
     .transformed(offset = cq.Vector(0, 0, 0), 
                  rotate=cq.Vector(45, 45, 0)) \
     .circle(0.25) \
     .extrude(hypot3D)
