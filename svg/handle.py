import xml.etree.ElementTree as ET
import copy
import csv
from typing import Iterable

import matplotlib.pyplot as plt
import re

from svg.transform import SvgTransform
from svg.element_factory import SvgGraphicsElementFactory

from svg.attribute_parser import FunctionParser


def get_xml_namespace(element):
    m = re.match(r'\{.*\}', element.tag)
    return m.group(0) if m else ''


class SvgHandle:
    def __init__(self, xml_data):
        self._xml_data = xml_data
        self._factory = SvgGraphicsElementFactory()
        self._elements = []

        self.x_offset = None
        self.y_offset = None
        self.width = None
        self.height = None

        if self._xml_data is not None:
            self._elementtree = ET.fromstring(self._xml_data)
            self._xml_namespace = get_xml_namespace(self._elementtree)
            self.populate_elements(self._elementtree, transform=SvgTransform())

    def populate_elements(self, element, transform):
        if 'transform' in element.attrib.keys():
            transform = transform.combine(element.attrib['transform'])

        if 'svg' in element.tag and 'viewBox' in element.attrib.keys():
            parser = FunctionParser()
            parameters = parser.extract_parameters(element.attrib['viewBox'])
            self.x_offset, self.y_offset, self.width, self.height = parameters

        tag = element.tag.replace(self._xml_namespace, '')
        if tag in self._factory.KNOWN_GRAPHICS:
            graphics = self._factory.get_graphics(type=tag,
                                                  attrib=element.attrib,
                                                  transform=transform)
            self._elements.append(graphics)

        for child_element in list(element):
            self.populate_elements(child_element, copy.deepcopy(transform))

    @property
    def elements(self):
        return self._elements

    def export_to_csv(self, filename, n_coordinates):
        fieldnames = ['id', 'x', 'y', 'index']
        with open(filename, 'w', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for element in self.elements:
                pathtable = element.export(n_coordinates)
                for index, x, y in zip(pathtable['index'], pathtable['x'], pathtable['y']):
                    entry = dict()
                    entry['id'] = pathtable['id']
                    entry['x'] = x
                    entry['y'] = y
                    entry['index'] = index
                    writer.writerow(entry)
        return 0

    def plot(self, n_coordinates=None):
        plt.figure()
        for element in self.elements:
            element.plot(n_coordinates)

        if self.x_offset is None or self.y_offset is None or self.width is None or self.height is None:
            return

        ax = plt.gca()
        ax.set_xlim((self.x_offset, self.x_offset + self.width))
        ax.set_ylim((self.y_offset, self.y_offset + self.height))
        ax.invert_yaxis()
