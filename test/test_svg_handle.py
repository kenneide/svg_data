import unittest
import os

from svg.handle import *
from svg.element import *
from test_helper import *


class TestSvgHandle(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.complex_xml = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="996.567" height="1074.307" viewBox="1.0 1.0 996.567 1074.307">
	<g id="Group1" transform="scale(2)">
		<g id="Group4" transform="translate(10 10)">
			<path id="Path1" d="M0 0 h2 v2, h-2, z"></path>
		</g>
		<g id="Group5" transform="translate(5, 6)">
			<path id="Path2" d="M20,40l3,2"></path>
		</g>
	</g>
</svg>"""
	
	def test_init(self):
		h = SvgHandle(xml_data=None)
		self.assertTrue(isinstance(h, SvgHandle))
		self.assertEqual(len(h.elements), 0)
		
	def test_get_elements(self):
		h = SvgHandle(xml_data=self.complex_xml)
		ids_expected = ['Path1', 'Path2']
		
		self.assertTrue(isinstance(h.elements, list))
		self.assertEqual(len(h.elements), len(ids_expected))
		
		for element, id_expected in zip(h.elements, ids_expected):
			self.assertTrue(issubclass(type(element), SvgGraphicsElement))
			self.assertEqual(element.id, id_expected)

	def test_transforms_cascade_correctly(self):
		h = SvgHandle(xml_data=self.complex_xml)
		element = h.elements[0]
		vertices = element.transformed_vertices
		expected_vertices = [
			(20.0, 20.0),
			(24.0, 20.0),
			(24.0, 24.0),
			(20.0, 24.0),
			(20.0, 20.0),
		]
		self.assertEqual(len(vertices), 5)
		for vertex, expected_vertex in zip(vertices, expected_vertices):
			self.assertTrue(tuplesAlmostEqual(vertex, expected_vertex, places=8))
		
	def test_export_csv(self):
		xml_data = """
		<svg>
		<path id="path1" d="M0,0l2,2"></path>
		</svg>
		"""
		h = SvgHandle(xml_data)
		
		filename = 'test.csv'
		statusflag = h.export_to_csv(filename, 3)
		
		self.assertEqual(statusflag, 0)
		
		with open(filename, 'r') as file:
			csv_got = file.read()
		os.remove(filename)
		
		csv_expected = """id,x,y,index
path1,0.0,0.0,1
path1,1.0,1.0,2
path1,2.0,2.0,3
"""
		
		print(csv_got)
		print(csv_expected)
		
		self.assertEqual(csv_got, csv_expected)
		
	def test_plot(self):
		h = SvgHandle(xml_data=self.complex_xml)
		
		h.plot(10)
		ax = plt.gca()
		
		x_min, x_max = ax.get_xlim()
		y_min, y_max = ax.get_ylim()
		
		x_min_expected = 1.0
		x_max_expected = 997.567
		y_min_expected = 1.0
		y_max_expected = 1075.307
		
		limits_got = [x_min, x_max, y_min, y_max]
		# y-min and y-max are swapped here because of the axis inversion!
		limits_expected = [x_min_expected, x_max_expected, y_max_expected, y_min_expected]
		for got, expected in zip(limits_got, limits_expected):
			self.assertAlmostEqual(got, expected, places=1)
		
		
