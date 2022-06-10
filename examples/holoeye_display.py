"""
Holoeye display example.
"""

from hardware import SlmDisplayDevices
import numpy as np
import click
from slm_controller import display


@click.command()
@click.option("--show_time", type=float, default=5.0, help="Time to show the pattern on the SLM.")
def holoeye_display_example(show_time):

    # Instantiate display object
    D = display.create_display(SlmDisplayDevices.HOLOEYE_LC_2012.value)
    D.set_show_time(show_time)

    # Show a 1x1 checkerboard pattern on the SLM
    phaseData = (np.indices((D.height, D.width)).sum(axis=0) % 2) * 255

    # Display
    D.imshow(phaseData)


if __name__ == "__main__":
    holoeye_display_example()
