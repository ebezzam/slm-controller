"""
Binary display example.
"""

from slm_controller.hardware import SLMDevices
import numpy as np
import click
from slm_controller import utils, slm


@click.command()
@click.option("--file_path", type=str, default=None)
@click.option("--not_original_ratio", is_flag=True)
def nokia_display_example(file_path, not_original_ratio):

    # instantiate display object
    s = slm.create_slm(SLMDevices.NOKIA_5110.value)

    # prepare image data
    if file_path is not None:
        keep_aspect_ratio = not not_original_ratio
        image = utils.load_image(
            file_path, output_shape=s.shape, keep_aspect_ratio=keep_aspect_ratio, grayscale=True,
        )
    else:
        # random mask
        image = np.random.rand(*s.shape)

    # display
    s.imshow(image)


if __name__ == "__main__":
    nokia_display_example()
