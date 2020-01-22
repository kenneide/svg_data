from abc import ABC, abstractmethod
	
class SvgPathCommandInsufficientParametersException(BaseException):
	pass
	
class SvgPathCommandTooManyParametersException(BaseException):
	pass

class SvgPathCommandFactory():
	def __init__(self):
		self.KNOWN_COMMANDS = { 'M', 'm', 'L', 'l', 'H', 'h', 'V', 'v', 'Z', 'z' }
		self.required_num_of_parameters = {
			'M': 2,
			'm': 2,
			'V': 1,
			'v': 1,
			'L': 2,
			'l': 2,
			'H': 1,
			'h': 1,
			'Z': 0,
			'z': 0
		}
		self._pathstart = None
		
	def get_required_num_of_parameters(self, type):
		if type not in self.KNOWN_COMMANDS:
			raise NotImplementedError
		return self.required_num_of_parameters[type]
		
	def get_command(self, type, parameters):
		if type not in self.KNOWN_COMMANDS:
			raise NotImplementedError
			
		if len(parameters) < self.required_num_of_parameters[type]:
			raise SvgPathCommandInsufficientParametersException
		elif len(parameters) > self.required_num_of_parameters[type]:
			raise SvgPathCommandTooManyParametersException
			
		if type == 'M':
			command = MSvgPathCommand(parameters)
			if self._pathstart is None:
				self._pathstart = command.get_pathstart()
		elif type == 'L':
			command = LSvgPathCommand(parameters)
		elif type == 'H':
			command = HSvgPathCommand(parameters)
		elif type == 'V':
			command = VSvgPathCommand(parameters)
		elif type == 'm':
			command = mSvgPathCommand(parameters)
		elif type == 'l':
			command = lSvgPathCommand(parameters)
		elif type == 'h':
			command = hSvgPathCommand(parameters)
		elif type == 'v':
			command = vSvgPathCommand(parameters)
		elif type.lower() == 'z':
			command = ZSvgPathCommand(parameters, pathstart=self._pathstart)
		
		return command

class SvgPathCommand(ABC):
	def __init__(self, type, parameters):
		self.type = type
		self.parameters = parameters
		
	@abstractmethod
	def get_next_vertex(self, current_vertex):
		pass
		
class MSvgPathCommand(SvgPathCommand):
	def __init__(self, parameters):
		super().__init__('M', parameters)
		
	def get_next_vertex(self, current_vertex):
		next_vertex = (self.parameters[0], self.parameters[1])
		return next_vertex
		
	def get_pathstart(self):
		return (self.parameters[0], self.parameters[1])
	
class mSvgPathCommand(SvgPathCommand):
	def __init__(self, parameters):
		super().__init__('m', parameters)

	def get_next_vertex(self, command, current_vertex):
		next_vertex = (self.parameters[0], self.parameters[1])
		return next_vertex

class VSvgPathCommand(SvgPathCommand):
	def __init__(self, parameters):
		super().__init__('V', parameters)
		
	def get_next_vertex(self, current_vertex):	
		next_vertex = (current_vertex[0], self.parameters[0])			
		return next_vertex
		
class vSvgPathCommand(SvgPathCommand):
	def __init__(self, parameters):
		super().__init__('v', parameters)
		
	def get_next_vertex(self, current_vertex):	
		next_vertex = (current_vertex[0], self.parameters[0]+current_vertex[1])
		return next_vertex
	
class LSvgPathCommand(SvgPathCommand):
	def __init__(self, parameters):
		super().__init__('L', parameters)
		
	def get_next_vertex(self, current_vertex):	
		next_vertex = (self.parameters[0], self.parameters[1])
		return next_vertex
	
class lSvgPathCommand(SvgPathCommand):
	def __init__(self, parameters):
		super().__init__('l', parameters)
		
	def get_next_vertex(self, current_vertex):	
		next_vertex = (self.parameters[0]+current_vertex[0], self.parameters[1]+current_vertex[1])
		return next_vertex
	
class HSvgPathCommand(SvgPathCommand):
	def __init__(self, parameters):
		super().__init__('H', parameters)
		
	def get_next_vertex(self, current_vertex):	
		next_vertex = (self.parameters[0], current_vertex[1])
		return next_vertex
	
class hSvgPathCommand(SvgPathCommand):
	def __init__(self, parameters):
		super().__init__('h', parameters)
		
	def get_next_vertex(self, current_vertex):	
		next_vertex = (self.parameters[0]+current_vertex[0], current_vertex[1])
		return next_vertex
	
class ZSvgPathCommand(SvgPathCommand):
	def __init__(self, parameters, pathstart=None):
		super().__init__('Z', parameters)
		self._pathstart = pathstart
		
	def get_next_vertex(self, current_vertex):	
		if self._pathstart is not None:
			next_vertex = self._pathstart
		else:
			raise Exception(msg='No path start to go to!')
		return next_vertex
