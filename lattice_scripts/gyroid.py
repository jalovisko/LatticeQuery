# Python
import numpy as np
from numpy import sin, cos, pi
from skimage import measure
from math import sqrt
import cadquery as cq
from cadquery import Shape

AG = 2.8
AFT = 0.15
HCD = 95.
AFW = 13.
NCD = 7
AFL = 150.

# DEFINE GEOMETRY EQUATION
def gyroid(x, y, z, t = 0):
    return cos(x)*sin(y) + cos(y)*sin(z) + cos(z)*sin(x) - t # Gyroïd

# GEOMETRY EQUATION SPECIFIC PARAMETERS
lattice_param = 1. # Gyroid
resolution= 6j # Gyroid (>6 crashes)
tol = 1. # Gyroid
# GENERATE POINTS
spc = np.array([1., 1., 1.]) / sqrt(2) * (AG + 2*AFT) # sets fin gap and stretching
strut_param = 0.
res = int(np.imag(resolution))
x, y, z = pi/2 * np.mgrid[-1:1:resolution, -1:1:resolution, -1:1:resolution] * lattice_param 
vol = gyroid(x, y, z) # All
# TRANSFORM VOLUME INTO SURFACE POINTS
verts, faces, norm, val = measure.marching_cubes_lewiner(vol, spacing=(1., 1., 1.))
xv, yv, zv = verts[:, 0], verts[:, 1], verts[:, 2]
xvm, yvm, zvm = max(xv), max(yv), max(zv)
# CENTER
gxyz  = np.array([ [(x-xvm/2)/xvm * spc[0], (y-yvm/2)/yvm * spc[1], (z-zvm/2)/zvm * spc[2]] for x,y,z in zip(xv, yv, zv) ]) 
xmax, ymax, zmax = max(gxyz[:,0]), max(gxyz[:,1]), max(gxyz[:,2]) 
xmin, ymin, zmin = min(gxyz[:,0]), min(gxyz[:,1]), min(gxyz[:,2])
# FIND SURFACE EDGES
NS = 6 # number of surface sides
bounds_L = [xmax, ymin, zmax, xmin, ymax, zmin]
corners_L = np.array([[0.,0.,0.]]) 
gxyz = np.append(gxyz, corners_L, axis=0)
i_L = [0, 1, 2, 0, 1, 2] # axis order
x_L = [2, 0, 1, 2, 0, 1] # opposite axis order
l_L = [zmin, xmin, ymin, zmin, xmin, ymin] # opposite axis minimums
gm_L = []
im_L = ()
for i in range(NS):
    m = bounds_L[i]
    im = np.where(np.isclose(m, gxyz[:,i_L[i]]) & (np.sign(m) * gxyz[:,x_L[i]] <= (1.-tol) * l_L[i])) # Eliminate points from other edges
    im_L = im_L + im
    gm = gxyz[im]
    gm_max = gm[np.argsort(np.linalg.norm(gm, axis=1))[-1]]
    gmo = list(gm[ np.argsort(np.linalg.norm(gm-gm_max, axis=1)) ])
    gm_L.append(gmo)
gx_max, gz_min, gy_max, gx_min, gz_max, gy_min = gm_L
xyz_max = gx_max + gz_min[::-1] + gy_max + gx_min[::-1] + gz_max + gy_min[::-1]

# Eliminate edge points from interpolation points (otherwise crashes)
gxyz = np.array([pt for pt in gxyz if pt[0]<xmax if pt[0]>xmin if pt[1]<ymax if pt[1]>ymin if pt[2]<zmax if pt[2]>zmin])
print(gxyz)
# Create interpolated surface
#fin = cq.Workplane('XY').interpPlate(surf_edges = gxyz,
#                                     surf_pts = xyz_max,
#                                     thickness = AFT)

# Gyroïd, all edges are splines on different workplanes.

thickness = 0.1
edge_points = [
    [[3.54, 3.54], [1.77, 0.0], [3.54, -3.54]],
    [[-3.54, -3.54], [0.0, -1.77], [3.54, -3.54]],
    [[-3.54, -3.54], [0.0, -1.77], [3.54, -3.54]],
    [[-3.54, -3.54], [-1.77, 0.0], [-3.54, 3.54]],
    [[3.54, 3.54], [0.0, 1.77], [-3.54, 3.54]],
    [[3.54, 3.54], [0.0, 1.77], [-3.54, 3.54]],
]
plane_list = ["XZ", "XY", "YZ", "XZ", "YZ", "XY"]
offset_list = [-3.54, 3.54, 3.54, 3.54, -3.54, -3.54]
edge_wire = (
    cq.Workplane(plane_list[0]).workplane(offset=-offset_list[0]).spline(edge_points[0])
)
for i in range(len(edge_points) - 1):
    edge_wire = edge_wire.add(
        cq.Workplane(plane_list[i + 1])
        .workplane(offset=-offset_list[i + 1])
        .spline(edge_points[i + 1])
    )
surface_points = [[0, 0, 0]]
plate_4 = cq.Workplane("XY").interpPlate(edge_wire, surface_points, thickness)
print("plate_4.val().Volume() = ", plate_4.val().Volume())
plate_4 = plate_4.translate((0, 5 * 12, 0))


#show_object(fin)
#fin.val().exportStep('Gyroid_Cell.stp')
