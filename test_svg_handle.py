import unittest
from svg_handle import *

class TestSvgHandle(unittest.TestCase):
	def test_init(self):
		h = SvgHandle(xml_data=None)
		self.assertTrue(isinstance(h, SvgHandle))
		self.assertTrue(h.elements is None)
		
	def test_get_groups(self):
		xml_data = '<svg><g id="1"></g><g id="2"></g><g id="3"></g></svg>'
		h = SvgHandle(xml_data)
		self.assertEqual(len(h.groups), 3)
	
	def test_get_paths(self):
		xml_data = '<svg><g id="1"><path id=\"Path_1\" d=\"M-40.087,0V5.838\"></path></g><g id="2"></g><g id="3"></g></svg>'
		h = SvgHandle(xml_data)
		self.assertEqual(len(h.paths), 1)
		
						
