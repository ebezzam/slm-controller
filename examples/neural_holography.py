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

import matplotlib.pyplot as plt


# Show Holoeye Logo using neural holography code

# image_res = (1080, 1920)
# roi_res = (880, 1600)
# x = roi_res[0] / image_res[0]
# y = roi_res[1] / image_res[1]

# print(x, y)

distance = 0.34
wavelength = 532e-9  # TODO change everywhere, holoeye software?
iterations = 500

slm_res = devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.SLM_SHAPE]
image_res = slm_res

# print(image_res[0] * x, image_res[1] * y)
roi_res = (620, 850)  # TODO about 80%


@click.command()
@click.option("--show_time", type=float, default=5.0, help="Time to show the pattern on the SLM.")
def neural_holography_example(show_time):

    device = "cuda" if torch.cuda.is_available() else "cpu"

    image_loader = ImageLoader(
        "examples/",
        image_res=image_res,
        homography_res=roi_res,
        shuffle=False,
        vertical_flips=False,
        horizontal_flips=False,
    )

    target_amp, _, _ = image_loader.load_image(0)
    target_amp = torch.mean(target_amp, axis=0)

    _, ax = plt.subplots()
    ax.imshow(target_amp)
    plt.title("Target Amplitude Screen")
    plt.show()

    target_amp = target_amp[None, None, :, :]
    target_amp = target_amp.to(device)

    init_phase = (-0.5 + 1.0 * torch.rand(1, 1, *slm_res)).to(device)

    _, ax = plt.subplots()
    ax.imshow(init_phase[0, 0, :, :].cpu().detach())
    plt.title("Initial Phase SLM")
    plt.show()

    gs = GS(
        distance,
        wavelength,
        devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.CELL_DIM],
        iterations,
        device=device,
    )

    # sgd = SGD(
    #     distance,
    #     wavelength,
    #     devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.CELL_DIM],
    #     iterations,
    #     region_of_interest_res,
    #     device=device,
    # )

    # dpac = DPAC(
    #     distance,
    #     wavelength,
    #     devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.CELL_DIM],
    #     device=device,
    # )

    final_phase_gs = gs(target_amp, init_phase).cpu().detach()

    _, ax = plt.subplots()
    ax.imshow(final_phase_gs[0, 0, :, :])
    plt.title("Final Phase SLM")
    plt.show()

    # phase_out_8bit_gs = phasemap_8bit(final_phase_gs, inverted=True)

    # final_phase_sgd = sgd(target_amp, init_phase).cpu().detach()
    # phase_out_8bit_sgd = phasemap_8bit(final_phase_sgd)

    # _, final_phase_dpac = dpac(target_amp).cpu().detach()
    # phase_out_8bit_dpac = phasemap_8bit(final_phase_dpac)

    # instantiate display object
    # D = display.HoloeyeDisplay(show_time)

    # # display
    # D.imshow(phase_out_8bit_gs)
    # # D.imshow(phase_out_8bit_sgd)
    # # D.imshow(phase_out_8bit_dpac)


if __name__ == "__main__":
    neural_holography_example()
