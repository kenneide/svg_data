import numpy as np

def tuplesAlmostEqual(tuple_got, tuple_expected, places):
		assert len(tuple_got) == len(tuple_expected)
		tolerance = 10.**-float(places)
		for float_got, float_expected in zip(tuple_got, tuple_expected):
			if np.abs(float_got - float_expected) > tolerance:
				return False
		return True
		
def matricesAlmostEqual(matrix_got, matrix_expected, places):
		N = len(matrix_got)
		M = len(matrix_got[0])
		assert N == len(matrix_expected)
		assert M == len(matrix_expected[0])
				
		tolerance = 10.**-float(places)
		for index in range(N):
			for jndex in range(M):
				if np.abs(matrix_got[index][jndex] - matrix_expected[index][jndex]) > tolerance:
					return False
		return True
