import numpy as np
from attribute_parser import FunctionParser

def matrix_mult(A, B):
	N = len(A)
	M = len(A[0])
	assert M == len(B)
	K = len(B[0])

	product = []

	for index in range(N):
		product.append([])
		for jndex in range(K):
			product[index].append(0.)
			for kndex in range(M):
				product[index][jndex] += A[index][kndex] * B[kndex][jndex]
				
	return product

class SvgTransformUnknownOperationException(Exception):
	pass
	

class SvgTransform():
	def __init__(self, text=None):
		self.transform_list = []
		self._matrix = [
			[1., 0., 0., 0.],
			[0., 1., 0., 0.],
			[0., 0., 1., 0.],
			[0., 0., 0., 1.],
			]
			
		if text is not None:
			self.add_transform(text)
			
	@property
	def matrix(self):
		return self._matrix
	
	@matrix.setter
	def matrix(self, matrix):
		assert len(matrix) == 4
		assert len(matrix[0]) == 4
		self._matrix = matrix
		
	def add_transform(self, transform_text):
		m = self.convert_text_to_matrix(transform_text)
		self.update_matrix(m)
		self.transform_list.append(transform_text)
		
	def convert_text_to_matrix(self, text):
		parser = FunctionParser()
		if 'translate' in text:
			param = parser.extract_parameters(text)
			if len(param) == 1:
				# if only a single parameters is extracted, the second is assumed to be zero
				param.append(0.)
			x_offset, y_offset = param
			matrix = [
				[1., 0., 0., x_offset],
				[0., 1., 0., y_offset],
				[0., 0., 1., 0.],
				[0., 0., 0., 1.],
				]
		elif 'scale' in text:
			param = parser.extract_parameters(text)
			scale, = param
			matrix = [
				[param[0], 0., 0., 0.],
				[0., param[0], 0., 0.],
				[0., 0., 1., 0.],
				[0., 0., 0., 1.],
				]
		elif 'rotate' in text:
			param = parser.extract_parameters(text)
			angle_deg, = param
			angle_rad = 2*np.pi*angle_deg/360.
			matrix = [
				[np.cos(angle_rad), -np.sin(angle_rad), 0., 0.],
				[np.sin(angle_rad), np.cos(angle_rad), 0., 0.],
				[0., 0., 1., 0.],
				[0., 0., 0., 1.],
				]
		else:
			raise SvgTransformUnknownOperationException
			
		return matrix

	def apply(self, v):
		v_transformed = []
		for x, y in v:
			V = [
				[x],
				[y],
				[0],
				[1],
				]
			Vt = matrix_mult(self._matrix, V)
			v_transformed.append((Vt[0][0], Vt[1][0]))
			
		return v_transformed
			
	def combine(self, text):
		new_transform = self
		new_transform.add_transform(text)
		return new_transform
						
	def update_matrix(self, m):
		self._matrix = matrix_mult(self._matrix, m)
