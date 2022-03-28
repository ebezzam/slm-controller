"""
Holoeye display example.
"""

import numpy as np
from slm_controller import display

# Calculates a lens using numpy and show it on the SLM.
# Taken from the Holoeye code examples lens.py

import math

# TODO is not persistent!


def holoeye_display_example():

    # instantiate display object
    D = display.HoloeyeDisplay()

    # Configure the lens properties:
    innerRadius = D.height / 3
    centerX = 0
    centerY = 0

    # Calculate the phase values of a lens in a pixel-wise matrix:

    # pre-calc. helper variables:
    phaseModulation = 2 * math.pi
    dataWidth = D.width
    dataHeight = D.height

    x = (
        np.linspace(1, dataWidth, dataWidth, dtype=np.float32)
        - np.float32(dataWidth / 2)
        - np.float32(centerX)
    )
    y = (
        np.linspace(1, dataHeight, dataHeight, dtype=np.float32)
        - np.float32(dataHeight / 2)
        - np.float32(centerY)
    )

    x2 = np.matrix(x * x)
    y2 = np.matrix(y * y).transpose()

    phaseData = (
        np.float32(phaseModulation)
        * np.array(
            (
                np.dot(np.ones([dataHeight, 1], np.float32), x2)
                + np.dot(y2, np.ones([1, dataWidth], np.float32))
            ),
            dtype=np.float32,
        )
        / np.float32(innerRadius * innerRadius)
    )

    # display
    D.imshow(phaseData)


if __name__ == "__main__":
    holoeye_display_example()
