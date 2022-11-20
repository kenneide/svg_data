from svg.handle import SvgHandle
import matplotlib.pyplot as plt
import os

root = 'examples/'

filenames = [
	#'bicycle.svg',
	'ireland.svg',
	#'narrowhouse-skull.svg',
	#'Realistic-Human-Skull.svg',
	#'skullandbones.svg',
]

NUMBER_OF_COORDINATES = 5

for filename in filenames:
	with open(root + '/' + filename, 'r') as file:
		svg_data = file.read()

	svg = SvgHandle(svg_data)

	name = os.path.basename(filename)

	svg.export_to_csv(root + '/' + name + '.csv', NUMBER_OF_COORDINATES)

	svg.plot(NUMBER_OF_COORDINATES)

	plt.show()

plt.close('all')
