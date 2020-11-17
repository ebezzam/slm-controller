"""
Monochrome display example.
"""

import numpy as np
import click
from slm_controller import display, util


@click.command()
@click.option("--file_path", type=str, default=None)
@click.option("--not_original_ratio", is_flag=True)
def monochrome_display_example(file_path, not_original_ratio):

    # instantiate display object
    D = display.MonochromeDisplay()

    # prepare image data
    if file_path is not None:
        raise NotImplementedError
    else:
        # random mask
        P = 0.5
        image = np.random.rand(*D.shape)
        image = image < P

    # display
    D.imshow(image)


if __name__ == "__main__":
    monochrome_display_example()
