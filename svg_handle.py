from bs4 import BeautifulSoup
from svg_path import SvgPath
import xml.etree.ElementTree as ET

CONTAINER_ELEMENT = { 'a', 'defs', 'glyph', 'g', 'marker', 'mask', 'missing-glyph', 'pattern', 'svg', 'switch', 'symbol'}

class SvgHandle():
	def __init__(self, xml_data):
		self._raw_data = xml_data
		self._elementtree = self.construct_tree_from_data()
		self.traverse_tree(self._elementtree, transform_list=[])
		
	def construct_tree_from_data(self):
		if self._raw_data is not None:
			return ET.fromstring(self._raw_data)
		else:
			return None

	def traverse_tree(self, element, transform):
		if 'path' in child.tag:
			return SvgPath(d=child.attrib['d'], transform)		
		elif 'transform' in element.attrib.keys():
				transform_list.append(child.attrib['transform'])
		
		for child in children:
			paths = self.traverse_tree(child, transform_list=transform_list)
			if 'path' in child.tag:
				
			elif 'transform' in child.attrib.keys():
				transform_list.append(child.attrib['transform'])
		
		return 
		
	@property
	def paths(self):
		return [SvgPath(pathtag) for pathtag in self.elements.find_all('path')]
