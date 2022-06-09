"""
IDS camera single image capture example.
"""

from slm_controller.camera import IDSCamera
import matplotlib.pyplot as plt


def main():
    # Initialize ids camera
    camera = IDSCamera()

    # Acquire one image
    image = camera.acquire_images()[0]

    # and plot it using matplotlib
    _, ax = plt.subplots()
    ax.imshow(image, cmap="gray")
    plt.show()


if __name__ == "__main__":
    main()
