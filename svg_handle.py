from bs4 import BeautifulSoup
from svg_path import SvgPath


import xml.parsers.expat

# 3 handler functions
def start_element(name, attrs):
    print('Start element:', name, attrs)
def end_element(name):
    print('End element:', name)
def char_data(data):
    print('Character data:', repr(data))

class SvgHandle():
	def __init__(self, xml_data):
		self._raw_data = xml_data
		self._elements = self.import_data()
		
	def import_data(self):
		if self._raw_data is not None:
			return BeautifulSoup(self._raw_data, 'html5lib')
		else:
			return None
			
	def parse(self):
				
		parser = xml.parsers.expat.ParserCreate()
		
		parser.StartElementHandler = start_element
		parser.EndElementHandler = end_element
		parser.CharacterDataHandler = char_data
		
		parser.Parse(xml_data, 1)
		
	@property
	def elements(self):
		return self._elements
		
	@property
	def groups(self):
		return self.elements.find_all('g')
		
	@property
	def paths(self):
		return [SvgPath(pathtag) for pathtag in self.elements.find_all('path')]
