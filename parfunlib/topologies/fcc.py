##############################################################################
# Copyright (C) 2021, Advanced Design and Manufacturing Lab (ADML). 
# All rights reserved. 
#
# This software and its documentation and related materials are owned by 
# ADML. The software may only be incorporated into application programs owned
# by members of ADML. The structure and organization of this software are
# the valuable trade secrets of ADML and its suppliers. The software is also 
# protected by copyright law and international treaty provisions.
#
# By use of this software, its documentation or related materials, you 
# acknowledge and accept the above terms.
##############################################################################

from ..commons import eachpointAdaptive

from math import hypot, acos, degrees, hypot
import numpy as np

import cadquery as cq

# Register our custom plugins before use.
cq.Workplane.eachpointAdaptive = eachpointAdaptive

def create_diagonal_strut(
		location: cq.occ_impl.geom.Location,
		unit_cell_size: np.float64,
		radius: np.float64,
		angle_x: np.float64,
		angle_y: np.float64) -> cq.occ_impl.shapes.Compound:
	"""
	Creates a solid model of a diagonal cylindrical strut.
	The angle is chosen with respect to the positive X direction

	Parameters
    ----------
        location : cq.occ_impl.geom.Location
            point location of the strut
        unit_cell_size : np.float64
            unit cell size (in mm)
		angle_x : np.float64
			angle between the stut and the positibe direction of X
			in the local coordinate system
		angle_y : np.float64
			angle between the stut and the positibe direction of Y
			in the local coordinate system
	Returns
	-------
		cq.occ_impl.shapes.Compound
			a solid model of the strut
	"""
	hypot2D = hypot(unit_cell_size, unit_cell_size)
	result = (
		cq.Workplane()
		.transformed(rotate = cq.Vector(angle_x, angle_y, 0))
		.circle(radius)
		.extrude(hypot2D)
	)
	return result.val().located(location)

def fcc_diagonals(unit_cell_size: np.float64,
					strut_radius: np.float64) -> cq.cq.Workplane:
	"""
	Creates a solid model of the diagonals in a FCC unit cell.

	Parameters
    ----------
        location : cq.occ_impl.geom.Location
            point location of the strut
        unit_cell_size : np.float64
            unit cell size (in mm)
		strut_radius : np.float64
			strut radius (in mm)
	Returns
	-------
		result : cq.occ_impl.shapes.Compound
			a solid model of the strut
	"""
	# In a cube ABCDA1B1C1D1 this is the angle ABA1
	corner_points = unit_cell_size * np.array(
		[(0, 0),
		(0, 0),
		(1, 0),
		(1, 0),
		(1, 1),
		(1, 1),
		(0, 1),
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
				 "angle_y": 0},
				{"unit_cell_size": unit_cell_size,
				"radius": strut_radius,
				 "angle_x": 0,
				 "angle_y": 45},
				{"unit_cell_size": unit_cell_size,
				"radius": strut_radius,
				 "angle_x": 0,
				 "angle_y": - 45},
				{"unit_cell_size": unit_cell_size,
				 "radius": strut_radius,
				 "angle_x": - 45,
				 "angle_y": 0},
				{"unit_cell_size": unit_cell_size,
				 "radius": strut_radius,
				 "angle_x": 45,
				 "angle_y": 0},
				{"unit_cell_size": unit_cell_size,
				 "radius": strut_radius,
				 "angle_x": 0,
				 "angle_y": - 45},
				{"unit_cell_size": unit_cell_size,
				 "radius": strut_radius,
				 "angle_x": 45,
				 "angle_y": 0},
				{"unit_cell_size": unit_cell_size,
				"radius": strut_radius,
				 "angle_x": 0,
				 "angle_y": 45}
				],
			useLocalCoords = True
		)
	)
	return result
# Register our custom plugin before use.
cq.Workplane.fcc_diagonals = fcc_diagonals

def fcc_vertical_struts(unit_cell_size: np.float64,
						strut_radius: np.float64) -> cq.cq.Workplane:
	"""
	Creates vertical struts of a unit cell.

	Parameters
    ----------
        unit_cell_size : np.float64
            unit cell size (in mm)
		strut_radius: np.float64
			strut radius (in mm)
	Returns
	-------
		result : cq.cq.Workplane
			a solid model of the union of all vertical struts
	"""
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
cq.Workplane.fcc_vertical_struts = fcc_vertical_struts

def fcc_bottom_horizontal_struts(unit_cell_size, strut_radius):
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
cq.Workplane.fcc_bottom_horizontal_struts = fcc_bottom_horizontal_struts

def fcc_horizontal_diagonal_struts(unit_cell_size, strut_radius):
	result = cq.Workplane("XY")
	corner_points = unit_cell_size * np.array(
		[(0, 0, 0),
		(1, 0, 0),
		(1, 1, 1),
		(0, 1, 1)]
	)
	angle = 135.0
	hypot2D = hypot(unit_cell_size, unit_cell_size)
	for point in corner_points:
		result = (result
				  .union(
					  cq.Workplane()
					  .transformed(offset = cq.Vector(point[0], point[1], point[2]),
								   rotate = cq.Vector(90, angle, 0))
					  .circle(strut_radius)
					  .extrude(hypot2D)
					  )
				  )
		angle += 90
	return result
# Register our custom plugin before use.
cq.Workplane.fcc_horizontal_diagonal_struts = fcc_horizontal_diagonal_struts

def fcc_top_horizontal_struts(unit_cell_size, strut_radius):
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
cq.Workplane.fcc_top_horizontal_struts = fcc_top_horizontal_struts

# Creates 4 nodes at the XY plane of each unit cell
def create_nodes(node_diameter,
				unit_cell_size,
				type,
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
	if type in ['fcc', 'fbcc']:
		corner_points = np.vstack([corner_points, unit_cell_size * np.array([(0.5, 0.5)])])
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
	middle_points = unit_cell_size * np.array(
		[(0.5, 0),
		(1, 0.5),
		(0.5, 1),
		(0, 0.5)]
	)
	for point in middle_points:
		result= (result
				  .union(
					  cq.Workplane()
					  .transformed(offset = cq.Vector(point[0], point[1], half_unit_cell_size))
					  .box(added_node_diameter, added_node_diameter, added_node_diameter)
					  .edges("|Z")
					  .fillet(node_radius)
					  .edges("|X")
					  .fillet(node_radius)
					  )
				  )

	return result
cq.Workplane.create_nodes = create_nodes

def unit_cell(location, unit_cell_size, strut_radius, node_diameter, type):
	result = cq.Workplane("XY")
	result = result.union(fcc_diagonals(unit_cell_size, strut_radius))
	if type in ['sfccz', 'sfbcc']:
		result = result.union(fcc_vertical_struts(unit_cell_size, strut_radius))
	if type in ['fcc', 'fbcc']:
		result = result.union(fcc_horizontal_diagonal_struts(unit_cell_size, strut_radius))
	result = result.union(create_nodes(node_diameter, unit_cell_size, type))
	return result.val().located(location)
cq.Workplane.unit_cell = unit_cell

def fcc_heterogeneous_lattice(unit_cell_size,
							  min_strut_diameter,
							  max_strut_diameter,
							  min_node_diameter,
							  max_node_diameter,
							  Nx, Ny, Nz,
							  type = 'fcc',
							  rule = 'linear'):
	if type not in ['fcc', 'sfcc', 'sfccz']:
		raise TypeError(f'The type \'{type}\' does not exist!')
	min_strut_radius = min_strut_diameter / 2.0
	max_strut_radius = max_strut_diameter / 2.0
	if rule == 'linear':
		strut_radii = np.linspace(min_strut_radius,
	   		 					  max_strut_radius,
		    					  Nz)
		node_diameters = np.linspace(min_node_diameter,
	    							 max_node_diameter,
		    						 Nz)
	if rule == 'sin':
		average = lambda num1, num2: (num1 + num2) / 2
		strut_radii = np.sin(
			np.linspace(min_strut_radius, max_strut_radius, Nz)*12) + 2*average(min_strut_radius, max_strut_radius)
		node_diameters = np.sin(
			np.linspace(min_node_diameter, max_node_diameter, Nz)*12) + 2*average(min_node_diameter, max_node_diameter)
	UC_pnts = []
	for i in range(Nx):
		for j in range(Ny):
			for k in range(Nz):
				UC_pnts.append((i * unit_cell_size, j * unit_cell_size, k * unit_cell_size))
	print("Datapoints generated")
	result = cq.Workplane().tag('base')
	result = result.pushPoints(UC_pnts)
	unit_cell_params = []
	for i in range(Nx * Ny):
		for j in range(Nz):
			unit_cell_params.append({"unit_cell_size": unit_cell_size,
				"strut_radius": strut_radii[j],
				"node_diameter": node_diameters[j],
				"type": type})
	result = result.eachpointAdaptive(unit_cell,
									  callback_extra_args = unit_cell_params,
									  useLocalCoords = True)
	print("The lattice is generated")
	return result