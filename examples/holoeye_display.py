"""
Holoeye display example.
"""

import numpy as np
import click
from slm_controller import display

# Show a 1x1 checkerboard pattern on the SLM


@click.command()
@click.option("--show_time", type=float, default=5.0, help="Time to show the pattern on the SLM.")
def holoeye_display_example(show_time):

    # instantiate display object
    D = display.HoloeyeDisplay(show_time)

    phaseData = (np.indices((D.height, D.width)).sum(axis=0) % 2) * 255

    # display
    D.imshow(phaseData)


if __name__ == "__main__":
    holoeye_display_example()
