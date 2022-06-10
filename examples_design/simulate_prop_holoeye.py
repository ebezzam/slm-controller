"""
Simulated propagation of the slm pattern generated using the holoeye software.
"""

from slm_design.utils import show_plot
from slm_design.simulate_prop import lens_prop, lensless_prop
from slm_design.transform_fields import (
    load_holoeye_slm_pattern,
    lens_to_lensless,
)


def simulate_prop_holoeye():
    # Load slm phase map computed with holoeye software
    holoeye_slm_field = load_holoeye_slm_pattern()

    # Make it compliant with the data structure used in the project
    slm_field = holoeye_slm_field[0, 0, :, :]

    # Simulate the propagation in the lens setting and show the results
    propped_slm_field = lens_prop(holoeye_slm_field)[0, 0, :, :]
    show_plot(slm_field, propped_slm_field, "Holoeye with lens")

    # Transform the initial phase map to the lensless setting
    holoeye_slm_field = lens_to_lensless(holoeye_slm_field)
    slm_field = holoeye_slm_field[0, 0, :, :]

    # Simulate the propagation in the lensless setting and show the results
    propped_slm_field = lensless_prop(holoeye_slm_field)[0, 0, :, :]
    show_plot(slm_field, propped_slm_field, "Holoeye without lens")


if __name__ == "__main__":
    simulate_prop_holoeye()
