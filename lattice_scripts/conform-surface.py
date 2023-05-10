import cadquery as cq
import numpy as np
from math import sin, sqrt

from lq.commons import cylinder_by_two_points, make_sphere

# Set initial parameters
dia = 2
x = 0
y = 0
z = 0

offset = 2

# Create a numpy array with a range of 0 to 25 with a step of 0.25
t = np.arange(0.0, 25.0, 0.25)

# Calculate f(t) and df(t) using given formulas
f = 5*np.sin(t)/t
df = (t * np.cos(t) - np.sin(t))/(t*t)

# Calculate slope using df(t)
slope = - 1/df

# Set diameters and unit cell parameters
d_min = 0.125
d_max = 0.75
Nx = 10 # number of unit cells along X
hz = 3 # height along Z

# Initialize lists to store coordinates
pts=[]
g_pts1=[]
g_pts2=[]

# Calculate coordinates and store them in the lists
for idx, x in enumerate(t):
    y = f[idx]
    if x == 0:
        # adds a coordinate to pts, g_pts1, and g_pts2
        y = 1.0 * 5
        pts += [(x, y, z)]
        g_pts1 += [(x, y + offset, z)]
        g_pts2 += [(x, y - offset, z)]
    else:
        # calculates the necessary values for xg1, yg1, xg2, and yg2
        # using some mathematical formulas
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

# Create a spline path with the coordinates in pts
path = cq.Workplane("XY").spline(pts)

# Create a sweep along the path with varying diameters
sweep = (cq.Workplane("XY")
    .pushPoints([path.val().locationAt(0)]).circle(d_min)
    .pushPoints([path.val().locationAt(1)]).circle(d_max)
    .consolidateWires()
    .sweep(path,multisection=True)
    )

# Create a spline path with the coordinates in g_pts1 and
# create a sweep along the path
path_g1 = cq.Workplane("XY").spline(g_pts1)
sweep_g1 = (cq.Workplane("XY")
    .pushPoints([path_g1.val().locationAt(0)]).circle(d_min)
    .pushPoints([path_g1.val().locationAt(1)]).circle(d_max)
    .consolidateWires()
    .sweep(path_g1,multisection=True)
    )


path_g2 = cq.Workplane("XY").spline(g_pts2)
sweep_g2 = (cq.Workplane("XY")
    .pushPoints([path_g2.val().locationAt(0)]).circle(0.25)
    .pushPoints([path_g2.val().locationAt(1)]).circle(0.75)
    .consolidateWires()
    .sweep(path_g2,multisection=True)
    )

show_object(sweep)
show_object(sweep_g1)
show_object(sweep_g2)

diameters = np.linspace(0.125,0.75,10)
n_pts = int(len(pts) / Nx)
for p, gp1, gp2, d in zip(pts[::n_pts], g_pts1[::n_pts], g_pts2[::n_pts], diameters):
    # Z-struts
    p_o = (p[0], p[1], hz)
    cyl = cylinder_by_two_points(p, p_o, d)
    show_object(cyl)
    gp1_o = (gp1[0], gp1[1], hz)
    cyl = cylinder_by_two_points(gp1, gp1_o, d)
    show_object(cyl)
    gp2_o = (gp2[0], gp2[1], hz)
    cyl = cylinder_by_two_points(gp2, gp2_o, d)
    show_object(cyl)
    # Y-struts
    cyl = cylinder_by_two_points(p, gp1, d)
    show_object(cyl)
    cyl = cylinder_by_two_points(p, gp2, d)
    show_object(cyl)