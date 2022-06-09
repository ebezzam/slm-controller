"""
Holoeye display example.
"""

import numpy as np
import click
from slm_controller import display

# TODO use factory methods to create both cameras and displays


@click.command()
@click.option("--show_time", type=float, default=5.0, help="Time to show the pattern on the SLM.")
def holoeye_display_example(show_time):

    # Instantiate display object
    D = display.HoloeyeDisplay(show_time)

    # Show a 1x1 checkerboard pattern on the SLM
    phaseData = (np.indices((D.height, D.width)).sum(axis=0) % 2) * 255

    # Display
    D.imshow(phaseData)


if __name__ == "__main__":
    holoeye_display_example()
