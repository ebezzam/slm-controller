from slm_controller.camera import IDS
import matplotlib.pyplot as plt
from PIL import Image


def main():
    camera = IDS()

    image = camera.acquire_image()
    _, ax = plt.subplots()
    ax.imshow(image, cmap="gray")
    plt.show()

    # image = camera.acquire_image()
    # im = Image.fromarray(image)
    # im.save(f"frame_{camera.frame}.png")

    image = camera.acquire_image()
    _, ax = plt.subplots()
    ax.imshow(image, cmap="gray")
    plt.show()

    image = camera.acquire_image()
    _, ax = plt.subplots()
    ax.imshow(image, cmap="gray")
    plt.show()

    image = camera.acquire_image()
    _, ax = plt.subplots()
    ax.imshow(image, cmap="gray")
    plt.show()


if __name__ == "__main__":
    main()
