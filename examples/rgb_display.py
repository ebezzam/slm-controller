"""
RGB display example.
"""

import numpy as np
import click
from slm_controller import display, util


@click.command()
@click.option("--fp", type=str, default=None)
@click.option("--rgb", is_flag=True)
@click.option("--not_original_ratio", is_flag=True)
def rgb_display_example(fp, rgb, not_original_ratio):

    # instantiate display object
    D = display.RGBDisplay()

    # prepare image data
    if fp is not None:
        keep_aspect_ratio = not not_original_ratio
        image = util.load_image(fp, output_shape=D.shape, keep_aspect_ratio=keep_aspect_ratio)

    else:
        if rgb:
            image = np.random.rand(3, *D.shape)
        else:
            image = np.random.rand(*D.shape)

        # save new pattern
        fp = "slm_pattern.npy"
        np.save(fp, image)
        print(f"Created random pattern and saved to : {fp}")

    # display
    D.imshow(image)


if __name__ == "__main__":
    rgb_display_example()
