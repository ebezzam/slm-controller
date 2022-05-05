import matplotlib.pyplot as plt
from slm_controller import display
import slm_controller.neural_holography.utils as utils
from slm_controller.transform_fields import (
    holoeye_with_lens,
    neural_with_lens,
)


holoeye_slm_field = holoeye_with_lens().angle()
neural_slm_field = neural_with_lens().angle()

holoeye_slm_field = utils.phasemap_8bit(holoeye_slm_field)
neural_slm_field = utils.phasemap_8bit(neural_slm_field)

_, ax = plt.subplots()
ax.imshow(holoeye_slm_field)
plt.show()

_, ax = plt.subplots()
ax.imshow(neural_slm_field)
plt.show()

D = display.HoloeyeDisplay(20)

# display
print("Holoeye")
D.imshow(holoeye_slm_field)
print("Neural Holography")
D.imshow(neural_slm_field)
