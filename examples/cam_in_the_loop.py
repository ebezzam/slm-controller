"""
Neural holography example.
"""

from matplotlib import pyplot as plt
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
from slm_controller.neural_holography.module import SGD, PhysicalProp
from slm_controller.neural_holography.utils import phasemap_8bit
from slm_controller.neural_holography.augmented_image_loader import ImageLoader


# Show Holoeye Logo using neural holography code

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
@click.option("--epochs", type=int, default=5, help="Number of epochs.")
@click.option("--show_time", type=float, default=5.0, help="Time to show the pattern on the SLM.")
def cam_in_the_loop(epochs, show_time):
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

    init_phase = (-0.5 + 1.0 * torch.rand(1, 1, *slm_res)).to(device)
    phase = init_phase

    for _ in range(epochs):
        # sgd = SGD(
        #     distance, wavelength, feature_size, iterations, roi_res, device=device
        # )
        # angles = sgd(target_amp, phase).cpu().detach()
        # extended = extend_to_complex(angles)
        # final_phase_sgd = neural_holography_to_lens_setting(extended).angle()

        camera_prop = PhysicalProp()
        captured_amp = camera_prop(init_phase)[0, 0, :, :].numpy()

        ax, _ = plt.subplots()
        ax.imshow(captured_amp, cm="Gray")
        plt.show()

    # phase_out_8bit_sgd = phasemap_8bit(final_phase_sgd)

    # # instantiate display object
    # D = display.HoloeyeDisplay(show_time)

    # # display
    # D.imshow(phase_out_8bit_sgd)


if __name__ == "__main__":
    cam_in_the_loop()
