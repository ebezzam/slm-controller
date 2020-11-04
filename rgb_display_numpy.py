"""
Example to display a numpy array
"""

import numpy as np
from rgb import RGBDisplay

# instantiate display object
display = RGBDisplay()

# create random image
width = display.get_width()
height = display.get_height()
numpy_image = np.random.rand(height, width) * 255

# display
display.display_numpy(numpy_image)
