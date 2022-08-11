"""
RGB SLM example.
"""

from slm_controller.hardware import SLMDevices
import numpy as np
import click
from slm_controller import slm, utils


@click.command()
@click.option(
    "--file_path",
    type=str,
    default=None,
    help="Path to image to display, create random pattern if None.",
)
@click.option("--monochrome", is_flag=True, help="Show monochrome image, otherwise use RGB.")
@click.option(
    "--not_original_ratio",
    is_flag=True,
    help="Reshape which can distort the image, otherwise scale and crop to match original aspect ratio.",
)
def adafruit_slm_example(file_path, monochrome, not_original_ratio):
    # instantiate SLM object
    s = slm.create(SLMDevices.ADAFRUIT.value)

    # prepare image data
    if file_path is not None:
        keep_aspect_ratio = not not_original_ratio
        image = utils.load_image(
            file_path, output_shape=s.shape, keep_aspect_ratio=keep_aspect_ratio
        )

    else:
        # random mask
        image = np.random.rand(*s.shape) if monochrome else np.random.rand(3, *s.shape)

    # display
    s.imshow(image)


if __name__ == "__main__":
    adafruit_slm_example()
