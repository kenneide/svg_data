import unittest
import numpy as np
from svg_transform import *
from test_helper import *


class TestSvgTransfrom(unittest.TestCase):
	
	def test_init(self):
		t = SvgTransform(text=None)
		self.assertTrue(isinstance(t, SvgTransform))
		
	def test_get_matrix(self):
		t = SvgTransform(text=None)
		matrix_got = t.matrix
		matrix_expected = [
			[1., 0., 0., 0.],
			[0., 1., 0., 0.],
			[0., 0., 1., 0.],
			[0., 0., 0., 1.],
			]
		self.assertTrue(matricesAlmostEqual(matrix_got, matrix_expected, places=8))
		
	def test_translate_matrix(self):
		t = SvgTransform(text='translate(-10 20)')
		matrix_got = t.matrix
		matrix_expected = [
			[1., 0., 0., -10.],
			[0., 1., 0., 20.],
			[0., 0., 1., 0.],
			[0., 0., 0., 1.],
			]
		self.assertTrue(matricesAlmostEqual(matrix_got, matrix_expected, places=8))
				
	def test_scale_matrix(self):
		t = SvgTransform(text='scale(2)')
		matrix_got = t.matrix
		matrix_expected = [
			[2., 0., 0., 0.],
			[0., 2., 0., 0.],
			[0., 0., 1., 0.],
			[0., 0., 0., 1.],
			]
		self.assertTrue(matricesAlmostEqual(matrix_got, matrix_expected, places=8))
		
	def test_rotate_matrix(self):
		t = SvgTransform(text='rotate(45)')
		matrix_got = t.matrix
		matrix_expected = [
			[np.cos(np.pi*0.25), -np.sin(np.pi*0.25), 0., 0.],
			[np.sin(np.pi*0.25), np.cos(np.pi*0.25), 0., 0.],
			[0., 0., 1., 0.],
			[0., 0., 0., 1.],
			]
		self.assertTrue(matricesAlmostEqual(matrix_got, matrix_expected, places=8))

	def test_add_transform(self):
		t = SvgTransform(text='rotate(45)')
		t.add_transform(transform_text='scale(2)')
		matrix_got = t.matrix
		matrix_expected = [
			[2.*np.cos(np.pi*0.25), -2.*np.sin(np.pi*0.25), 0., 0.],
			[2.*np.sin(np.pi*0.25), 2.*np.cos(np.pi*0.25), 0., 0.],
			[0., 0., 1., 0.],
			[0., 0., 0., 1.],
			]
		self.assertTrue(matricesAlmostEqual(matrix_got, matrix_expected, places=8))

	def test_apply_transform(self):
		t = SvgTransform(text='scale(2)')
		points_got = t.apply([(1., 3.), (-2., 10)])
		points_expected = [
			(2., 6.),
			(-4., 20.)
			]
		for point_got, point_expected in zip(points_got, points_expected):
			self.assertTrue(tuplesAlmostEqual(point_got, point_expected, places=8))
								
	def test_matrix_multiplication(self):
		X = [
			[1., 2., 3.],
			[4., 5., 6.],
			[7., 8., 9.],
			[10., 11., 12.]
			]
		Y = [
			[1., 2.],
			[1., 2.],
			[3., 4.]
			]
			
		matrix_got = matrix_mult(X, Y)
		matrix_expected = [
			[12., 18.],
			[27., 42.],
			[42., 66.],
			[57., 90.]
		]
		self.assertTrue(matricesAlmostEqual(matrix_got, matrix_expected, places=8))
