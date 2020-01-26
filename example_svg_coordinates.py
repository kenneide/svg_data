from svg_handle import SvgHandle
import matplotlib.pyplot as plt

filename = './svg/ireland.svg'
	
with open(filename, 'r') as file:
	svg_data = file.read()
	
svg = SvgHandle(svg_data)

filename = './output.csv'
n_coordinates = 50

svg.export_to_csv(filename, n_coordinates)

svg.plot(50)
plt.show()
plt.close('all')
