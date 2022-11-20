import matplotlib.pyplot as plt

from svg.path_commands import *
from svg.path_segment import *
from svg.element import *


class SvgPathDataUnexpectedParameterException(BaseException):
	pass


class SvgPath(SvgGraphicsElement):
		
	def __init__(self, id=None, pathdata=None, transform=None):
		super().__init__(id=id, transform=transform)
		self._commands = []
		self._segments = []
		self._pathstart = None
		self._pathdata = pathdata
		
		self._factory = SvgPathCommandFactory()
		types, parameters = self._factory.extract_commands_from_pathdata(self._pathdata)
		self.add_commands(types, parameters)

		self.segmentize()
		
	@property
	def commands(self):
		return self._commands
					
	def add_commands(self, type, parameters):
		for type, parameter_set in zip(type, parameters):
			command = self._factory.get_command(type, parameter_set)
			self._commands.append(command)

	def segmentize(self):
		current_vertex = None
		for command in self.commands:
			next_vertex = command.get_next_vertex(current_vertex)
			self._vertices.append(next_vertex)
			current_vertex = next_vertex
		
		current_vertex = self.transformed_vertices[0]
		for command, next_vertex in zip(self.commands[1:], self.transformed_vertices[1:]):
			self._segments.append(LinearSvgPathSegment(start=current_vertex, end=next_vertex))
			current_vertex = next_vertex
		
	def length(self):
		pathlength = 0.
		for segment in self._segments:
			pathlength += segment.length()
		return pathlength
		
	def plot(self, n_coordinates):
		entry = self.export(n_coordinates)
		plt.plot(entry['x'], entry['y'])
		
	def export(self, n_coordinates):
		points = self.get_coordinates(n_coordinates)
		x = [element[0] for element in points]
		y = [element[1] for element in points]
		table = {
			'id': self._id,
			'x': x,
			'y': y,
			'index': list(np.arange(1,len(points)+1)),
		}
		return table
		
	def get_coordinates(self, n_coordinates):

		transformed_vertices = self.transform.apply(self.vertices)
		
		distance_between_coordinates = self.length() / (n_coordinates - 1)
		
		coordinates = [transformed_vertices[0]]
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
