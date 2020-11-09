"""
Data cube display.
"""

import numpy as np
import click
from slm_controller import display, util


@click.command()
@click.option("--file_path", type=str, default=None)
@click.option("--rgb", is_flag=True)
@click.option("--not_original_ratio", is_flag=True)
def rgb_display_example(file_path, rgb, not_original_ratio):

    # instantiate display object
    D = display.RGBDisplay()

    # prepare image data
    if file_path is not None:
        keep_aspect_ratio = not not_original_ratio
        image = util.load_image(
            file_path, output_shape=D.shape, keep_aspect_ratio=keep_aspect_ratio
        )
    else:
        if rgb:
            image = np.random.rand(3, *D.shape)
        else:
            image = np.random.rand(*D.shape)

    # display
    D.imshow(image)


if __name__ == "__main__":
    rgb_display_example()