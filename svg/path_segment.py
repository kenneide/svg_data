from abc import ABC, abstractmethod
import numpy as np


class SvgPathSegment(ABC):
	
	start = None
	end = None
	
	def __init__(self, start, end):
		self.start = start
		self.end = end
			
	@abstractmethod
	def interpolate(self, ratio):
		pass
		
	@abstractmethod
	def length(self):
		pass
	
class LinearSvgPathSegment(SvgPathSegment):
	def __init__(self, start, end):
		super().__init__(start, end)

	def interpolate(self, ratio):
		pass
		
	def length(self):
		(x0, y0) = self.start
		(x1, y1) = self.end
		return np.sqrt((y1-y0)**2+(x1-x0)**2)
		
	def interpolate(self, ratio):
		(x0, y0) = self.start
		(x1, y1) = self.end
		return (ratio*(x1-x0)+x0, ratio*(y1-y0)+y0)
