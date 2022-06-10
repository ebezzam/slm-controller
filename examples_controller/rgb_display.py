"""
RGB display example.
"""

from slm_controller.hardware import DisplayDevices
import numpy as np
import click
from slm_controller import display, utils


@click.command()
@click.option("--fp", type=str, default=None)
@click.option("--rgb", is_flag=True)
@click.option("--not_original_ratio", is_flag=True)
def rgb_display_example(fp, rgb, not_original_ratio):

    # instantiate display object
    D = display.create_display(DisplayDevices.ADAFRUIT_RGB.value)

    # prepare image data
    if fp is not None:
        keep_aspect_ratio = not not_original_ratio
        image = utils.load_image(fp, output_shape=D.shape, keep_aspect_ratio=keep_aspect_ratio)

    else:
        image = np.random.rand(3, *D.shape) if rgb else np.random.rand(*D.shape)
        # save new pattern
        fp = "slm_pattern.npy"
        np.save(fp, image)
        print(f"Created random pattern and saved to : {fp}")

    # display
    print(f"Image shape : {image.shape}")
    D.imshow(image)


if __name__ == "__main__":
    rgb_display_example()
