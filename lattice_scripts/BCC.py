import cadquery as cq

result = cq.Workplane("front")  \
     .transformed(offset=cq.Vector(0, -1.5, 1.0),rotate=cq.Vector(60, 0, 0)) \
     .rect(1.5,1.5,forConstruction=True).vertices().circle(0.25).extrude(0.5)