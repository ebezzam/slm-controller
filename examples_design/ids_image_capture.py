"""
IDS camera single image capture example.
"""

from slm_design.hardware import CamDevices
from slm_design import camera
import matplotlib.pyplot as plt


def main():
    # Initialize ids camera
    cam = camera.create_camera(CamDevices.IDS.value)

    # Acquire one image
    image = cam.acquire_images()[0]

    # and plot it using matplotlib
    _, ax = plt.subplots()
    ax.imshow(image, cmap="gray")
    plt.show()


if __name__ == "__main__":
    main()
