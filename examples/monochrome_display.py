"""
Monochrome display example.
"""

import numpy as np
import click
from slm_controller import display, util


@click.command()
@click.option("--file_path", type=str, default=None)
@click.option("--threshold", type=int, default=0.5)
@click.option("--not_original_ratio", is_flag=True)
def monochrome_display_example(file_path, threshold, not_original_ratio):

    # instantiate display object
    D = display.MonochromeDisplay()

    # prepare image data
    if file_path is not None:
        keep_aspect_ratio = not not_original_ratio
        image = util.load_image(
            file_path, output_shape=D.shape, keep_aspect_ratio=keep_aspect_ratio
        )
        image = image / 255.0

    else:
        # random mask
        image = np.random.rand(*D.shape)

    # make binary image
    image = image < threshold

    # display
    D.imshow(image)


if __name__ == "__main__":
    monochrome_display_example()
