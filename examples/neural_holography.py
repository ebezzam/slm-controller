"""
Neural holography example.
"""

import numpy as np
import torch
import click
from slm_controller import display
from slm_controller.hardware import DeviceOptions, DeviceParam, devices
from PIL import Image, ImageOps
from slm_controller.neural_holography.module import GS

# Show Holoeye Logo using neural holography code


@click.command()
@click.option("--show_time", type=float, default=5.0, help="Time to show the pattern on the SLM.")
def neural_holography_example(show_time):

    height, width = devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.SLM_SHAPE]
    img = Image.open("examples/HOLOEYE_logo.png")
    img = ImageOps.grayscale(img)
    img = img.resize((height, height))
    padding = int((width - height) / 2)
    target_amp = np.pad(np.array(img), ((0, 0), (padding, padding)), mode="constant")
    target_amp = target_amp[None, None, :, :]
    # PyTorch Complex tensor (torch.cfloat) of size (num_images, 1, height, width)
    target_amp[0, :, :, :] = 1
    target_amp[:, 0, :, :] = 1
    target_amp = torch.from_numpy(target_amp).to("cuda")

    init_phase = np.random.uniform(-np.pi, np.pi, (height, width))
    init_phase = init_phase[None, None, :, :]
    init_phase[0, :, :, :] = 1
    init_phase[:, 0, :, :] = 1
    init_phase = torch.from_numpy(init_phase).to("cuda")

    gs = GS(0.2, 520e-9, devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.CELL_DIM], 100,)
    final_phase = gs(target_amp, init_phase)

    final_phase = final_phase.to("cpu")
    final_phase = final_phase.numpy()
    final_phase = final_phase[0, 0, :, :]

    final_phase = (255 * (final_phase - np.min(final_phase)) / np.ptp(final_phase)).astype(int)

    # instantiate display object
    D = display.HoloeyeDisplay(show_time)

    # display
    D.imshow(final_phase)


if __name__ == "__main__":
    neural_holography_example()
