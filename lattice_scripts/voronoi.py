"""
(L, H, W, t) = (100.0, 20.0, 20.0, 1.0)
pts = [
    (0, H/2.0, 0),
    (W/2.0, H/2.0, 0),
    (W/2.0, (H/2.0 - t), 0),
    (t/2.0, (H/2.0 - t), 0),
    (t/2.0, (t - H/2.0), 0),
    (W/2.0, (t - H/2.0), 0),
    (W/2.0, H/-2.0, 0),
    (0, H/-2.0, 0)
]
result = cq.Workplane().polyline(pts)
"""

import numpy as np
import scipy

import cadquery as cq

from lq.commons import cylinder_by_two_points, make_sphere

<<<<<<< HEAD
air_traffic_mess = np.random.random_sample((5000000, 3))*465
=======
air_traffic_mess = np.random.random_sample((100000, 3)) * 9
print(f'{len(air_traffic_mess)} seeds generated')
>>>>>>> 74ebf6f0590a6abb5159c91dddb09e0b85c41647
vor = scipy.spatial.Voronoi(air_traffic_mess)

def fits(pt):
    for i in pt:
        if i < 0 or i > 1:
            return False
    return True

<<<<<<< HEAD
=======
print(f'{len(vor.ridge_vertices)} ridges detected')
j = 0
>>>>>>> 74ebf6f0590a6abb5159c91dddb09e0b85c41647
for ridge_indices in vor.ridge_vertices:
    voronoi_ridge_coords = vor.vertices[ridge_indices]
    print(f'Ridge {j} of {len(vor.ridge_vertices)}...')
    j += 1
    for i in range(1, len(voronoi_ridge_coords[...,0])): 
        startPoint = (
            voronoi_ridge_coords[...,0][0],
            voronoi_ridge_coords[...,1][0],
            voronoi_ridge_coords[...,2][0]
            )
        endPoint = (
            voronoi_ridge_coords[...,0][i],
            voronoi_ridge_coords[...,1][i],
            voronoi_ridge_coords[...,2][i]
            )
        if not fits(startPoint) or not fits(endPoint):
            continue
        print(startPoint, endPoint)
        #edge = cq.Edge.makeLine(startPoint, endPoint)
        #show_object(edge)
        radius = 0.01
        beam = cylinder_by_two_points(startPoint, endPoint, radius)
        show_object(beam)
        #sphere = make_sphere(cq.Vector(startPoint), radius)
        #show_object(sphere)
        #sphere = make_sphere(cq.Vector(endPoint), radius)
        #show_object(sphere)

#result = cq.Workplane().polyline(pts)