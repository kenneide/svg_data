from svg_path_commands import *
import numpy as np
import matplotlib.pyplot as plt
from svg_transform import *

class SvgPathDataUnexpectedParameterException(BaseException):
	pass
		

class SvgPath():
		
	def __init__(self, pathdata: str, transform=None):
		
		self._commands = []
		self._vertices = []
		self._pathstart = None
		self._pathdata = pathdata
		
		self._command_factory = SvgPathCommandFactory()
		
		if isinstance(transform, SvgTransform):
			self.transform = transform
		else:
			self.transform = SvgTransform(text=None)

		self.parse_commands_from_pathdata()
		assert self.commands[0].type == 'M'
		self.calculate_vertices()
		
	@property
	def commands(self):
		return self._commands

	def preprocess_and_tokenize_pathdata(self):
		data = self._pathdata
		
		for command in self._command_factory.KNOWN_COMMANDS:
			data = data.replace(command, ' ' + command + ' ')
		
		data = data.replace('-', ' -')
		
		data = data.replace(',', ' ')
		
		while '  ' in data:
			data = data.replace('  ', ' ')
		data = data.strip()
		
		need_space_here = []
		looking_for_space = False
		for index, character in enumerate(data):
			if character == '.' and not looking_for_space:
				looking_for_space = True
			elif character == '.' and looking_for_space:
				looking_for_space = True
				need_space_here.append(index)
			elif character == ' ':
				looking_for_space = False
				
		offset = 0
		for index in need_space_here:
			data = data[:index+offset] + ' 0' +data[index+offset:]
			offset += 2
				
		return data.split(' ')
						
	def parse_commands_from_pathdata(self):
		tokens = self.preprocess_and_tokenize_pathdata()
		this_command_type = None
		this_command_parameters = []
		for token in tokens:
			if token.isalpha():
				if this_command_type is not None:
					self.add_command(this_command_type, this_command_parameters)
				this_command_type = token
				this_command_parameters = []
			else:
				if this_command_type is not None:
					this_command_parameters.append(float(token))
				elif token == '':
					break
				else:
					raise SvgPathDataUnexpectedParameterException()
		
		self.add_command(this_command_type, this_command_parameters)
					
	def add_command(self, type, parameters):
		n = len(parameters)
		m = self._command_factory.get_required_num_of_parameters(type)
		
		if m == 0 and n > 0:
			raise SvgPathCommandTooManyParametersException
		elif m == 0 and n == 0:
			command = self._command_factory.get_command(type, parameters)
			self._commands.append(command)
		elif m > 0:
			parameters = np.array(parameters).reshape((n/m,m))
			for parameter_set in parameters:
				command = self._command_factory.get_command(type, parameter_set)
				self._commands.append(command)
	
	@property
	def vertices(self):
		return self._vertices
			
	def calculate_vertices(self):
		vertices = []
		current_vertex = None
		for command in self.commands:
			current_vertex = command.get_next_vertex(current_vertex)
			vertices.append(current_vertex)
		
		self._vertices = self.transform.apply(vertices)
	
		return self._vertices
		
	def calculate_length(self):
		pathlength = 0.
		current_vertex = self.vertices[0]
		self._subpath_length = []
		for next_vertex in self.vertices[1:]:
			self._subpath_length.append(
				self.calculate_distance_between(current_vertex, next_vertex)
			) 
			current_vertex = next_vertex
		return np.sum(self._subpath_length)
		
	def calculate_distance_between(self, start_vertex, end_vertex):
		(x0, y0) = start_vertex
		(x1, y1) = end_vertex
		return np.sqrt((y1-y0)**2+(x1-x0)**2)
	
	def interpolate_vertices(self, ratio, start_vertex, end_vertex):
		(x0, y0) = start_vertex
		(x1, y1) = end_vertex
		return (ratio*(x1-x0)+x0, ratio*(y1-y0)+y0)
		
	def get_coordinates(self, n_coordinates: int):
		assert n_coordinates > 0
		if n_coordinates == 1:
			return self.vertices[0]
		
		path_length = self.calculate_length()
		n_segments = n_coordinates - 1
		segment_length = path_length / n_segments
		
		coordinates = [self.vertices[0]]
		subpath_index = 0
		cumulative_distance_to_next_vertex = self._subpath_length[subpath_index]
		for index in range(1, n_coordinates):
			distance_to_coordinate = index*segment_length
			
			while distance_to_coordinate > cumulative_distance_to_next_vertex + 10**-8:
				subpath_index += 1
				cumulative_distance_to_next_vertex += self._subpath_length[subpath_index]
			
			before_vertex = self.vertices[subpath_index]
			after_vertex = self.vertices[subpath_index+1]
			
			cumulative_distance_to_before_vertex = cumulative_distance_to_next_vertex - self._subpath_length[subpath_index]
			
			subpath_portion = distance_to_coordinate - cumulative_distance_to_before_vertex
			subpath_length = self.calculate_distance_between(before_vertex, after_vertex);
			subpath_ratio = subpath_portion / subpath_length
						
			next_coordinate = self.interpolate_vertices(subpath_ratio, before_vertex, after_vertex) 

			coordinates.append(next_coordinate)			
			
		return coordinates
		
	def plot(self, n_coordinates: int):
		coordinates = self.get_coordinates(n_coordinates)
		x = [element[0] for element in coordinates]
		y = [element[1] for element in coordinates]
		plt.plot(x, -1*np.array(y))
		plt.show()
