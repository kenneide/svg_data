from svg_handle import SvgHandle
import matplotlib.pyplot as plt

filename = 'ireland.svg'
	
with open(filename, 'r') as file:
	svg_data = file.read()
	
svg = SvgHandle(svg_data)

svg.plot(500)
plt.show()
plt.close('all')
