from svg_path_commands import *
import numpy as np
import matplotlib.pyplot as plt
from svg_transform import *
from svg_path_segment import *

class SvgPathDataUnexpectedParameterException(BaseException):
	pass
		

class SvgPath():
		
	def __init__(self, pathdata: str, transform=None):
		
		self._commands = []
		self._vertices = []
		self._segments = []
		self._pathstart = None
		self._pathdata = pathdata
		
		if isinstance(transform, SvgTransform):
			self.transform = transform
		else:
			self.transform = SvgTransform(text=None)

		self._factory = SvgPathCommandFactory()
		types, parameters = self._factory.extract_commands_from_pathdata(self._pathdata)
		self.add_commands(types, parameters)

		self.segmentize()
		
	@property
	def commands(self):
		return self._commands
		
	@property
	def vertices(self):
		return self._vertices
					
	def add_commands(self, type, parameters):
		for type, parameter_set in zip(type, parameters):
			command = self._factory.get_command(type, parameter_set)
			self._commands.append(command)
			
	def segmentize(self):
		vertices = []
		current_vertex = None
		for command in self.commands:
			next_vertex = command.get_next_vertex(current_vertex)
			vertices.append(next_vertex)
			current_vertex = next_vertex
		
		self._vertices = self.transform.apply(vertices)
		
		current_vertex = self._vertices[0]
		for command, next_vertex in zip(self.commands[1:], self._vertices[1:]):
			self._segments.append(LinearSvgPathSegment(start=current_vertex, end=next_vertex))
			current_vertex = next_vertex
		
	def length(self):
		pathlength = 0.
		for segment in self._segments:
			pathlength += segment.length()
		return pathlength
		
	def get_coordinates(self, n_coordinates: int):
		assert n_coordinates > 0

		distance_between_coordinates = self.length() / (n_coordinates - 1)
		
		coordinates = [self.vertices[0]]
		subpath_index = 0
		cumulative_distance_to_next_vertex = self._segments[0].length()
		for index in range(1, n_coordinates):
			distance_to_coordinate = index*distance_between_coordinates
			
			while distance_to_coordinate > cumulative_distance_to_next_vertex + 10**-8:
				subpath_index += 1
				cumulative_distance_to_next_vertex += self._segments[subpath_index].length()
			
			cumulative_distance_to_before_vertex = cumulative_distance_to_next_vertex - self._segments[subpath_index].length()
			
			subpath_portion = distance_to_coordinate - cumulative_distance_to_before_vertex
			subpath_ratio = subpath_portion / self._segments[subpath_index].length()
						
			next_coordinate = self._segments[subpath_index].interpolate(subpath_ratio) 

			coordinates.append(next_coordinate)			
			
		return coordinates
		
	def plot(self, n_coordinates: int):
		coordinates = self.get_coordinates(n_coordinates)
		x = [element[0] for element in coordinates]
		y = [element[1] for element in coordinates]
		plt.plot(x, -1*np.array(y))
		plt.show()
