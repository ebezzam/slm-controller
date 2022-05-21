"""
Neural holography example.
"""

import torch
import click
from slm_controller import display
from slm_controller.hardware import (
    DeviceOptions,
    DeviceParam,
    devices,
    physical_params,
    PhysicalParams,
)
from slm_controller.transform_fields import (
    neural_holography_to_lens_setting,
    extend_to_complex,
)
from slm_controller.neural_holography.module import DPAC
from slm_controller.neural_holography.utils import phasemap_8bit
from slm_controller.neural_holography.augmented_image_loader import ImageLoader


import matplotlib.pyplot as plt
from slm_controller.simulate_prop import lens_prop, lensless_prop
import torch
from slm_controller.neural_holography.augmented_image_loader import ImageLoader

distance = physical_params[PhysicalParams.PROPAGATION_DISTANCE]
wavelength = physical_params[PhysicalParams.WAVELENGTH]
feature_size = devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.CELL_DIM]
iterations = 500

slm_res = devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.SLM_SHAPE]
image_res = slm_res

# image_res = (1080, 1920)
# roi_res = (880, 1600)

# x = roi_res[0] / image_res[0]
# y = roi_res[1] / image_res[1]
# print(image_res[0] * x, image_res[1] * y)
roi_res = (620, 850)  # TODO about 80%


@click.command()
@click.option("--show_time", type=float, default=5.0, help="Time to show the pattern on the SLM.")
def temp(show_time):
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

    target_amp = target_amp[None, None, :, :]
    target_amp = target_amp.to(device)

    dpac = DPAC(distance, wavelength, feature_size, device=device)
    _, angles = dpac(target_amp)
    angles = angles.cpu().detach()
    extended = extend_to_complex(angles)
    final_phase_dpac = neural_holography_to_lens_setting(extended).angle()
    phase_out_8bit_dpac = phasemap_8bit(final_phase_dpac)

    # instantiate display object
    D = display.HoloeyeDisplay(show_time)

    # display
    D.imshow(phase_out_8bit_dpac)
    D.imshow(phasemap_8bit(angles))

    # ===================================================

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

    target_amp = target_amp[None, None, :, :]
    target_amp = target_amp.to(device)

    dpac = DPAC(distance, wavelength, feature_size, device=device)
    _, angles = dpac(target_amp)
    angles = angles.cpu().detach()[0, 0, :, :]

    _, ax = plt.subplots()
    ax.imshow(angles)
    plt.show()

    dpac = DPAC(distance, wavelength, feature_size, device=device)
    _, angles = dpac(target_amp)
    angles = angles.cpu().detach()
    neural_holography_slm_field = extend_to_complex(angles)

    temp = neural_holography_to_lens_setting(neural_holography_slm_field)
    slm_field = temp[0, 0, :, :]
    propped_slm_field = lens_prop(temp)[0, 0, :, :]
    show_plot(slm_field, propped_slm_field, "Neural Holography DPAC with lens")

    slm_field = neural_holography_slm_field[0, 0, :, :]
    propped_slm_field = lensless_prop(neural_holography_slm_field)[0, 0, :, :]
    show_plot(slm_field, propped_slm_field, "Neural Holography DPAC without lens")


def show_plot(slm_field, propped_slm_field, title):
    # plot
    fig = plt.figure()
    fig.suptitle(title)
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)
    ax1.title.set_text("Phase on SLM")
    ax2.title.set_text("Amplitude on SLM")
    ax3.title.set_text("Phase after propagation to screen")
    ax4.title.set_text("Amplitude after propagation to screen")
    ax1.imshow(slm_field.angle())
    ax2.imshow(slm_field.abs())
    ax3.imshow(propped_slm_field.angle())
    ax4.imshow(propped_slm_field.abs())
    plt.show()


if __name__ == "__main__":
    temp()
