import cadquery as cq

def cylinder(z_uc, angle_uc_size, z_uz_size, r_uz_size,

                       min_thickness, max_thickness,
                       inner_radius, outer_radius):
    r_uc = (outer_radius - inner_radius) / r_uz_size
    delta_thickness = (max_thickness - min_thickness) / r_uc
    
    t = min_thickness
    arcs = cq.Workplane()
    
    for r in range(inner_radius, outer_radius + 1, r_uz_size):
        for z in range(z_uc + 1):
            arcs = arcs.union(
                cq.Workplane()
                .transformed(offset = cq.Vector(r,
                                                z * z_uz_size,
                                                0))
                .circle(t)
                .revolve(360,
                         [-r, 0, 0],
                         [-r, 1, 0])
                )
    
        t += delta_thickness
    
    t = min_thickness
    radials = cq.Workplane()
    for r in range(inner_radius, outer_radius, r_uz_size):
        for z in range(z_uc + 1):
            for phi in range(0, 360, angle_uc_size):
                radials = radials.union(cq.Workplane()
                            .transformed(rotate = cq.Vector(0,
                                                            phi,
                                                            0))
                            .transformed(offset = cq.Vector(0,
                                                            z * z_uz_size,
                                                            r))
                            .circle(t)
                            .extrude(r_uz_size)
                            )
        t += delta_thickness
    
    
    t = min_thickness
    axials = cq.Workplane()
    for r in range(inner_radius, outer_radius + 1, r_uz_size):
        for phi in range(0, 360, angle_uc_size):
            axials = axials.union(cq.Workplane()
                                  .transformed(rotate = cq.Vector(0,
                                                                  phi,
                                                                  0))
                                  .transformed(offset = cq.Vector(0,
                                                                  0,
                                                                  r))
                                  .transformed(rotate = cq.Vector(- 90,
                                                                  0,
                                                                  0))
                                  .circle(t)
                                  .extrude(z_uc * z_uz_size)
                                  )
        t += delta_thickness
    return arcs, radials, axials