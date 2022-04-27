import torch
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from slm_controller.hardware import DeviceOptions, DeviceParam, devices
import slm_controller.neural_holography.utils as utils
from slm_controller.neural_holography.propagation_ASM import propagation_ASM

prop_dist = 0.34
wavelength = 532e-9
feature_size = devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.CELL_DIM]
phase_path = None
prop_model = "ASM"
propagator = propagation_ASM
writer = None
dtype = torch.float32
precomputed_H_f = None
precomputed_H_b = None

im = Image.open("examples/holoeye_slm_pattern.png")
im = torch.from_numpy(np.array(im)).type(torch.FloatTensor)
im = torch.mean(im, axis=2)

print(torch.min(im), torch.max(im))  # TODO max only 254 ??

max_val = torch.max(im)

angles = (im / max_val) * (2 * np.pi) - np.pi

mags = torch.ones_like(im)

holoeye_slm_field = torch.polar(mags, angles)
holoeye_slm_field = holoeye_slm_field[None, None, :, :]

torch.save(holoeye_slm_field, "examples/slm_field_holoeye.pt")

neural_slm_field = torch.load("examples/slm_field.pt")

print(holoeye_slm_field.angle().numpy()[0, 0, :, :].min())
print(neural_slm_field.angle().numpy()[0, 0, :, :].min())
print(holoeye_slm_field.angle().numpy()[0, 0, :, :].max())
print(neural_slm_field.angle().numpy()[0, 0, :, :].max())
print(holoeye_slm_field.abs().numpy()[0, 0, :, :].min())
print(neural_slm_field.abs().numpy()[0, 0, :, :].min())
print(holoeye_slm_field.abs().numpy()[0, 0, :, :].max())
print(neural_slm_field.abs().numpy()[0, 0, :, :].max())


res_image = utils.propagate_field(
    holoeye_slm_field,
    propagator,
    prop_dist,
    wavelength,
    feature_size,
    prop_model,
    dtype,
    precomputed_H_f,
)

res_image = res_image.abs().numpy()[0, 0, :, :]

# plot
_, ax = plt.subplots()
ax.imshow(res_image)
plt.show()

res_image = utils.propagate_field(
    neural_slm_field,
    propagator,
    prop_dist,
    wavelength,
    feature_size,
    prop_model,
    dtype,
    precomputed_H_f,
)

res_image = res_image.abs().numpy()[0, 0, :, :]

_, ax = plt.subplots()
ax.imshow(res_image)
plt.show()
