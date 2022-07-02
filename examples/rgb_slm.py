"""
RGB SLM example.
"""

from slm_controller.hardware import SLMDevices
import numpy as np
import click
from slm_controller import utils, slm


@click.command()
@click.option("--fp", type=str, default=None)
@click.option("--rgb", is_flag=True)
@click.option("--not_original_ratio", is_flag=True)
def rgb_slm_example(fp, rgb, not_original_ratio):

    # instantiate SLM object
    s = slm.create_slm(SLMDevices.ADAFRUIT_RGB.value)

    # prepare image data
    if fp is not None:
        keep_aspect_ratio = not not_original_ratio
        image = utils.load_image(fp, output_shape=s.shape, keep_aspect_ratio=keep_aspect_ratio)

    else:
        image = np.random.rand(3, *s.shape) if rgb else np.random.rand(*s.shape)
        # save new pattern
        fp = "slm_pattern.npy"
        np.save(fp, image)  # TODO why only here?
        print(f"Created random pattern and saved to : {fp}")

    # display
    print(f"Image shape : {image.shape}")
    s.imshow(image)


if __name__ == "__main__":
    rgb_slm_example()
