"""
Binary display example.
"""

from hardware import SlmDisplayDevices
import numpy as np
import click
from slm_controller import display, util


@click.command()
@click.option("--file_path", type=str, default=None)
@click.option("--not_original_ratio", is_flag=True)
def nokia_display_example(file_path, not_original_ratio):

    # instantiate display object
    D = display.create_display(SlmDisplayDevices.NOKIA_5110.value)

    # prepare image data
    if file_path is not None:
        keep_aspect_ratio = not not_original_ratio
        image = util.load_image(
            file_path, output_shape=D.shape, keep_aspect_ratio=keep_aspect_ratio, grayscale=True,
        )
    else:
        # random mask
        image = np.random.rand(*D.shape)

    # display
    D.imshow(image)


if __name__ == "__main__":
    nokia_display_example()
