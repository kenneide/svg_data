from svg_path_commands import *
import numpy as np
import matplotlib.pyplot as plt

class SvgPathUnexpectedParameterException(BaseException):
	pass
	
class SvgPathInsufficientParametersException(BaseException):
	pass
		

class SvgPath():
		
	def __init__(self, pathdata: str, transform: None):
		
		self._commands = []
		self._vertices = []
		self._pathstart = None

		self._transform = transform
		self._pathdata = pathdata

		self.parse_commands_from_pathdata()
		assert self.commands[0].type == 'M'
		self.calculate_vertices()
		
	@property
	def commands(self):
		return self._commands

	def preprocess_and_tokenize_pathdata(self):
		data = self._pathdata
		
		for command in KNOWN_COMMANDS:
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
					raise SvgPathUnexpectedParameterException()
		
		self.add_command(this_command_type, this_command_parameters)
		
		while self.check_for_multiple_parameters() > 0:
			pass
		
	def check_for_multiple_parameters(self):
		indices_where_to_insert = []
		
		for index, command in enumerate(self._commands):
			n = required_num_of_parameters[command.type]
			if len(command.parameters) > n:
				#need to split this command into two...
				indices_where_to_insert.append(index)
			elif len(command.parameters) < n:
				print('command {} does not have enough parameters (got {})'.format(command.type, len(command.parameters)))
				raise SvgPathInsufficientParametersException
				
		offset = 0
		for index in indices_where_to_insert:
			jndex = index + offset
			n = required_num_of_parameters[self._commands[jndex].type]
			new_type = self._commands[jndex].type
			new_parameters = self._commands[jndex].parameters[n:]
			self._commands[jndex].parameters = self._commands[jndex].parameters[:n]
			new_command = SvgPathCommand(new_type, new_parameters)
			self._commands = self._commands[:jndex+1] + [new_command] + self._commands[jndex+1:]
			offset += 1
			
		return len(indices_where_to_insert)
					
	def add_command(self, command_type, parameters):
		self._commands.append(SvgPathCommand(command_type, parameters))
	
	@property
	def vertices(self):
		return self._vertices
		
	def transform_vertices(self, vertices):
		x_offset, y_offset = self.get_translate_offset()
		vertices = [(x+x_offset, y+y_offset) for x, y in vertices]
		return vertices				
			
	def calculate_vertices(self):
		vertices = []
		current_vertex = None
		for command in self.commands:
			current_vertex = self.get_next_vertex(command, current_vertex)
			vertices.append(current_vertex)
		
		self._vertices = self.transform_vertices(vertices)
	
		return self._vertices
		
	def get_translate_offset(self):
		if self._transform is not None:
			self._transform = self._transform.replace(',', ' ')
			while '  ' in self._transform:
				self._transform = self._transform.replace('  ', ' ')
			
			try:
				first, second = self._transform.split('(')[1].split(' ')
				first = float(first)
				second = float(second[:-1])
				return first, second
			except:
				# only a single item to unpack --> assume y_offset == 0
				first = self._transform.split('(')[1]
				first = float(first[:-1])
				return (first, 0.)
		else:
			return (0., 0.)
		
	def get_next_vertex(self, command, current_vertex):
		if command.type == 'M':
			next_vertex = (command.parameters[0], command.parameters[1])
			if self._pathstart is None:
				self._pathstart = next_vertex
		elif command.type == 'L':
			next_vertex = (command.parameters[0], command.parameters[1])
		elif command.type == 'H':
			next_vertex = (command.parameters[0], current_vertex[1])
		elif command.type == 'V':
			next_vertex = (current_vertex[0], command.parameters[0])			
		elif command.type == 'm':
			next_vertex = (command.parameters[0]+current_vertex[0], command.parameters[1]+current_vertex[1])
		elif command.type == 'l':
			next_vertex = (command.parameters[0]+current_vertex[0], command.parameters[1]+current_vertex[1])
		elif command.type == 'h':
			next_vertex = (command.parameters[0]+current_vertex[0], current_vertex[1])
		elif command.type == 'v':
			next_vertex = (current_vertex[0], command.parameters[0]+current_vertex[1])
		elif command.type.lower() == 'z':
			if self._pathstart is not None:
				next_vertex = self._pathstart
			else:
				raise Exception(msg='No path start to go to!')
				
		return next_vertex
		
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
		
	def plot(self, n_coordinates: int, x_offset=0., y_offset=0.):
		coordinates = self.get_coordinates(n_coordinates)
		x = [element[0]+x_offset for element in coordinates]
		y = [element[1]+y_offset for element in coordinates]
		plt.plot(x, -1*np.array(y))
		plt.show()
