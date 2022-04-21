"""
Neural holography example.
"""

import torch
import click
from slm_controller import display
from slm_controller.hardware import DeviceOptions, DeviceParam, devices
from slm_controller.neural_holography.module import GS, SGD, DPAC
from slm_controller.neural_holography.utils import phasemap_8bit
from slm_controller.neural_holography.augmented_image_loader import ImageLoader

# Show Holoeye Logo using neural holography code

distance = 0.34
wavelength = 520e-9
iterations = 100

final_res = devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.SLM_SHAPE]
region_of_interest_res = (200, 200)


@click.command()
@click.option("--show_time", type=float, default=5.0, help="Time to show the pattern on the SLM.")
def neural_holography_example(show_time):

    device = "cuda" if torch.cuda.is_available() else "cpu"

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

    init_phase = (-0.5 + 1.0 * torch.rand(1, 1, final_res[0], final_res[1])).to(device)

    gs = GS(
        distance,
        wavelength,
        devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.CELL_DIM],
        iterations,
        device=device,
    )

    sgd = SGD(
        distance,
        wavelength,
        devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.CELL_DIM],
        iterations,
        device=device,
    )

    dpac = DPAC(
        distance,
        wavelength,
        devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.CELL_DIM],
        device=device,
    )

    final_phase_gs = gs(target_amp, init_phase)
    phase_out_8bit_gs = phasemap_8bit(final_phase_gs.cpu().detach())

    final_phase_sgd = sgd(target_amp, init_phase)
    phase_out_8bit_sgd = phasemap_8bit(final_phase_sgd.cpu().detach())

    _, final_phase_dpac = dpac(target_amp)
    phase_out_8bit_dpac = phasemap_8bit(final_phase_dpac.cpu().detach())

    # instantiate display object
    D = display.HoloeyeDisplay(show_time)

    # display
    D.imshow(phase_out_8bit_gs)
    D.imshow(phase_out_8bit_sgd)
    D.imshow(phase_out_8bit_dpac)


if __name__ == "__main__":
    neural_holography_example()
