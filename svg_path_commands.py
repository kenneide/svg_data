KNOWN_COMMANDS = {
	'M', 'm', 'L', 'l', 'H', 'h', 'V', 'v', 'Z', 'z'
}

required_num_of_parameters = {
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

class SvgPathCommand():
	def __init__(self, type, parameters):
		self.type = type
		self.parameters = parameters

