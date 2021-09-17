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
from .bcc import bcc_diagonals
from .bcc import create_nodes as create_bcc_nodes
from .fcc import create_diagonal_strut
from .fcc import fcc_diagonals
from .fcc import fcc_vertical_struts
from .fcc import fcc_bottom_horizontal_struts
from .fcc import fcc_horizontal_diagonal_struts
from .fcc import fcc_top_horizontal_struts
from .fcc import create_nodes

from math import hypot, acos, degrees, hypot
import numpy as np

import cadquery as cq

# Register our custom plugins before use.
cq.Workplane.eachpointAdaptive = eachpointAdaptive
cq.Workplane.bcc_diagonals = bcc_diagonals
cq.Workplane.create_bcc_nodes = create_bcc_nodes
cq.Workplane.create_diagonal_strut = create_diagonal_strut
cq.Workplane.fcc_diagonals = fcc_diagonals
cq.Workplane.fcc_vertical_struts = fcc_vertical_struts
cq.Workplane.fcc_bottom_horizontal_struts = fcc_bottom_horizontal_struts
cq.Workplane.fcc_horizontal_diagonal_struts = fcc_horizontal_diagonal_struts
cq.Workplane.fcc_top_horizontal_struts = fcc_top_horizontal_struts
cq.Workplane.create_nodes = create_nodes

def unit_cell(location, unit_cell_size, strut_radius, node_diameter, type):
	result = cq.Workplane("XY")
	result = result.union(bcc_diagonals(unit_cell_size, strut_radius))
	result = result.union(fcc_diagonals(unit_cell_size, strut_radius))
	if type in ['sfbcc', 'sfbccz']:
		result = result.union(create_nodes(node_diameter, unit_cell_size, type))
	if type in ['fbccz', 'sfbccz']:
		result = result.union(fcc_vertical_struts(unit_cell_size, strut_radius))
	if type == 'fbcc':
		result = result.union(fcc_horizontal_diagonal_struts(unit_cell_size, strut_radius))
		result = result.union(create_nodes(node_diameter, unit_cell_size, type))
	#result = result.union(create_bcc_nodes(node_diameter, unit_cell_size))
	return result.val().located(location)
cq.Workplane.unit_cell = unit_cell

def fbcc_heterogeneous_lattice(unit_cell_size,
							  min_strut_diameter,
							  max_strut_diameter,
							  min_node_diameter,
							  max_node_diameter,
							  Nx, Ny, Nz,
							  type = 'fbcc',
							  rule = 'linear'):
	if type not in ['fbcc', 'sfbcc', 'sfbccz']:
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