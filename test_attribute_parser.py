import unittest
from attribute_parser import *

class TestAttributeParser(unittest.TestCase):
	
	def test_init(self):
		parser = NumericalListParser()
		self.assertTrue(issubclass(type(parser), AttributeParser))
		
	def test_parse_list_of_strings(self):
		parser = StringListParser()
		elements_got = parser.parse('1, 2, 3, a', bad_delimiters=[','], good_delimiter=' ')
		elements_expected = ['1', '2', '3', 'a']
		print(elements_got)
		for got, expected in zip(elements_got, elements_expected):
			self.assertEqual(got, expected)
		
	def test_parse_list_of_numbers(self):
		parser = NumericalListParser()
		elements_got = parser.parse('1, 2.5, 3.14, 4', bad_delimiters=[','], good_delimiter=' ')
		elements_expected = [1.0, 2.5, 3.14, 4.0]
		for got, expected in zip(elements_got, elements_expected):
			self.assertAlmostEqual(got, expected, places=8)
			
	def test_parse_mixed_list_of_strings_and_numbers(self):
		parser = MixedListParser()
		elements_got = parser.parse('1, 2.5, M, 4', bad_delimiters=[','], good_delimiter=' ')
		elements_expected = [1.0, 2.5, 'M', 4.0]
		for got, expected in zip(elements_got, elements_expected):
			if type(elements_got) is str:
				self.assertEqual(got, expected)
			else:
				self.assertAlmostEqual(got, expected, places=8)
				
	def test_no_spaces(self):
		parser = MixedListParser()
		elements_got = parser.parse('1,2.5,M,4', bad_delimiters=[','], good_delimiter=' ')
		elements_expected = [1.0, 2.5, 'M', 4.0]
		for got, expected in zip(elements_got, elements_expected):
			if type(elements_got) is str:
				self.assertEqual(got, expected)
			else:
				self.assertAlmostEqual(got, expected, places=8)
		
	def test_multiple_delimiters(self):
		parser = MixedListParser()
		elements_got = parser.parse('1, ,   2.5,M, a', bad_delimiters=[','], good_delimiter=' ')
		elements_expected = [1.0, 2.5, 'M', 'a']
		for got, expected in zip(elements_got, elements_expected):
			if type(elements_got) is str:
				self.assertEqual(got, expected)
			else:
				self.assertAlmostEqual(got, expected, places=8)
		
