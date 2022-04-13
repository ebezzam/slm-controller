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
from slm_controller.neural_holography.utils import phasemap_8bit
from slm_controller.neural_holography.augmented_image_loader import ImageLoader

# Show Holoeye Logo using neural holography code


@click.command()
@click.option("--show_time", type=float, default=5.0, help="Time to show the pattern on the SLM.")
def neural_holography_example(show_time):

    device = "cuda" if torch.cuda.is_available() else "cpu"

    slm_res = devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.SLM_SHAPE]
    img_res = slm_res

    image_loader = ImageLoader(
        "examples/",
        channel=0,
        image_res=img_res,
        homography_res=slm_res,
        shuffle=False,
        vertical_flips=False,
        horizontal_flips=False,
    )

    target_amp, _, _ = image_loader.load_image(0)
    target_amp = target_amp.to(device)

    init_phase = (-0.5 + 1.0 * torch.rand(1, 1, slm_res[0], slm_res[1])).to(device)

    gs = GS(
        0.2,
        520e-9,
        devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.CELL_DIM],
        100,
        device=device,
    )
    final_phase = gs(target_amp, init_phase)

    phase_out_8bit = phasemap_8bit(final_phase.cpu().detach(), inverted=True)

    # instantiate display object
    D = display.HoloeyeDisplay(show_time)

    # display
    D.imshow(phase_out_8bit)


if __name__ == "__main__":
    neural_holography_example()
