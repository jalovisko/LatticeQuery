import numpy as np

R = 2.5
A = 4*R/70
N = 15

phi = np.arange(0, 2 * np.pi, 0.01)
rho = R + A * np.sin(N * phi)

sPnts = []
for p, r in zip(phi, rho):
    x = 2 * r * np.cos(p)
    y = r * np.sin(p)
    sPnts += [(x, y, 0)]

s = cq.Workplane("XY").moveTo(sPnts[0][0], sPnts[0][1])
r = s.spline(sPnts[1:], includeCurrent = True).close()
result = r.workplane(offset = 10.0).ellipse(2.5, 1.25).loft(combine=True)