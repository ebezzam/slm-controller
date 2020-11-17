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
        P = 0.5
        image = np.random.choice([0, 1], size=D.shape, p=[P, 1 - P])

    # display
    D.imshow(image)

    # # prepare image data
    # if file_path is not None:
    #     keep_aspect_ratio = not not_original_ratio
    #     image = util.load_image(
    #         file_path, output_shape=D.shape, keep_aspect_ratio=keep_aspect_ratio
    #     )
    # else:
    #     if rgb:
    #         image = np.random.rand(3, *D.shape)
    #     else:
    #         image = np.random.rand(*D.shape)
    #
    # # display
    # D.imshow(image)


if __name__ == "__main__":
    monochrome_display_example()
