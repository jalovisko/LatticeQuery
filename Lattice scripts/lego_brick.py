import cadquery as cq

lbumps = 4 # number of bumps long
wbumps = 2 # number of bumps wide
thin = True # True for thin, False for thick

pitch = 8.0
clearance = 0.1
bumpDiam = 4.8
bumpHeight = 1.8
height = 3.2 if thin else 9.6

t = (pitch - (2 * clearance) - bumpDiam) / 2.0
postDiam = pitch - t # works out to 6.5
total_length = lbumps * pitch - 2.0 * clearance
total_width = wbumps * pitch - 2.0 * clearance

s = cq.Workplane("XY").box(total_length, total_width, height)
s = s.faces("<Z").shell(-1.0 * t)
s = s.faces(">Z").workplane(). \
    rarray(pitch, pitch, lbumps, wbumps, True). \
        circle(bumpDiam / 2.0). \
            extrude(height - t)

tmp = s.faces("<Z").workplane(invert = True)

if lbumps > 1 and wbumps > 1:
    tmp = tmp.rarray(pitch, pitch, lbumps - 1, wbumps - 1, center = True). \
        circle(postDiam / 2.0).circle(bumpDiam / 2.0).extrude(height - t)
elif lbumps > 1:
    tmp = tmp.rarray(pitch, pitch, lbumps - 1, 1, center = True). \
        circle(t).extrude(height - t)
elif wbumps > 1:
    tmp = tmp.rarray(pitch, pitch, 1, wbumps - 1, center = True). \
        circle(t).extrude(height - t)
else:
    tmp = s

# replay(tmp)
#result = cq.Workplane("XY" ).box(3, 3, 0.5).edges("|Z").fillet(0.125)