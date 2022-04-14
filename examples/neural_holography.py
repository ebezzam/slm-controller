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

    final_res = devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.SLM_SHAPE]
    region_of_interest_res = (200, 200)

    image_loader = ImageLoader(
        "examples/",
        channel=0,
        image_res=final_res,
        homography_res=region_of_interest_res,
        shuffle=False,
        vertical_flips=False,
        horizontal_flips=False,
    )

    target_amp, _, _ = image_loader.load_image(0)
    target_amp = target_amp.to(device)

    print(target_amp.min(), target_amp.max())

    init_phase = (-0.5 + 1.0 * torch.rand(1, 1, final_res[0], final_res[1])).to(device)

    print(init_phase.min(), init_phase.max())

    gs = GS(
        0.34,
        520e-9,
        devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.CELL_DIM],
        100,
        device=device,
    )

    final_phase = gs(target_amp, init_phase)

    print(final_phase.min(), final_phase.max())

    phase_out_8bit = phasemap_8bit(final_phase.cpu().detach(), inverted=True)

    print(phase_out_8bit.min(), phase_out_8bit.max())

    # instantiate display object
    D = display.HoloeyeDisplay(show_time)

    # display
    D.imshow(phase_out_8bit)


if __name__ == "__main__":
    neural_holography_example()
