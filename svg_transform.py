import numpy as np

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
		
	def add_transform(self, text):
		m = self.convert_text_to_matrix(text)
		self.update_matrix(m)
		
	def extract_parameters(self, text, num_param):
		parameter_text = text[text.find("(")+1:text.find(")")]
		if num_param == 1:
			parameter_list = [float(parameter_text)]
		if num_param == 2:
			parameter_text = parameter_text.replace(',', ' ')
			while '  ' in parameter_text:
				parameter_text = parameter_text.replace('  ', ' ')
			parameter_list = [float(p) for p in parameter_text.split(' ')]
		return parameter_list
		
	def convert_text_to_matrix(self, text):
		if 'translate' in text:
			param = self.extract_parameters(text, 2)
			if len(param) == 1:
				# if only a single parameters is extracted, the second is assumed to be zero
				param.append(0.)
			m = [
				[1., 0., 0., param[0]],
				[0., 1., 0., param[1]],
				[0., 0., 1., 0.],
				[0., 0., 0., 1.],
				]
		elif 'scale' in text:
			param = self.extract_parameters(text, 1)
			m = [
				[param[0], 0., 0., 0.],
				[0., param[0], 0., 0.],
				[0., 0., 1., 0.],
				[0., 0., 0., 1.],
				]
		elif 'rotate' in text:
			param = self.extract_parameters(text, 1)
			angle = 2*np.pi*param[0]/360.
			m = [
				[np.cos(angle), -np.sin(angle), 0., 0.],
				[np.sin(angle), np.cos(angle), 0., 0.],
				[0., 0., 1., 0.],
				[0., 0., 0., 1.],
				]
		else:
			raise SvgTransformUnknownOperationException
			
		return m

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
			
						
	def update_matrix(self, m):
		self._matrix = matrix_mult(m, self._matrix)
