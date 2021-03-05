import cadquery as cq
from random import random

def createLs(self, diam = 10):
    L = cq.Workplane().circle(diam / 2).extrude(- 500)
    L = (L.transformed(offset = cq.Vector(0, 0, - 500))
         .transformed(rotate = cq.Vector(90, 0, 0))
         .circle(diam / 2.0).extrude(- 500))

    return self.union(self.eachpoint(lambda loc: L.val().located(loc), True))

cq.Workplane.createLs = createLs

pnts = []
for i in range(10):
    pnts.append((i * 100, 0))
diams = [5 + 50 * random() for _ in range(len(pnts))]

L2 = cq.Workplane().tag('base')

for pnt, diam in zip(pnts, diams):
    L2 = L2.workplaneFromTagged('base').center(*pnt).createLs(diam)