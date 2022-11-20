import unittest
from test_helper import *
from svg.path_segment import *


class TestLinearSvgPathSegment(unittest.TestCase):
	def test_init(self):
		start = (0., 0.)
		end = (1., 1.)
		segment = LinearSvgPathSegment(start, end)
		self.assertTrue(isinstance(segment, SvgPathSegment))
		
	def test_length(self):
		start = (0., 0.)
		end = (1., 1.)
		segment = LinearSvgPathSegment(start, end)
		length_got = segment.length()
		length_expected = np.sqrt(2)
		self.assertAlmostEqual(length_got, length_expected, places=8)
		
	def test_interpolate(self):
		start = (0., 0.)
		end = (2., 4.)
		segment = LinearSvgPathSegment(start, end)
		point_got = segment.interpolate(0.5)
		point_expected = (1., 2)
		self.assertTrue(tuplesAlmostEqual(point_got, point_expected, places=8))
		
