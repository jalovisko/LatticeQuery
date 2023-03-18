import cadquery as cq

from lq.commons import cylinder_by_two_points, make_sphere

dia = 2
x = 0
y = 0
z = 0

pts = [(x, y, z),
       (x+5, y, z),
       (x+10, y+2.5, z),
       (x+15, y, z),
       (x+20, y+5,z),
       (x+25, y+7.5,z),
       (x+27.5,y+5,z)]
path= cq.Workplane("XY").spline(pts)

sweep = (cq.Workplane("XY")
    .pushPoints([path.val().locationAt(0)]).circle(0.25)
    .pushPoints([path.val().locationAt(1)]).circle(0.75)
    .consolidateWires()
    .sweep(path,multisection=True)
    )