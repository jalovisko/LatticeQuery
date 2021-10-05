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

from typing import Tuple
from numpy.lib.function_base import append
from ..commons import eachpointAdaptive

from math import hypot, acos, degrees
import numpy as np

import cadquery as cq

# Register our custom plugins before use.
cq.Workplane.eachpointAdaptive = eachpointAdaptive

PNT_LEVELS = [
		[(1, 0), (0.5, 0.5), (0, 1)],
		[(0.75, 0.25), (0.25, 0.75)],
		[(0.5, 0), (1, 0.5), (0.5, 1), (0, 0.5)],
		[(0.25, 0.25), (0.75, 0.75)],
		[(0, 0), (0.5, 0.5), (1, 1)]
		]

def create_strut(
		unit_cell_size: np.float64,
		offset: Tuple,
		angle: Tuple,
		radius: np.float64) -> cq.occ_impl.shapes.Compound:
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
	hypot2D = hypot(0.25 * unit_cell_size, 0.25 * unit_cell_size)
	strut_len = hypot(hypot2D, 0.25 * unit_cell_size)
	result = cq.Workplane()
	result = result.transformed(rotate = cq.Vector(angle),
								offset = cq.Vector(offset))
	result = result.circle(radius).extrude(strut_len)
	return result
# Register our custom plugin before use.
cq.Workplane.create_strut = create_strut


def create_diamond_struts(
		unit_cell_size: np.float64,
		radius: np.float64) -> cq.occ_impl.shapes.Compound:
	"""
	Creates a solid model of all cylindrical struts
	of the diamond topology.

	Parameters
    ----------
        location : cq.occ_impl.geom.Location
            point location of the strut
        unit_cell_size : np.float64
            unit cell size (in mm)
		radius : np.float64
			strut radius (in mm)
	Returns
	-------
		cq.occ_impl.shapes.Compound
			a solid model of the struts
		
	"""
	angle_x = 45
	# In a cube ABCDA1B1C1D1 this is the angle C1AD
	angle_c1ad = 90 - degrees(acos(3**-.5))
	# 4 bottom struts
	result = create_strut(unit_cell_size,
							(unit_cell_size, 0, 0),
							(-45, -angle_c1ad, 0),
							radius)
	result = result.union(create_strut(unit_cell_size,
										(0.5*unit_cell_size, 0.5*unit_cell_size, 0),
										(-45, - angle_c1ad, 0),
										radius))
	result = result.union(create_strut(unit_cell_size,
										(0.5*unit_cell_size, 0.5*unit_cell_size, 0),
										(45, angle_c1ad, 0),
										radius))
	result = result.union(create_strut(unit_cell_size,
										(0, unit_cell_size, 0),
										(45, angle_c1ad, 0),
										radius))
	# 4 2nd level struts
	result = result.union(create_strut(unit_cell_size,
										(0.75 * unit_cell_size, 0.25 * unit_cell_size, 0.25 * unit_cell_size),
										(-45, angle_c1ad, 0),
										radius))
	result = result.union(create_strut(unit_cell_size,
										(0.75 * unit_cell_size, 0.25 * unit_cell_size, 0.25 * unit_cell_size),
										(45, - angle_c1ad, 0),
										radius))
	result = result.union(create_strut(unit_cell_size,
										(0.25 * unit_cell_size, 0.75 * unit_cell_size, 0.25 * unit_cell_size),
										(-45, angle_c1ad, 0),
										radius))
	result = result.union(create_strut(unit_cell_size,
										(0.25 * unit_cell_size, 0.75 * unit_cell_size, 0.25 * unit_cell_size),
										(45, - angle_c1ad, 0),
										radius))
	# 4 3rd level struts
	result = result.union(create_strut(unit_cell_size,
										(0.5 * unit_cell_size, 0, 0.5 * unit_cell_size),
										(-45, - angle_c1ad, 0),
										radius))
	result = result.union(create_strut(unit_cell_size,
										(unit_cell_size, 0.5 * unit_cell_size, 0.5 * unit_cell_size),
										(-45, - angle_c1ad, 0),
										radius))
	result = result.union(create_strut(unit_cell_size,
										(0.5 * unit_cell_size, unit_cell_size, 0.5 * unit_cell_size),
										(45, angle_c1ad, 0),
										radius))
	result = result.union(create_strut(unit_cell_size,
										(0, 0.5 * unit_cell_size, 0.5 * unit_cell_size),
										(45, angle_c1ad, 0),
										radius))
	# 4 top struts
	result = result.union(create_strut(unit_cell_size,
										(0.25*unit_cell_size, 0.25*unit_cell_size, 0.75 * unit_cell_size),
										(45, - angle_c1ad, 0),
										radius))
	result = result.union(create_strut(unit_cell_size,
										(0.25*unit_cell_size, 0.25*unit_cell_size, 0.75 * unit_cell_size),
										(- 45, angle_c1ad, 0),
										radius))
	result = result.union(create_strut(unit_cell_size,
										(0.75*unit_cell_size, 0.75*unit_cell_size, 0.75 * unit_cell_size),
										(45, - angle_c1ad, 0),
										radius))
	result = result.union(create_strut(unit_cell_size,
										(0.75*unit_cell_size, 0.75*unit_cell_size, 0.75 * unit_cell_size),
										(- 45, angle_c1ad, 0),
										radius))

	return result
# Register our custom plugin before use.
cq.Workplane.create_diamond_struts = create_diamond_struts



# Creates 4 nodes at the XY plane of each unit cell
def create_nodes(node_diameter,
				unit_cell_size,
				delta = 0.01 # a small coefficient is needed because CQ thinks that it cuts through emptiness
				):
	added_node_diameter = node_diameter + delta
	node_radius = node_diameter / 2.0
	
	z_level = 0
	result = cq.Workplane("XY")
	for pnt_level in PNT_LEVELS:
		for pnt in pnt_level:
			result = (result
					.union(
						cq.Workplane()
						.transformed(offset = cq.Vector(pnt[0] * unit_cell_size,
														pnt[1] * unit_cell_size,
														z_level))
						.box(added_node_diameter, added_node_diameter, added_node_diameter)
						.edges("|Z")
						.fillet(node_radius)
						.edges("|X")
						.fillet(node_radius)
						)
					)
		z_level += 0.25 * unit_cell_size
	return result
cq.Workplane.create_nodes = create_nodes

def unit_cell(location, unit_cell_size, strut_radius, node_diameter, type):
	result = cq.Workplane("XY")
	result = result.union(create_diamond_struts(unit_cell_size, strut_radius))
	result = result.union(create_nodes(node_diameter, unit_cell_size))
	return result.val().located(location)
cq.Workplane.unit_cell = unit_cell

def diamond_heterogeneous_lattice(unit_cell_size,
							  min_strut_diameter,
							  max_strut_diameter,
							  min_node_diameter,
							  max_node_diameter,
							  Nx, Ny, Nz,
							  rule = 'linear'):
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