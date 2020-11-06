"""
Data cube display.
"""

import numpy as np
import click
import display


@click.command()
@click.option("--file_path", type=str, default=None)
@click.option("--rgb", is_flag=True)
def rgb_display_example(file_path, rgb):

    # instantiate display object
    D = display.RGBDisplay()

    # prepare image data
    if file_path is not None:
        image = display.load_image(file_path, width=D.width, height=D.height)
    else:
        if rgb:
            image = np.random.rand(3, *D.shape)
        else:
            image = np.random.rand(*D.shape)

    # display
    D.imshow(image)


if __name__ == "__main__":
    rgb_display_example()
