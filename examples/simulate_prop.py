import torch
import matplotlib.pyplot as plt

from slm_controller.hardware import DeviceOptions, DeviceParam, devices
import slm_controller.neural_holography.utils as utils
from slm_controller.neural_holography.propagation_ASM import propagation_ASM
from slm_controller.transform_fields import (
    load_holoeye,
    load_neural,
    holoeye_with_lens,
    holoeye_without_lens,
    neural_with_lens,
    neural_without_lens,
)

prop_dist = 0.34
wavelength = 532e-9
feature_size = devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.CELL_DIM]
prop_model = "ASM"
propagator = propagation_ASM
dtype = torch.float32
precomputed_H_f = None


def lens_prop(slm_field):
    slm_field = slm_field[None, None, :, :]
    return utils.fftshift(torch.fft.fftn(slm_field, dim=(-2, -1), norm="ortho"))[0, 0, :, :]


def lensless_prop(slm_field):
    slm_field = slm_field[None, None, :, :]
    return utils.propagate_field(
        slm_field,
        propagator,
        prop_dist,
        wavelength,
        feature_size,
        prop_model,
        dtype,
        precomputed_H_f,
    )[0, 0, :, :]


holoeye_slm_field = load_holoeye()
neural_slm_field = load_neural()

propped_holoeye_slm_field = lens_prop(holoeye_with_lens())

# plot
fig = plt.figure()
fig.suptitle("Holoeye with lens")
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
ax1.title.set_text("Phase")
ax2.title.set_text("Amp")
ax3.title.set_text("Prop phase")
ax4.title.set_text("Prop amp")
ax1.imshow(holoeye_slm_field.angle())
ax2.imshow(holoeye_slm_field.abs())
ax3.imshow(propped_holoeye_slm_field.angle())
ax4.imshow(propped_holoeye_slm_field.abs())
plt.show()

propped_holoeye_slm_field = lensless_prop(holoeye_without_lens())

# plot
fig = plt.figure()
fig.suptitle("Holoeye without lens")
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
ax1.title.set_text("Phase")
ax2.title.set_text("Amp")
ax3.title.set_text("Prop phase")
ax4.title.set_text("Prop amp")
ax1.imshow(holoeye_slm_field.angle())
ax2.imshow(holoeye_slm_field.abs())
ax3.imshow(propped_holoeye_slm_field.angle())
ax4.imshow(propped_holoeye_slm_field.abs())
plt.show()

propped_neural_slm_field = lens_prop(neural_with_lens())

# plot
fig = plt.figure()
fig.suptitle("Neural with lens")
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
ax1.title.set_text("Phase")
ax2.title.set_text("Amp")
ax3.title.set_text("Prop phase")
ax4.title.set_text("Prop amp")
ax1.imshow(neural_slm_field.angle())
ax2.imshow(neural_slm_field.abs())
ax3.imshow(propped_neural_slm_field.angle())
ax4.imshow(propped_neural_slm_field.abs())
plt.show()

propped_neural_slm_field = lensless_prop(neural_without_lens())


# plot
fig = plt.figure()
fig.suptitle("Neural without lens")
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
ax1.title.set_text("Phase")
ax2.title.set_text("Amp")
ax3.title.set_text("Prop phase")
ax4.title.set_text("Prop amp")
ax1.imshow(neural_slm_field.angle())
ax2.imshow(neural_slm_field.abs())
ax3.imshow(propped_neural_slm_field.angle())
ax4.imshow(propped_neural_slm_field.abs())
plt.show()
