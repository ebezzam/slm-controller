"""
Data cube display.
"""

import numpy as np

import display


### instantiate display object
D = display.RGBDisplay()

### create image data
I_bw = np.random.rand(*D.shape)
# I_rgb = np.random.rand(3, *D.shape)
# I_file = display.load_image('./blinka.jpg')

### display
D.imshow(I_bw)
# D.imshow(I_rgb)
# D.imshow(I_file)
