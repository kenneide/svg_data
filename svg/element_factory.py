from svg.path import SvgPath


class SvgGraphicsElementsFactoryNotImplementedError(NotImplementedError):
	pass
	

class SvgGraphicsElementFactory():
	def __init__(self):
		self.KNOWN_GRAPHICS = ['path']
		
	def get_graphics(self, type, attrib, transform):
		if type in self.KNOWN_GRAPHICS:			
			id = None
			if 'id' in attrib.keys():
				id = attrib['id']
				
			if type == 'path':
				pathdata = None
				if 'id' in attrib.keys():
					id = attrib['id']
				if 'd' in attrib.keys():
					pathdata = attrib['d']
				return SvgPath(id=id, pathdata=pathdata, transform=transform)
		else:
			raise SvgGraphicsElementsFactoryNotImplementedError()
