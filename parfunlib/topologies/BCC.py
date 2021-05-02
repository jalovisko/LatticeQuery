from ..commons import eachpointAdaptive

from math import hypot, acos, degrees
import numpy as np

import cadquery as cq

# Register our custom plugins before use.
cq.Workplane.eachpointAdaptive = eachpointAdaptive

# The angle is chosen with respect to the positive X direction
def create_diagonal_strut(location, unit_cell_size, radius, angle_x, angle_y):
	hypot2D = hypot(unit_cell_size, unit_cell_size)
	hypot3D = hypot(hypot2D, unit_cell_size)
	result = (
		cq.Workplane()
		.transformed(rotate = cq.Vector(angle_x, angle_y, 0))
		.circle(radius)
		.extrude(hypot3D)
	)
	return result.val().located(location)

def BCC_diagonals(unit_cell_size, strut_radius):
	# In a cube ABCDA1B1C1D1 this is the angle C1AD
	angle_C1AD = 90 - degrees(acos(3**-.5))
	corner_points = unit_cell_size * np.array(
		[(0, 0),
		(1, 0),
		(1, 1),
		(0, 1)]
	)
	result = (
		cq.Workplane("XY")
		.pushPoints(corner_points)
		.eachpointAdaptive(
			create_diagonal_strut,
			callback_extra_args = [
				{"unit_cell_size": unit_cell_size,
				"radius": strut_radius,
				 "angle_x": - 45,
				 "angle_y": angle_C1AD},
				{"unit_cell_size": unit_cell_size,
				"radius": strut_radius,
				 "angle_x": - 45,
				 "angle_y": - angle_C1AD},
				{"unit_cell_size": unit_cell_size,
				"radius": strut_radius,
				 "angle_x": 45,
				 "angle_y": - angle_C1AD},
				{"unit_cell_size": unit_cell_size,
				"radius": strut_radius,
				 "angle_x": 45,
				 "angle_y": angle_C1AD}
				],
			useLocalCoords = True
		)
	)
	return result
# Register our custom plugin before use.
cq.Workplane.BCC_diagonals = BCC_diagonals

def BCC_vertical_struts(unit_cell_size, strut_radius):
	result = cq.Workplane("XY")
	corner_points = unit_cell_size * np.array(
		[(0, 0),
		(1, 0),
		(1, 1),
		(0, 1)]
	)
	for point in corner_points:
		result = (result
				  .union(
					  cq.Workplane()
					  .transformed(offset = cq.Vector(point[0], point[1]))
					  .circle(strut_radius)
					  .extrude(unit_cell_size)
					  )
				  )
	return result
# Register our custom plugin before use.
cq.Workplane.BCC_vertical_struts = BCC_vertical_struts

def BCC_bottom_horizontal_struts(unit_cell_size, strut_radius):
	result = cq.Workplane("XY")
	angle = 90
	corner_points = unit_cell_size * np.array(
		[(0, 0),
		(1, 0),
		(1, 1),
		(0, 1)]
	)
	for point in corner_points:
		result = (result
				  .union(
					  cq.Workplane()
					  .transformed(offset = cq.Vector(point[0], point[1], 0),
								   rotate = cq.Vector(90, angle, 0))
					  .circle(strut_radius)
					  .extrude(unit_cell_size)
					  )
				  )
		angle += 90
	return result
# Register our custom plugin before use.
cq.Workplane.BCC_bottom_horizontal_struts = BCC_bottom_horizontal_struts

def BCC_top_horizontal_struts(unit_cell_size, strut_radius):
	result = cq.Workplane("XY")
	angle = 90
	corner_points = unit_cell_size * np.array(
		[(0, 0),
		(1, 0),
		(1, 1),
		(0, 1)]
	)
	for point in corner_points:
		result = (result
				  .union(
					  cq.Workplane()
					  .transformed(offset = cq.Vector(point[0], point[1], unit_cell_size),
								   rotate = cq.Vector(90, angle, 0))
					  .circle(strut_radius)
					  .extrude(unit_cell_size)
					  )
				  )
		angle += 90
	return result
# Register our custom plugin before use.
cq.Workplane.BCC_top_horizontal_struts = BCC_top_horizontal_struts

# Creates 4 nodes at the XY plane of each unit cell
def createNodes(node_diameter,
				unit_cell_size,
				delta = 0.01 # a small coefficient is needed because CQ thinks that it cuts through emptiness
				):
	added_node_diameter = node_diameter + delta
	node_radius = node_diameter / 2.0
	result = cq.Workplane("XY")
	corner_points = unit_cell_size * np.array(
		[(0, 0),
		(1, 0),
		(1, 1),
		(0, 1)]
	)
	for point in corner_points:
		result= (result
				  .union(
					  cq.Workplane()
					  .transformed(offset = cq.Vector(point[0], point[1], 0))
					  .box(added_node_diameter, added_node_diameter, added_node_diameter)
					  .edges("|Z")
					  .fillet(node_radius)
					  .edges("|X")
					  .fillet(node_radius)
					  )
				  )
		result= (result
				  .union(
					  cq.Workplane()
					  .transformed(offset = cq.Vector(point[0], point[1], unit_cell_size))
					  .box(added_node_diameter, added_node_diameter, added_node_diameter)
					  .edges("|Z")
					  .fillet(node_radius)
					  .edges("|X")
					  .fillet(node_radius)
					  )
				  )
	half_unit_cell_size = unit_cell_size / 2
	result= (result
			 .union(
				 cq.Workplane()
				 .transformed(offset = cq.Vector(half_unit_cell_size,
												 half_unit_cell_size,
												 half_unit_cell_size))
				 .box(added_node_diameter, added_node_diameter, added_node_diameter)
				 .edges("|Z")
				 .fillet(node_radius)
				 .edges("|X")
				 .fillet(node_radius)
				 )
			 )
	return result
cq.Workplane.createNodes = createNodes

def unit_cell(location, unit_cell_size, strut_radius, node_diameter):
	result = cq.Workplane("XY")
	result = (result
			  .union(BCC_diagonals(unit_cell_size, strut_radius))
			  .union(BCC_vertical_struts(unit_cell_size, strut_radius))
			  .union(BCC_bottom_horizontal_struts(unit_cell_size, strut_radius))
			  .union(BCC_top_horizontal_struts(unit_cell_size, strut_radius))
			  .union(createNodes(node_diameter, unit_cell_size))
			  )
	return result.val().located(location)
cq.Workplane.unit_cell = unit_cell

def BCC_heterogeneous_lattice(unit_cell_size,
							  min_strut_diameter, 
							  max_strut_diameter,
							  min_node_diameter,
							  max_node_diameter,
							  Nx, Ny, Nz):
	min_strut_radius = min_strut_diameter / 2.0
	max_strut_radius = max_strut_diameter / 2.0
	strut_radii = np.linspace(min_strut_radius,
							  max_strut_radius,
							  Nz)
	node_diameters = np.linspace(min_node_diameter,
								 max_node_diameter,
								 Nz)
	UC_pnts = []
	for i in range(Nx):
		for j in range(Ny):
			for k in range(Nz):
				UC_pnts.append((i * unit_cell_size, j * unit_cell_size, k * unit_cell_size))
	result = cq.Workplane().tag('base')
	result = result.pushPoints(UC_pnts)
	result = result.eachpointAdaptive(unit_cell,
									  callback_extra_args = [
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[0],
										   "node_diameter": node_diameters[0]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[1],
										   "node_diameter": node_diameters[1]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[2],
										   "node_diameter": node_diameters[2]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[3],
										   "node_diameter": node_diameters[3]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[4],
										   "node_diameter": node_diameters[4]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[0],
										   "node_diameter": node_diameters[0]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[1],
										   "node_diameter": node_diameters[1]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[2],
										   "node_diameter": node_diameters[2]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[3],
										   "node_diameter": node_diameters[3]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[4],
										   "node_diameter": node_diameters[4]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[0],
										   "node_diameter": node_diameters[0]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[1],
										   "node_diameter": node_diameters[1]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[2],
										   "node_diameter": node_diameters[2]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[3],
										   "node_diameter": node_diameters[3]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[4],
										   "node_diameter": node_diameters[4]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[0],
										   "node_diameter": node_diameters[0]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[1],
										   "node_diameter": node_diameters[1]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[2],
										   "node_diameter": node_diameters[2]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[3],
										   "node_diameter": node_diameters[3]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[4],
										   "node_diameter": node_diameters[4]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[0],
										   "node_diameter": node_diameters[0]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[1],
										   "node_diameter": node_diameters[1]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[2],
										   "node_diameter": node_diameters[2]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[3],
										   "node_diameter": node_diameters[3]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[4],
										   "node_diameter": node_diameters[4]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[0],
										   "node_diameter": node_diameters[0]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[1],
										   "node_diameter": node_diameters[1]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[2],
										   "node_diameter": node_diameters[2]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[3],
										   "node_diameter": node_diameters[3]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[4],
										   "node_diameter": node_diameters[4]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[0],
										   "node_diameter": node_diameters[0]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[1],
										   "node_diameter": node_diameters[1]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[2],
										   "node_diameter": node_diameters[2]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[3],
										   "node_diameter": node_diameters[3]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[4],
										   "node_diameter": node_diameters[4]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[0],
										   "node_diameter": node_diameters[0]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[1],
										   "node_diameter": node_diameters[1]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[2],
										   "node_diameter": node_diameters[2]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[3],
										   "node_diameter": node_diameters[3]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[4],
										   "node_diameter": node_diameters[4]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[0],
										   "node_diameter": node_diameters[0]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[1],
										   "node_diameter": node_diameters[1]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[2],
										   "node_diameter": node_diameters[2]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[3],
										   "node_diameter": node_diameters[3]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[4],
										   "node_diameter": node_diameters[4]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[0],
										   "node_diameter": node_diameters[0]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[1],
										   "node_diameter": node_diameters[1]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[2],
										   "node_diameter": node_diameters[2]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[3],
										   "node_diameter": node_diameters[3]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[4],
										   "node_diameter": node_diameters[4]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[0],
										   "node_diameter": node_diameters[0]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[1],
										   "node_diameter": node_diameters[1]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[2],
										   "node_diameter": node_diameters[2]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[3],
										   "node_diameter": node_diameters[3]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[4],
										   "node_diameter": node_diameters[4]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[0],
										   "node_diameter": node_diameters[0]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[1],
										   "node_diameter": node_diameters[1]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[2],
										   "node_diameter": node_diameters[2]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[3],
										   "node_diameter": node_diameters[3]},
										  {"unit_cell_size": unit_cell_size,
										   "strut_radius": strut_radii[4],
										   "node_diameter": node_diameters[4]}
										  ],
									  useLocalCoords = True)
	#result = result.unit_cell(unit_cell_size, strut_radius, node_diameter)
	return result
