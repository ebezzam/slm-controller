"""
Holoeye SLM example.
"""

from slm_controller.hardware import SLMDevices, SLMParam, slm_devices
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
    "--not_original_ratio",
    is_flag=True,
    help="Reshape which can distort the image, otherwise scale and crop to match original aspect ratio.",
)
@click.option(
    "--show_time",
    type=float,
    default=None,
    help="Time to show the mask on the SLM, show indefinitely if None. In that case the user has to kill the script manually.",
)
def main(file_path, not_original_ratio, show_time):
    # prepare image data
    shape = slm_devices[SLMDevices.HOLOEYE_LC_2012.value][SLMParam.SLM_SHAPE]

    if file_path is not None:
        keep_aspect_ratio = not not_original_ratio
        image = utils.load_image(
            file_path,
            output_shape=shape,
            keep_aspect_ratio=keep_aspect_ratio,
            grayscale=True,
        )

        image = utils.quantize(image)

    else:
        # random mask
        rng = np.random.RandomState(1)
        image = rng.randint(low=0, high=np.iinfo(np.uint8).max, size=shape, dtype=np.uint8)

    # instantiate SLM object
    s = slm.create(SLMDevices.HOLOEYE_LC_2012.value)
    s.set_show_time(show_time)

    # display
    s.imshow(image)


if __name__ == "__main__":
    main()
