import unittest
from svg_handle import *
from svg_path import *

complex_xml = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="996.567" height="1074.307" viewBox="0 0 996.567 1074.307">
	<g id="Group_39" data-name="Group 39" transform="translate(-570.214 -227.66)">
		<g id="Group_37" data-name="Group 37" transform="translate(0 307)">
			<g id="Group_36" data-name="Group 36" transform="translate(-410.524 3.027)">
				<g id="Group_31" data-name="Group 31" transform="translate(980.738 175.153)">
					<path id="Path_8" data-name="Path 8" d="M237.5,211.13"></path>
				</g>
				<g id="Group_32" data-name="Group 32" transform="translate(1118.755 720.81)">
					<path id="Path_9" data-name="Path 9" d="M378.345,43.255" transform="translate(114.76 13.12)"></path>
				</g>
				<g id="Group_35" data-name="Group 35" transform="translate(1613.922 425.317)">
					<path id="Path_10" data-name="Path 10" d="M278.81,16.089" transform="translate(84.57 4.88)"></path>
				</g>
				<g id="Group_33" data-name="Group 33" transform="translate(1330.158 355.879)">
					<path id="Path_11" data-name="Path 11" d="M222.1,150.86" transform="translate(67.39 45.76)"></path>
				</g>
				<g id="Group_34" data-name="Group 34" transform="translate(1557.547 345.14)">
					<path id="Path_12" data-name="Path 12" d="M133.852,47.47" transform="translate(40.6 14.4)"></path>
				</g>
			</g>
		</g>
	</g>
</svg>"""


class TestSvgHandle(unittest.TestCase):
	def test_init(self):
		h = SvgHandle(xml_data=None)
		self.assertTrue(isinstance(h, SvgHandle))
		self.assertTrue(h.elements is None)
		
	def test_get_paths(self):
		h = SvgHandle(complex_xml)
		self.assertEqual(h.paths, 5)
		self.assertTrue(isinstance(h.paths[0], SvgPath))
		
	def test_transformed_correctly(self):
		xml_data = ''
		h = SvgHandle(xml_data)
		paths = h.paths[0]
		vertex = paths.get_coordinates(1)
		expected_vertex = [(10., 10.)]
		self.assertEqual(len(h.paths), 1)
		
