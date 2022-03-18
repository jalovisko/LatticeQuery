##############################################################################
# Copyright (C) 2022, Advanced Design and Manufacturing Lab (ADML). 
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

from unittest import result
from ..commons import cylinder_by_two_points, eachpointAdaptive

from math import hypot
import numpy as np

import cadquery as cq

# Register our custom plugins before use.
cq.Workplane.eachpointAdaptive = eachpointAdaptive

def octagon(self,
	unit_cell_size: float,
	strut_radius: float
	) -> cq.cq.Workplane:
	"""
	It creates an octagon
	
	Args:
	  unit_cell_size (float): float
	  strut_radius (float): float
	
	Returns:
	  A CQ object.
	"""
	# The following coordinates are based on permutations
	# of the TCO:
	# https://en.wikipedia.org/wiki/Truncated_cuboctahedron#Cartesian_coordinates
	truncation = 0.5 *unit_cell_size * np.sqrt(2) / (1 + 2 * np.sqrt(2))
	octagon_height = unit_cell_size * (1 + np.sqrt(2)) / (1 + 2 * np.sqrt(2))
	regular_octagon_side = unit_cell_size / (1 + 2 * np.sqrt(2))
	# Creating a list of vertices for the octagon.
	vertices = [
		(truncation, 0, truncation*2),
		(truncation, 0, truncation*2 + regular_octagon_side),
		(2*truncation, 0, unit_cell_size - truncation),
		(2*truncation + regular_octagon_side, 0, unit_cell_size - truncation),
		(unit_cell_size - truncation, 0, truncation*2 + regular_octagon_side),
		(unit_cell_size - truncation, 0, truncation*2),
		(2*truncation + regular_octagon_side, 0, truncation),
		(2*truncation, 0, truncation),
	]
	# all edges:
	result = cq.Workplane()
	for v in range(len(vertices)):
		result = result.union(cylinder_by_two_points(
			vertices[v],
			# looping to the first point:
			vertices[v + 1 if v + 1 != len(vertices) else 0],
			strut_radius
		))
	return self.union(self.eachpoint(lambda loc: result.val().located(loc), True))
cq.Workplane.octagon = octagon

def octagonal_faces(unit_cell_size: float,
	strut_radius: float
	) -> cq.cq.Workplane:
	faces = cq.Workplane().octagon(unit_cell_size, strut_radius)
	faces = faces.union(
		cq.Workplane()
		.transformed(
        	offset = cq.Vector(unit_cell_size, 0, 0))
		.transformed(
        	rotate = cq.Vector(0, 0, 90))
		.octagon(unit_cell_size, strut_radius)
	)
	return faces

def z_struts(
		unit_cell_size: np.float64,
		strut_radius: np.float64,
		truncation: np.float64) -> cq.cq.Workplane:
	"""
	Creates vertical struts of a unit cell

	Parameters
    ----------
        unit_cell_size : np.float64
            unit cell size (in mm)
		strut_radius: np.float64
			strut radius (in mm)
		truncation: np.float64
			the truncation ratio [0..1]
	Returns
	-------
		result: cq.cq.Workplane
			a solid model of the union of all vertical struts
	"""
	result = cq.Workplane("XY")
	half_truncation = 0.5 * truncation
	corner_points = unit_cell_size * np.array(
		[(half_truncation, 0),
		(1 - half_truncation, 0),
		(1, half_truncation),
		(1, 1 - half_truncation),
		(1 - half_truncation, 1),
		(half_truncation, 1),
		(0, 1 - half_truncation),
		(0, half_truncation)]
	)
	truncation_delta = truncation * unit_cell_size / 2
	for point in corner_points:
		result = (result
				  .union(
					  cq.Workplane()
					  .transformed(offset = cq.Vector(point[0], point[1], truncation_delta))
					  .circle(strut_radius)
					  .extrude(unit_cell_size - 2 * truncation_delta)
					  )
				  )
	return result
# Register our custom plugin before use.
cq.Workplane.z_struts = z_struts

def bottom_xy_struts(unit_cell_size, strut_radius, truncation):
	truncation_delta = truncation * unit_cell_size / 2
	result = cq.Workplane("XY")
	angle = 90
	corner_points = unit_cell_size * np.array(
		[(0, 0),
		(1, 0),
		(1, 1),
		(0, 1)]
	)
	truncation_data_top = np.array(
		[(truncation_delta, 0),
		(0, truncation_delta),
		(- truncation_delta, 0),
		(0, - truncation_delta)]
	)
	truncation_data_bottom = np.array(
		[(truncation_delta, truncation_delta),
		(- truncation_delta, truncation_delta),
		(- truncation_delta, - truncation_delta),
		(truncation_delta, - truncation_delta)]
	)
	for idp, point in enumerate(corner_points):
		result = (result
				  .union(
					  cq.Workplane()
					  .transformed(offset = cq.Vector(point[0] + truncation_data_top[idp][0],
					  		  				point[1] + truncation_data_top[idp][1],
							  				truncation_delta),
								   rotate = cq.Vector(90, angle, 0))
					  .circle(strut_radius)
					  .extrude(unit_cell_size - 2 * truncation_delta)
					  )
				  )
		result = (result
				  .union(
					  cq.Workplane()
					  .transformed(offset = cq.Vector(point[0] + truncation_data_bottom[idp][0],
					  		  				point[1] + truncation_data_bottom[idp][1],
							  				0),
								   rotate = cq.Vector(90, angle, 0))
					  .circle(strut_radius)
					  .extrude(unit_cell_size - 2 * truncation_delta)
					  )
				  )
		angle += 90
	return result
# Register our custom plugin before use.
cq.Workplane.bottom_xy_struts = bottom_xy_struts

def top_xy_struts(unit_cell_size, strut_radius, truncation):
	truncation_delta = truncation * unit_cell_size / 2
	result = cq.Workplane("XY")
	angle = 90
	corner_points = unit_cell_size * np.array(
		[(0, 0),
		(1, 0),
		(1, 1),
		(0, 1)]
	)
	truncation_data_bottom = np.array(
		[(truncation_delta, 0),
		(0, truncation_delta),
		(- truncation_delta, 0),
		(0, - truncation_delta)]
	)
	truncation_data_top = np.array(
		[(truncation_delta, truncation_delta),
		(- truncation_delta, truncation_delta),
		(- truncation_delta, - truncation_delta),
		(truncation_delta, - truncation_delta)]
	)
	for idp, point in enumerate(corner_points):
		result = (result
				  .union(
					  cq.Workplane()
					  .transformed(offset = cq.Vector(point[0] + truncation_data_bottom[idp][0],
					  		  					point[1] + truncation_data_bottom[idp][1],
												unit_cell_size - truncation_delta),
								   rotate = cq.Vector(90, angle, 0))
					  .circle(strut_radius)
					  .extrude(unit_cell_size - 2 * truncation_delta)
					  )
				  )
		result = (result
				  .union(
					  cq.Workplane()
					  .transformed(offset = cq.Vector(point[0] + truncation_data_top[idp][0],
					  		  				point[1] + truncation_data_top[idp][1],
							  				unit_cell_size),
								   rotate = cq.Vector(90, angle, 0))
					  .circle(strut_radius)
					  .extrude(unit_cell_size - 2 * truncation_delta)
					  )
				  )
		angle += 90
	return result
# Register our custom plugin before use.
cq.Workplane.top_xy_struts = top_xy_struts

def t_struts(strut_radius,
				unit_cell_size,
				truncation):
	corner_points = unit_cell_size * np.array(
		[(0, 0),
		(1, 0),
		(1, 1),
		(0, 1)]
	)
	truncation_delta = truncation * unit_cell_size / 2
	result = cq.Workplane("XY")
	angle_z = - 135
	for point in corner_points:
		if point[0] == 0:
			t_xz = truncation_delta 
			angle_x = - 45
		else:
			t_xz = - truncation_delta
			angle_x = 45
		if point[1] == 0:
			t_yz = truncation_delta
			angle_y = 45
		else:
			t_yz = - truncation_delta
			angle_y = - 45
		# Struts that are in XZ in the first octan
		result = result.union(
			cq.Workplane()
			.transformed(offset = cq.Vector(point[0] + t_xz,
												point[1] + t_yz,
												0),
						rotate = cq.Vector(0, angle_x, 0))
			.circle(strut_radius)
			.extrude(hypot(truncation_delta, truncation_delta))
		)
		result = result.union(
			cq.Workplane()
			.transformed(offset = cq.Vector(point[0] + t_xz,
												point[1] + t_yz,
												unit_cell_size),
						rotate = cq.Vector(0, angle_x * 3, 0))
			.circle(strut_radius)
			.extrude(hypot(truncation_delta, truncation_delta))
		)
		# Struts that are in XY in the first octan
		result = result.union(
			cq.Workplane()
			.transformed(offset = cq.Vector(point[0] + t_xz,
												point[1],
												truncation_delta),
						rotate = cq.Vector(90, angle_z, 0))
			.circle(strut_radius)
			.extrude(hypot(truncation_delta, truncation_delta))
		)
		result = result.union(
			cq.Workplane()
			.transformed(offset = cq.Vector(point[0] + t_xz,
												point[1],
												unit_cell_size - truncation_delta),
						rotate = cq.Vector(90, angle_z, 0))
			.circle(strut_radius)
			.extrude(hypot(truncation_delta, truncation_delta))
		)
		angle_z -= 90
		# Struts that are in YZ in the first octan
		result = result.union(
			cq.Workplane()
			.transformed(offset = cq.Vector(point[0] + t_xz,
												point[1] + t_yz,
												0),
						rotate = cq.Vector(angle_y, 0, 0))
			.circle(strut_radius)
			.extrude(hypot(truncation_delta, truncation_delta))
		)
		result = result.union(
			cq.Workplane()
			.transformed(offset = cq.Vector(point[0] + t_xz,
												point[1] + t_yz,
												unit_cell_size),
						rotate = cq.Vector(3*angle_y, 0, 0))
			.circle(strut_radius)
			.extrude(hypot(truncation_delta, truncation_delta))
		)

		
	return result
# Register our custom plugin before use.
cq.Workplane.t_struts = t_struts

# Creates 4 nodes at the XY plane of each unit cell
def create_nodes(node_diameter,
				unit_cell_size,
				truncation,
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
	truncation_delta = truncation * unit_cell_size / 2
	t_nodes = [
		[[truncation_delta, 0, truncation_delta],
		[0, truncation_delta, truncation_delta],
		[truncation_delta, truncation_delta, 0]],
		[[-truncation_delta, 0, truncation_delta],
		[0, truncation_delta, truncation_delta],
		[- truncation_delta, truncation_delta, 0]],
		[[- truncation_delta, 0, truncation_delta],
		[0, -truncation_delta, truncation_delta],
		[- truncation_delta, - truncation_delta, 0]],
		[[truncation_delta, 0, truncation_delta],
		[0, - truncation_delta, truncation_delta],
		[truncation_delta, - truncation_delta, 0]]
	]
	
	for idp, point in enumerate(corner_points):
		for t_node in t_nodes[idp]:
			result = (result
					.union(
						cq.Workplane()
						.transformed(offset = cq.Vector(point[0] + t_node[0],
															point[1] + t_node[1],
															t_node[2]))
						.box(added_node_diameter, added_node_diameter, added_node_diameter)
						.edges("|Z")
						.fillet(node_radius)
						.edges("|X")
						.fillet(node_radius)
						)
					)
			result = (result
					.union(
						cq.Workplane()
						.transformed(offset = cq.Vector(point[0] + t_node[0],
															point[1] + t_node[1],
															unit_cell_size - t_node[2]))
						.box(added_node_diameter, added_node_diameter, added_node_diameter)
						.edges("|Z")
						.fillet(node_radius)
						.edges("|X")
						.fillet(node_radius)
						)
					)
	return result
cq.Workplane.create_nodes = create_nodes

def unit_cell(location, unit_cell_size, strut_radius, node_diameter, truncation):
	result = cq.Workplane("XY")
	result = result.union(octagonal_faces(unit_cell_size, strut_radius))
	return result.val().located(location)
cq.Workplane.unit_cell = unit_cell

def tco_heterogeneous_lattice(unit_cell_size: float,
							  min_strut_diameter: float,
							  max_strut_diameter: float,
							  min_node_diameter: float,
							  max_node_diameter: float,
							  Nx: int, Ny: int, Nz: int,
							  truncation: float,
							  rule: str = 'linear') -> cq.cq.Workplane:
	"""
	The function creates a truncated
	Cubeoctahedron (TCO) heterogeneous lattice structure
	
	Args:
	  unit_cell_size (float): the size of the unit cell
	  min_strut_diameter (float): The minimum diameter of a strut.
	  max_strut_diameter (float): The maximum strut diameter.
	  min_node_diameter (float): The minimum node diameter of the lattice.
	  max_node_diameter (float): The maximum diameter of the nodes.
	  Nx (int): number of unit cells in the x direction
	  Ny (int): number of unit cells in the y direction
	  Nz (int): number of unit cells in the z direction
	  truncation (float): the fraction of the strut length that is truncated
	  rule (str): 'linear' or 'sin'. Defaults to linear
	
	Returns:
	  The lattice is returned as a CQ object.
	"""
	if not 0 <= truncation <= 1:
		raise ValueError("The truncation should take values from 0 to 1")
	min_strut_radius = min_strut_diameter / 2.0
	max_strut_radius = max_strut_diameter / 2.0
	if rule == 'linear':
		strut_radii = np.linspace(min_strut_radius,
	   		 					  max_strut_radius,
		    					  Nz)
		node_diameters = np.linspace(min_node_diameter,
	    							 max_node_diameter,
		    						 Nz)
	elif rule == 'sin':
		average = lambda num1, num2: (num1 + num2) / 2
		strut_radii = np.sin(
			np.linspace(min_strut_radius, max_strut_radius, Nz)*12) + 2*average(min_strut_radius, max_strut_radius)
		node_diameters = np.sin(
			np.linspace(min_node_diameter, max_node_diameter, Nz)*12) + 2*average(min_node_diameter, max_node_diameter)
	else:
		raise ValueError(f"Rule '{rule}' does not exist.")
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
				"truncation": truncation})
	result = result.eachpointAdaptive(unit_cell,
									  callback_extra_args = unit_cell_params,
									  useLocalCoords = True)
	print("The lattice is generated")
	return result