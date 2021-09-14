from ..commons import eachpointAdaptive, strut_based_unit_cell

from math import hypot, acos, degrees
import numpy as np

import cadquery as cq

# Register our custom plugins before use.
cq.Workplane.eachpointAdaptive = eachpointAdaptive

class BCC(strut_based_unit_cell):
	def __init__(self, location, unit_cell_size, strut_radius, node_diameter):
		super().__init__(location, unit_cell_size, strut_radius, node_diameter)
		self.__corner_points = unit_cell_size * np.array(
			[(0, 0),
			(1, 0),
			(1, 1),
			(0, 1)]
			)
		# In a cube ABCDA1B1C1D1 this is the angle C1AD
		self.__angle_C1AD = 90 - degrees(acos(3**-.5))

	# The angle is chosen with respect to the positive X direction
	def __create_diagonal_strut(angle_x, angle_y):
		hypot2D = hypot(self.unit_cell_size, self.unit_cell_size)
		hypot3D = hypot(hypot2D, self.unit_cell_size)
		result = (
			cq.Workplane()
			.transformed(rotate = cq.Vector(angle_x, angle_y, 0))
			.circle(self.strut_radius)
			.extrude(hypot3D)
		)
		return result.val().located(location)

	def __BCC_diagonals():
		result = (
			cq.Workplane("XY")
			.pushPoints(self.corner_points)
			.eachpointAdaptive(
				self.__create_diagonal_strut,
				callback_extra_args = [
					{"angle_x": - 45,
					 "angle_y": self.angle_C1AD},
					{"angle_x": - 45,
					 "angle_y": - self.angle_C1AD},
					{"angle_x": 45,
					 "angle_y": - self.angle_C1AD},
					{"angle_x": 45,
					 "angle_y": self.angle_C1AD}
					],
				useLocalCoords = True
			)
		)
		return result

	def __BCC_vertical_struts():
		result = cq.Workplane("XY")
		for point in self.corner_points:
			result = (result
					  .union(
						  cq.Workplane()
						  .transformed(offset = cq.Vector(point[0], point[1]))
						  .circle(self.strut_radius)
						  .extrude(self.unit_cell_size)
						  )
					  )
		return result

	def __BCC_bottom_horizontal_struts():
		result = cq.Workplane("XY")
		angle = 90
		for point in self.corner_points:
			result = (result
					  .union(
						  cq.Workplane()
						  .transformed(offset = cq.Vector(point[0], point[1], 0),
									   rotate = cq.Vector(90, angle, 0))
						  .circle(self.strut_radius)
						  .extrude(self.unit_cell_size)
						  )
					  )
			angle += 90
		return result

	def __BCC_top_horizontal_struts(unit_cell_size, strut_radius):
		result = cq.Workplane("XY")
		angle = 90
		for point in self.corner_points:
			result = (result
					  .union(
						  cq.Workplane()
						  .transformed(offset = cq.Vector(point[0], point[1], self.unit_cell_size),
									   rotate = cq.Vector(90, angle, 0))
						  .circle(self.strut_radius)
						  .extrude(self.unit_cell_size)
						  )
					  )
			angle += 90
		return result

	# Creates 4 nodes at the XY plane of each unit cell
	def createNodes(delta = 0.01 # a small coefficient is needed because CQ thinks that it cuts through emptiness
					):
		added_node_diameter = self.node_diameter + delta
		node_radius = self.node_diameter / 2.0
		result = cq.Workplane("XY")
		for point in self.corner_points:
			result = (result
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
			result = (result
					  .union(
						  cq.Workplane()
						  .transformed(offset = cq.Vector(point[0], point[1], self.unit_cell_size))
						  .box(added_node_diameter, added_node_diameter, added_node_diameter)
						  .edges("|Z")
						  .fillet(node_radius)
						  .edges("|X")
						  .fillet(node_radius)
						  )
					  )
		half_unit_cell_size = self.unit_cell_size / 2
		result = (result
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

	def get_model():
		result = cq.Workplane("XY")
		result = (result
				  .union(__BCC_diagonals(self.unit_cell_size, self.strut_radius))
				  .union(__BCC_vertical_struts(self.unit_cell_size, self.strut_radius))
				  .union(__BCC_bottom_horizontal_struts(self.unit_cell_size, self.strut_radius))
				  .union(__BCC_top_horizontal_struts(self.unit_cell_size, self.strut_radius))
				  .union(__createNodes(self.node_diameter, self.unit_cell_size))
				  )
		return result.val().located(self.location)

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
	unit_cell_params = []
	for i in range(Nx * Ny):
		for j in range(Nz):
			unit_cell_params.append({"unit_cell_size": unit_cell_size,
				"strut_radius": strut_radii[j],
				"node_diameter": node_diameters[j]})
	result = result.eachpointAdaptive(unit_cell,
									  callback_extra_args = unit_cell_params,
									  useLocalCoords = True)
	#result = result.unit_cell(unit_cell_size, strut_radius, node_diameter)
	return result
