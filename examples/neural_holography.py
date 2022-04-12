"""
Holoeye display example.
"""

import numpy as np
import click
from slm_controller import display
from slm_controller.hardware import DeviceOptions, DeviceParam, devices
import imageio
from PIL import Image
from neural_holography.module import GS

# Show smiley face using neural holography code


@click.command()
@click.option(
    "--show_time", type=float, default=2.0, help="Time to show the pattern on the SLM."
)
def holoeye_display_example(show_time):

    height, width = devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.SLM_SHAPE]
    img = imageio.imread("smiley.png")
    img = Image.fromarray(img).resize((height, height))
    padding = (width - height) / 2
    img = np.pad(img, [0, padding], mode="constant")
    print(img)

    target_amp = img * 255

    # instantiate display object
    D = display.HoloeyeDisplay(show_time)
    init_phase = np.uniform(-np.pi, np.pi, (D.height, D.width))

    gs = GS()
    final_phase = gs(target_amp, init_phase)

    # display
    D.imshow(final_phase)


if __name__ == "__main__":
    holoeye_display_example()
