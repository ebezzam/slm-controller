"""
Physical propagation of the slm pattern generated using the holoeye software.
"""


import click
from slm_controller.hardware import DisplayDevices
from slm_controller import display
import slm_design.neural_holography.utils as utils
from slm_design.transform_fields import load_holoeye_slm_pattern


@click.command()
@click.option("--show_time", type=float, default=5.0, help="Time to show the pattern on the SLM.")
def physical_prop_holoeye(show_time):
    # Load the slm pattern generated using the holoeye software
    holoeye_slm_field = load_holoeye_slm_pattern().angle()
    holoeye_slm_field = utils.phasemap_8bit(holoeye_slm_field)

    # Initialize slm
    D = display.create_display(DisplayDevices.HOLOEYE_LC_2012.value)
    D.set_show_time(show_time)

    # display
    D.imshow(holoeye_slm_field)


if __name__ == "__main__":
    physical_prop_holoeye()
