"""
Physical propagation of slm patterns generated using the SGD algorithm.
"""

import torch
import click
from slm_controller import slm
from slm_controller.hardware import (
    SLMDevices,
    SLMParam,
    slm_devices,
)

from slm_design.hardware import (
    physical_params,
    PhysicalParams,
)
from slm_design.transform_fields import lensless_to_lens
from slm_design.neural_holography.modules import SGD
from slm_design.neural_holography.utils import phasemap_8bit
from slm_design.neural_holography.augmented_image_loader import ImageLoader
from slm_design.utils import extend_to_complex

slm_device = SLMDevices.HOLOEYE_LC_2012.value


# Set parameters
distance = physical_params[PhysicalParams.PROPAGATION_DISTANCE]
wavelength = physical_params[PhysicalParams.WAVELENGTH]
feature_size = slm_devices[slm_device][SLMParam.CELL_DIM]
iterations = 500  # TODO make param

slm_res = slm_devices[slm_device][SLMParam.SLM_SHAPE]
image_res = slm_res

roi_res = (round(slm_res[0] * 0.8), round(slm_res[1] * 0.8))


@click.command()
@click.option("--show_time", type=float, default=5.0, help="Time to show the pattern on the SLM.")
def physical_prop_sgd(show_time):
    # Use GPU if detected in system
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Initialize image loader
    image_loader = ImageLoader(
        "images/target_amplitude",
        image_res=image_res,
        homography_res=roi_res,
        shuffle=False,
        vertical_flips=False,
        horizontal_flips=False,
    )

    # Instantiate display object
    s = slm.create_slm(slm_device)
    s.set_show_time(show_time)

    # Load the the first image in the folder
    target_amp, _, _ = image_loader.load_image(0)

    # Make it grayscale
    target_amp = torch.mean(target_amp, axis=0)

    # Transform the image to be compliant with the neural holography data structure
    target_amp = target_amp[None, None, :, :]
    target_amp = target_amp.to(device)

    # Setup a random initial slm phase map with values in [-0.5, 0.5]
    init_phase = (-0.5 + 1.0 * torch.rand(1, 1, *slm_res)).to(device)

    # Run Stochastic Gradient Descent based method
    sgd = SGD(distance, wavelength, feature_size, iterations, roi_res, device=device)
    angles = sgd(target_amp, init_phase).cpu().detach()

    # Extend the computed angles, aka the phase values, to a complex tensor again
    extended = extend_to_complex(angles)

    # Transform the results to the hardware setting using a lens
    final_phase_sgd = lensless_to_lens(extended).angle()

    # Quantize the the angles, aka phase values, to a bit values
    phase_out_8bit = phasemap_8bit(final_phase_sgd)

    # Display
    s.imshow(phase_out_8bit)


if __name__ == "__main__":
    physical_prop_sgd()
