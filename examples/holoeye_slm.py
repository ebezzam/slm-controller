"""
Holoeye SLM example.
"""

from slm_controller.hardware import SLMDevices
import numpy as np
import click
from slm_controller import slm


@click.command()
@click.option("--show_time", type=float, help="Time to show the pattern on the SLM.")
def holoeye_slm_example(show_time):

    # Instantiate SLM object
    s = slm.create_slm(SLMDevices.HOLOEYE_LC_2012.value)
    if show_time is not None:
        s.set_show_time(show_time)

    # Show a 1x1 checkerboard pattern on the SLM
    phaseData = (np.indices((s.height, s.width)).sum(axis=0) % 2) * 255

    # Display
    s.imshow(phaseData)


if __name__ == "__main__":
    holoeye_slm_example()
