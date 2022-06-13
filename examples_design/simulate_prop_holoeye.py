"""
Simulated propagation of the slm pattern generated using the holoeye software.
"""

from slm_design.utils import load_holoeye_slm_pattern, show_plot
from slm_design.simulate_prop import (
    lens_prop,
    lensless_prop,
    wave_prop_angular_spectrum,
    wave_prop_angular_spectrum_np,
    wave_prop_fft_di,
    wave_prop_direct_integration,
    wave_prop_fraunhofer,
    wave_prop_fresnel_one_step,
    wave_prop_fresnel_two_step,
    wave_prop_fresnel_multi_step,
    wave_prop_fresnel_conv,
    wave_prop_shifted_fresnel,
    wave_prop_spherical,
)
from slm_design.transform_fields import lens_to_lensless


def simulate_prop_holoeye():
    # Load slm phase map computed with holoeye software
    holoeye_slm_field = load_holoeye_slm_pattern()

    # Make it compliant with the data structure used in the project
    slm_field = holoeye_slm_field[0, 0, :, :]  # TODO improve this data structure!

    # Simulate the propagation in the lens setting and show the results
    propped_slm_field = lens_prop(holoeye_slm_field)[0, 0, :, :]
    show_plot(slm_field, propped_slm_field, "Holoeye with lens")

    # TODO test those
    # ==========================================================================
    propped_slm_field = wave_prop_fraunhofer(holoeye_slm_field)[0, 0, :, :]
    show_plot(slm_field, propped_slm_field, "Holoeye with Fraunhofer")

    propped_slm_field = wave_prop_angular_spectrum(holoeye_slm_field)[0, 0, :, :]
    show_plot(slm_field, propped_slm_field, "Holoeye with Angular Spectrum")

    propped_slm_field = wave_prop_angular_spectrum_np(holoeye_slm_field)[0, 0, :, :]
    show_plot(slm_field, propped_slm_field, "Holoeye with Angular Spectrum NP")

    # propped_slm_field = wave_prop_fft_di(holoeye_slm_field)[0, 0, :, :] #TODO add those! All?
    # show_plot(slm_field, propped_slm_field, "Holoeye with FFT Direct")

    propped_slm_field = wave_prop_direct_integration(holoeye_slm_field)[0, 0, :, :]
    show_plot(slm_field, propped_slm_field, "Holoeye with Direct Integration")

    propped_slm_field = wave_prop_fresnel_one_step(holoeye_slm_field)[0, 0, :, :]
    show_plot(slm_field, propped_slm_field, "Holoeye with Fresnel One Step")

    # propped_slm_field = wave_prop_fresnel_two_step(holoeye_slm_field)[0, 0, :, :]
    # show_plot(slm_field, propped_slm_field, "Holoeye with Fresnel Two Step")

    # propped_slm_field = wave_prop_fresnel_multi_step(holoeye_slm_field)[0, 0, :, :]
    # show_plot(slm_field, propped_slm_field, "Holoeye with Fresnel Multi Step")

    propped_slm_field = wave_prop_fresnel_conv(holoeye_slm_field)[0, 0, :, :]
    show_plot(slm_field, propped_slm_field, "Holoeye with Fresnel Convolution")

    propped_slm_field = wave_prop_shifted_fresnel(holoeye_slm_field)[0, 0, :, :]
    show_plot(slm_field, propped_slm_field, "Holoeye with Shifted Fresnel")

    # propped_slm_field = wave_prop_spherical(holoeye_slm_field)[0, 0, :, :]
    # show_plot(slm_field, propped_slm_field, "Holoeye with Spherical")

    # ==========================================================================

    # Transform the initial phase map to the lensless setting
    holoeye_slm_field = lens_to_lensless(holoeye_slm_field)
    slm_field = holoeye_slm_field[0, 0, :, :]

    # Simulate the propagation in the lensless setting and show the results
    propped_slm_field = lensless_prop(holoeye_slm_field)[0, 0, :, :]
    show_plot(slm_field, propped_slm_field, "Holoeye without lens")


if __name__ == "__main__":
    simulate_prop_holoeye()
