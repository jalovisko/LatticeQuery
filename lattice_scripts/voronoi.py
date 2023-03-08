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

air_traffic_mess = np.random.random_sample((50, 3))
vor = scipy.spatial.Voronoi(air_traffic_mess)

def fits(pt):
    for i in pt:
        if i < 0 or i > 1:
            return False
    return True
for ridge_indices in vor.ridge_vertices:
    voronoi_ridge_coords = vor.vertices[ridge_indices]
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
            pass
        print(startPoint, endPoint)
        edge = cq.Edge.makeLine(startPoint, endPoint)
        show_object(edge)
    #edges.append(edge)

#result = cq.Workplane().polyline(pts)