from svg_transform import *			

class SvgGraphicsElement():
	def __init__(self, id, transform):
		self._id = id
		self._vertices = []
		
		if isinstance(transform, SvgTransform):
			self.transform = transform
		else:
			self.transform = SvgTransform(text=None)		
		
	@property
	def vertices(self):
		return self._vertices
		
	@property
	def transformed_vertices(self):
		return self.transform.apply(self.vertices)
		
	@property
	def id(self):
		return self._id
		
