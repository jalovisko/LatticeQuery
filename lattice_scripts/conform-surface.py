import cadquery as cq
import numpy as np
from math import sin, sqrt

from lq.commons import cylinder_by_two_points, make_sphere

dia = 2
x = 0
y = 0
z = 0

offset = 2

t = np.arange(0.0, 25.0, 0.25)
f = 5*np.sin(t)/t
df = (t * np.cos(t) - np.sin(t))/(t*t)
slope = - 1/df

pts=[]
g_pts1=[]
g_pts2=[]
for idx, x in enumerate(t):
    y = f[idx]
    if x == 0:
        y = 1.0 * 5
        pts += [(x, y, z)]
        g_pts1 += [(x, y + offset, z)]
        g_pts2 += [(x, y - offset, z)]
    else:
        y = f[idx]
        pts += [(x, y, z)]
        k = slope[idx]
        A = 1 + k*k
        B = x + k * k * x
        C = x * x + k * k * x * x - offset * offset
        xg1 = (2 * B + sqrt((4*B*B - 4*A*C))) / (2*A)
        xg2 = (2 * B - sqrt((4*B*B - 4*A*C))) / (2*A)
        pre_yg1 = k * (xg1 - x) + y
        pre_yg2 = k * (xg2 - x) + y
        if pre_yg1 >= pre_yg2:
            yg1 = pre_yg1
            yg2 = pre_yg2
        else:
            yg1 = pre_yg2
            yg2 = pre_yg1
        g_pts1 += [(xg1, yg1, z)]
        g_pts2 += [(xg2, yg2, z)]

#pts = [(x, y, z),
#       (x+5, y, z),
#       (x+10, y+2.5, z),
#       (x+15, y, z),
#       (x+20, y+5,z),
#       (x+25, y+7.5,z),
#       (x+27.5,y+5,z)]
path = cq.Workplane("XY").spline(pts)

sweep = (cq.Workplane("XY")
    .pushPoints([path.val().locationAt(0)]).circle(0.25)
    .pushPoints([path.val().locationAt(1)]).circle(0.75)
    .consolidateWires()
    .sweep(path,multisection=True)
    )

path_g1 = cq.Workplane("XY").spline(g_pts1)
sweep_g2 = (cq.Workplane("XY")
    .pushPoints([path_g1.val().locationAt(0)]).circle(0.25)
    .pushPoints([path_g1.val().locationAt(1)]).circle(0.75)
    .consolidateWires()
    .sweep(path_g1,multisection=True)
    )


#path_g2 = cq.Workplane("XY").spline(g_pts2)
#sweep_g2 = (cq.Workplane("XY")
#    .pushPoints([path_g2.val().locationAt(0)]).circle(0.25)
#    .pushPoints([path_g2.val().locationAt(1)]).circle(0.75)
#    .consolidateWires()
#    .sweep(path_g1,multisection=True)
#    )