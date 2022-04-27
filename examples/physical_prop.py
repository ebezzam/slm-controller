import torch
from slm_controller import display
import slm_controller.neural_holography.utils as utils


holoeye_slm_field = torch.load("examples/slm_field_holoeye.pt").angle()
neural_slm_field = torch.load("examples/slm_field.pt").angle()

holoeye_slm_field = utils.phasemap_8bit(holoeye_slm_field)
neural_slm_field = utils.phasemap_8bit(neural_slm_field)

D = display.HoloeyeDisplay(20)

# display
print("Holoeye")
D.imshow(holoeye_slm_field)
print("Neural Holography")
D.imshow(neural_slm_field)
