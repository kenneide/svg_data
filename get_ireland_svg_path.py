from bs4 import BeautifulSoup
from svg_path import SvgPath
import csv
import matplotlib.pyplot as plt

filename = 'ireland.svg'

with open(filename, 'r', encoding='utf-8') as svgfile:
	htmldata = BeautifulSoup(svgfile, 'html5lib')
	
svgdata = htmldata.find("svg")
groups = svgdata.find_all('g')

n_coordinates = 100

def get_offset(text):
	first, second = text.split('(')[1].split(' ')
	first = float(first)
	second = float(second[:-1])
	return first, second

fieldnames = ['County', 'x', 'y', 'path']
with open('county_coordinates_100.csv', 'w', encoding='utf-8') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for group in groups:
		county = group['id']
		x_offset, y_offset = get_offset(group['transform'])
		path_tag = group.find('path')
		path = SvgPath(pathdata=path_tag['d'], transform=path_tag['transform'])
		coordinates = path.get_coordinates(n_coordinates)
		path.plot(n_coordinates, x_offset, y_offset)
		for index, (x, y) in enumerate(coordinates):
			entry = dict()
			entry['County'] = county
			entry['x'] = x + x_offset
			entry['y'] = y + y_offset
			entry['path'] = index+1
			writer.writerow(entry)
			
plt.show()
