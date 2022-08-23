"""
Adafruit SLM example.
"""

from slm_controller.hardware import SLMDevices, slm_devices, SLMParam
import numpy as np
import click
from slm_controller import slm, utils


@click.command()
@click.option(
    "--file_path",
    type=str,
    default=None,
    help="Path to image to display, create random mask if None.",
)
@click.option(
    "--monochrome", is_flag=True, help="Show monochrome image, otherwise use RGB."
)
@click.option(
    "--not_original_ratio",
    is_flag=True,
    help="Reshape which can distort the image, otherwise scale and crop to match original aspect ratio.",
)
def main(file_path, monochrome, not_original_ratio):
    # prepare image data
    shape = slm_devices[SLMDevices.ADAFRUIT.value][SLMParam.SLM_SHAPE]

    if file_path is not None:
        keep_aspect_ratio = not not_original_ratio
        image = utils.load_image(
            file_path, output_shape=shape, keep_aspect_ratio=keep_aspect_ratio
        )
        
        # TODO quantize image

    else:
        # random mask
        rng = np.random.RandomState(1)
        image = rng.rand(*shape) if monochrome else rng.rand(3, *shape) # TODO quantized version

    # instantiate SLM object
    s = slm.create(SLMDevices.ADAFRUIT.value)

    # display
    s.imshow(image)


if __name__ == "__main__":
    main()
