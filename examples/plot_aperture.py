import matplotlib.pyplot as plt
from slm_controller.aperture import RectAperture


slm_dim = (10, 16)
apert_dim = (2, 2)

# valid
ap = RectAperture(apert_dim=apert_dim, slm_dim=slm_dim)
ap.plot()
plt.show()
