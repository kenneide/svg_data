import unittest
import numpy as np
from svg_path import SvgPath
from svg_transform import SvgTransform
from test_helper import *

class TestSvgPath(unittest.TestCase):
		
	def test_instantiation(self):
		d = 'M 0 0'
		path = SvgPath(d)
		self.assertTrue(isinstance(path, SvgPath))
		
	def test_get_commands(self):
		d = 'M0  0'
		path = SvgPath(d)
		commands = path.commands
		self.assertEqual(len(commands), 1)
		self.assertEqual(commands[0].type, 'M')

	def test_parse_single_command_no_leading_space(self):
		d = 'M0,0'
		path = SvgPath(d)
		commands = path.commands
		self.assertEqual(len(commands), 1)
		self.assertEqual(commands[0].type, 'M')
		self.assertAlmostEqual(commands[0].parameters[0], 0., places=8)
		
	def test_parse_minus_parameters_no_space(self):
		d = 'M-35.6-24.45'
		path = SvgPath(d)
		commands = path.commands
		self.assertEqual(len(commands), 1)
		self.assertEqual(commands[0].type, 'M')
		self.assertAlmostEqual(commands[0].parameters[0], -35.6, places=8)
		self.assertAlmostEqual(commands[0].parameters[1], -24.45, places=8)

	@staticmethod
	def is_correctly_parsed(commands, expected_types, expected_parameters):
		tolerance = 10**-8
		if len(commands) != len(expected_types):
			return False
		for command, type, parameters in zip(commands, expected_types, expected_parameters):
			if not command.type == type:
				return False
			for parameter_got, parameter_expected in zip(command.parameters, parameters):
				if np.abs(parameter_got - parameter_expected) > tolerance:
					return False
		return True

	def test_parse_double_decimal(self):
		d = 'M-36.783-3.471H-49.724L-53.6.408'
		path = SvgPath(d)
		expected_types = ['M', 'H', 'L']
		expected_parameters = [[-36.783, -3.471], [-49.724], [-53.6, 0.408]]
		self.assertTrue(
			self.is_correctly_parsed(path.commands, expected_types, expected_parameters)
		)
		
	def test_parse_single_commands_with_leading_space(self):
		d = 'M 0 0'
		path = SvgPath(d)
		expected_types = ['M']
		expected_parameters = [[0., 0.]]
		self.assertTrue(
			self.is_correctly_parsed(path.commands, expected_types, expected_parameters)
		)
		
	def test_parse_two_commands_with_leading_spaces(self):
		d = 'M 0 0 V 10'
		path = SvgPath(d)
		expected_types = ['M', 'V']
		expected_parameters = [[0., 0.], [10.]]
		self.assertTrue(
			self.is_correctly_parsed(path.commands, expected_types, expected_parameters)
		)
		
	def test_parse_two_commands_with_few_spaces(self):
		d = 'M0 0V10'
		path = SvgPath(d)
		expected_types = ['M', 'V']
		expected_parameters = [[0., 0.], [10.]]
		self.assertTrue(
			self.is_correctly_parsed(path.commands, expected_types, expected_parameters)
		)
		
	def test_parse_commands_with_double_parameters(self):
		d = 'M0,0l10,20,30,40'
		path = SvgPath(d)
		expected_types = ['M', 'l', 'l']
		expected_parameters = [[0., 0.], [10., 20.], [30., 40.]]
		self.assertTrue(
			self.is_correctly_parsed(path.commands, expected_types, expected_parameters)
		)
		
	def test_complex_parse(self):
		d = 'M-36.8-4.738-40.039-1.5v8l-3.991,3.991H-54.2V5.47h-8.813L-67.2,9.654h-10.48v6.384l3.359,3.346V21.6l-5.968,5.968-.837-.837h-5.609v6.39l-5.541,5.541L-96.78,34.16l4.419-4.537V13.354L-96.228,9.48-91.444,4.7-96.6-.461l6.78-6.787h10.5l5.212-5.212h1.742v7.065H-57.8l6.21-6.2h7.939Z'
		path = SvgPath(d)
		
		expected_types = [
			'M', 'M', 'v', 'l', 'H', 'V', 'h', 'L', 'h', 'v', 'l', 'V', 'l', 'l', 'h', 'v',
			'l', 'L', 'l', 'V', 'L', 'L', 'L', 'l', 'h', 'l', 'h', 'v', 'H', 'l', 'h', 'Z'
			]
		
		expected_parameters = [
			[-36.8, -4.738],
			[-40.039, -1.5], 
			[8.], 
			[-3.991, 3.991], 
			[-54.2], 
			[5.47], 
			[-8.813], 
			[-67.2, 9.654],
			[-10.48], 
			[6.384], 
			[3.359, 3.346], 
			[21.6], 
			[-5.968, 5.968], 
			[-0.837, -0.837], 
			[-5.609], 
			[6.39], 
			[-5.541, 5.541], 
			[-96.78, 34.16], 
			[4.419, -4.537], 
			[13.354], 
			[-96.228, 9.48], 
			[-91.444, 4.7], 
			[-96.6, -.461], 
			[6.78, -6.787], 
			[10.5], 
			[5.212, -5.212], 
			[1.742], 
			[7.065], 
			[-57.8], 
			[6.21, -6.2], 
			[7.939],
			[]
			]
			
		self.assertTrue(
			self.is_correctly_parsed(path.commands, expected_types, expected_parameters)
		)
		
	def test_another_complex(self):
		d = 'M-14.2-3.369V6.349 l 9.383, 9.39 0.025, 5.646 H-22.317 L-37.34, 6.362 -26.767 -4.224 V-8.86H-2.6L2.722-3.542v.174Z'
		path = SvgPath(d)
		
		expected_types = [
			'M',
			'V',
			'l',
			'l',
			'H',
			'L',
			'L',
			'V',
			'H',
			'L',
			'v',
			'Z',
			]
		
		expected_parameters = [
			[-14.2, -3.369],
			[6.349],
			[9.383, 9.39],
			[0.025, 5.646],
			[-22.317],
			[-37.34, 6.362],
			[-26.767, -4.224],
			[-8.86],
			[-2.6],
			[2.722, -3.542],
			[0.174],
			[],
			]
			
		self.assertTrue(
			self.is_correctly_parsed(path.commands, expected_types, expected_parameters)
		)
		
						
class TestVerticesAndCoordinates(unittest.TestCase):
			
	def test_horizontal_line_vertices(self):
		# this defines a horizontal line 3 units long, starting at (0,0)
		d = 'M0 0 H3'
		horizontal_line = SvgPath(d)
		expected_vertices = [
			(0., 0.),
			(3., 0.)
			]
		vertices = horizontal_line.vertices
		self.assertEqual(len(vertices), 2)
		for vertex, expected_vertex in zip(vertices, expected_vertices):
			self.assertTrue(tuplesAlmostEqual(vertex, expected_vertex, places=8))
		
	def test_triangle_vertices(self):
		# this defines a horizontal line 3 units long, starting at (0,0)
		d = 'M0 0 H3 l-1.5 1.5 Z'
		triangle = SvgPath(d)
		expected_vertices = [
			(0., 0.),
			(3., 0.),
			(1.5, 1.5),
			(0., 0.)
			]
		vertices = triangle.vertices
		print(vertices)
		for vertex, expected_vertex in zip(vertices, expected_vertices):
			self.assertTrue(tuplesAlmostEqual(vertex, expected_vertex, places=8))
			
	def test_line_length(self):
		d = 'M0 0 H3'
		horizontal_line = SvgPath(d)
		pathlength = horizontal_line.calculate_length()
		expected_pathlength = 3.
		self.assertAlmostEqual(pathlength, expected_pathlength, places=8)
			
	def test_diagonal_line_length(self):
		d = 'M0 0 L1 1'
		diagonal_line = SvgPath(d)
		pathlength = diagonal_line.calculate_length()
		expected_pathlength = np.sqrt(2.)
		self.assertAlmostEqual(pathlength, expected_pathlength, places=8)
		
	def test_line_coordinates(self):
		d = 'M0 0 H3'
		horizontal_line = SvgPath(d)
		coordinates = horizontal_line.get_coordinates(3)
		expected_coordinates = [
			(0.0, 0.0),
			(1.5, 0.0),
			(3.0, 0.0)
			]
		self.assertEqual(len(coordinates), 3)
		for coordinate_pair, expected_coordinate_pair in zip(coordinates, expected_coordinates):
			self.assertTrue(tuplesAlmostEqual(coordinate_pair, expected_coordinate_pair, places=8))
		
	def test_diagonal_line_coordinate(self):
		d = 'M0 0 L1 1'
		diagonal_line = SvgPath(d)
		coordinates = diagonal_line.get_coordinates(5)
		expected_coordinates = [
			(0.00, 0.00),
			(0.25, 0.25),
			(0.50, 0.50),
			(0.75, 0.75),
			(1.00, 1.00)
			]
		self.assertEqual(len(coordinates), 5)
		for coordinate_pair, expected_coordinate_pair in zip(coordinates, expected_coordinates):
			self.assertTrue(tuplesAlmostEqual(coordinate_pair, expected_coordinate_pair, places=8))
		
	def test_box_coordinates(self):
		d = 'M10 10 h2 v2, h-2, z'
		box = SvgPath(d)
		coordinates = box.get_coordinates(9)
		expected_coordinates = [
			(10.0, 10.0),
			(11.0, 10.0),
			(12.0, 10.0),
			(12.0, 11.0),
			(12.0, 12.0),
			(11.0, 12.0),
			(10.0, 12.0),
			(10.0, 11.0),
			(10.0, 10.0)
			]
		print(coordinates)
		self.assertEqual(len(coordinates), 9)
		for coordinate_pair, expected_coordinate_pair in zip(coordinates, expected_coordinates):
			self.assertTrue(tuplesAlmostEqual(coordinate_pair, expected_coordinate_pair, places=8))
	
	def test_transform_translate(self):
		d = 'M0,0H3'
		transform = 'translate(1,2)'
		translated_line = SvgPath(d, transform=SvgTransform(text=transform))
		expected_vertices = [
			(1., 2.),
			(4., 2.)
			]
		vertices = translated_line.vertices
		self.assertEqual(len(vertices), 2)
		for vertex, expected_vertex in zip(vertices, expected_vertices):
			self.assertTrue(tuplesAlmostEqual(vertex, expected_vertex, places=8))
			
	def test_transform_translate_no_second_parameter(self):
		d = 'M0,0H3'
		transform = 'translate(1)'
		translated_line = SvgPath(d, transform=SvgTransform(text=transform))
		expected_vertices = [
			(1., 0.),
			(4., 0.)
			]
		vertices = translated_line.vertices
		self.assertEqual(len(vertices), 2)
		for vertex, expected_vertex in zip(vertices, expected_vertices):
			self.assertTrue(tuplesAlmostEqual(vertex, expected_vertex, places=8))
			
	def test_ignore_resetting_start_points(self):
		d = 'M0,0,1,2,V10Z'
		path = SvgPath(d)
		vertices = path.vertices
		expected_vertices = [
			(0., 0.),
			(1., 2.),
			(1., 10.),
			(0., 0.),
			]
		for vertex, expected_vertex in zip(vertices, expected_vertices):
			self.assertTrue(tuplesAlmostEqual(vertex, expected_vertex, places=8))
