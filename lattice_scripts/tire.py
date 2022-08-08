import cadquery as cq

from lq.commons import eachpointAdaptive
from lqq.topologies.conformal import cylinder

z_uc = 8 # no. of Z unit cell

angle_uc_size = 15 # degrees
z_uz_size = 100 # mm
r_uz_size = 100 # mm

min_thickness = 10 # mm
max_thickness = 40 # mm

inner_radius = 350 # mm
outer_radius = 950 # mm

arcs, radials, axials = cylinder(z_uc,
                                 angle_uc_size,
                                 z_uz_size, r_uz_size,
                                 min_thickness,
                                 max_thickness,
                                 inner_radius,
                                 outer_radius)
