from svg.path import SvgPath


class SvgGraphicsElementsFactoryNotImplementedError(NotImplementedError):
	pass
	

class SvgGraphicsElementFactory:

	KNOWN_GRAPHICS = ['path']

	def __init__(self):
		pass
		
	def get_graphics(self, type, attrib, transform):
		if type not in self.KNOWN_GRAPHICS:
			raise SvgGraphicsElementsFactoryNotImplementedError()

		id = None
		if 'id' in attrib.keys():
			id = attrib['id']

		if type != 'path':
			raise NotImplementedError

		pathdata = None
		if 'id' in attrib.keys():
			id = attrib['id']
		if 'd' in attrib.keys():
			pathdata = attrib['d']

		return SvgPath(id=id, pathdata=pathdata, transform=transform)


