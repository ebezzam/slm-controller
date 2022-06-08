"""
Physical propagation of slm patterns generated using the neural holography code.
"""

import torch
import click
from slm_controller import display
from slm_controller.hardware import (
    SlmDevices,
    SlmParam,
    slm_devices,
    physical_params,
    PhysicalParams,
)
from slm_controller.transform_fields import (
    lensless_to_lens,
    extend_to_complex,
)
from slm_controller.neural_holography.module import GS, SGD, DPAC
from slm_controller.neural_holography.utils import phasemap_8bit
from slm_controller.neural_holography.augmented_image_loader import ImageLoader

# Set parameters
distance = physical_params[PhysicalParams.PROPAGATION_DISTANCE]
wavelength = physical_params[PhysicalParams.WAVELENGTH]
feature_size = slm_devices[SlmDevices.HOLOEYE_LC_2012.value][SlmParam.CELL_DIM]
iterations = 500

slm_res = slm_devices[SlmDevices.HOLOEYE_LC_2012.value][SlmParam.SLM_SHAPE]
image_res = slm_res

roi_res = (620, 850)  # TODO about 80%


@click.command()
@click.option("--show_time", type=float, default=5.0, help="Time to show the pattern on the SLM.")
def physical_prop_neural_holography(show_time):
    # Use GPU if detected in system
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Initialize image loader
    image_loader = ImageLoader(
        "images/test",
        image_res=image_res,
        homography_res=roi_res,
        shuffle=False,
        vertical_flips=False,
        horizontal_flips=False,
    )

    # Instantiate display object
    D = display.HoloeyeDisplay(show_time)

    # Load the the first image in the folder
    target_amp, _, _ = image_loader.load_image(0)

    # Make it grayscale
    target_amp = torch.mean(target_amp, axis=0)

    # Transform the image to be compliant with the neural holography data structure
    target_amp = target_amp[None, None, :, :]
    target_amp = target_amp.to(device)

    # Setup a random initial slm phase map with values in [-0.5, 0.5]
    init_phase = (-0.5 + 1.0 * torch.rand(1, 1, *slm_res)).to(device)

    # Run Gerchberg-Saxton
    print("--- Run Gerchberg-Saxton ---")
    gs = GS(distance, wavelength, feature_size, iterations, device=device)
    angles = gs(target_amp, init_phase).cpu().detach()

    # Extend the computed angles, aka the phase values, to a complex tensor again
    extended = extend_to_complex(angles)

    # Transform the results to the hardware setting using a lens
    final_phase_gs = lensless_to_lens(extended).angle()

    # Quantize the the angles, aka phase values, to a bit values
    phase_out_8bit_gs = phasemap_8bit(final_phase_gs)

    # Display
    D.imshow(phase_out_8bit_gs)

    # Run Stochastic Gradient Descent based method
    print("--- Run SGD ---")
    sgd = SGD(distance, wavelength, feature_size, iterations, roi_res, device=device)
    angles = sgd(target_amp, init_phase).cpu().detach()

    # Extend the computed angles, aka the phase values, to a complex tensor again
    extended = extend_to_complex(angles)

    # Transform the results to the hardware setting using a lens
    final_phase_sgd = lensless_to_lens(extended).angle()

    # Quantize the the angles, aka phase values, to a bit values
    phase_out_8bit_sgd = phasemap_8bit(final_phase_sgd)

    # Display
    D.imshow(phase_out_8bit_sgd)

    # Run Double Phase Amplitude Coding #TODO does not work, not even out of the
    # box
    print("--- Run DPAC (buggy) ---")
    dpac = DPAC(distance, wavelength, feature_size, device=device)
    _, angles = dpac(target_amp)
    angles = angles.cpu().detach()

    # Extend the computed angles, aka the phase values, to a complex tensor again
    extended = extend_to_complex(angles)

    # Transform the results to the hardware setting using a lens
    final_phase_dpac = lensless_to_lens(extended).angle()

    # Quantize the the angles, aka phase values, to a bit values
    phase_out_8bit_dpac = phasemap_8bit(final_phase_dpac)

    # Display
    D.imshow(phase_out_8bit_dpac)


if __name__ == "__main__":
    physical_prop_neural_holography()
