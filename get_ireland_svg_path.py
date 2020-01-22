from bs4 import BeautifulSoup
from svg_path import SvgPath
from svg_transform import SvgTransform
import csv
import matplotlib.pyplot as plt

filename = 'ireland.svg'

with open(filename, 'r', encoding='utf-8') as svgfile:
	htmldata = BeautifulSoup(svgfile, 'html5lib')
	
svgdata = htmldata.find("svg")
groups = svgdata.find_all('g')

n_coordinates = 50

fieldnames = ['County', 'x', 'y', 'path']
with open('county_coordinates.csv', 'w', encoding='utf-8') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for group in groups:
		county = group['id']
		t = SvgTransform(group['transform'])
		path_tag = group.find('path')
		t.add_transform(text=path_tag['transform'])
		path = SvgPath(pathdata=path_tag['d'], transform=t)
		coordinates = path.get_coordinates(n_coordinates)
		path.plot(n_coordinates)
		for index, (x, y) in enumerate(coordinates):
			entry = dict()
			entry['County'] = county
			entry['x'] = x
			entry['y'] = y
			entry['path'] = index+1
			writer.writerow(entry)
			
plt.show()
plt.close()
