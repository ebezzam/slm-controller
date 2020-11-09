import matplotlib.pyplot as plt
import click
from slm_controller.aperture import RectAperture


aperture_options = ["rect", "square", "circle", "line"]


@click.command()
@click.option("--shape", default="rect", type=click.Choice(aperture_options))
def plot_aperture(shape):

    # 1.8'' RGB display by Adafruit: https://cdn-shop.adafruit.co3m/datasheets/JD-T1800.pdf
    # pixel_shape = (0.18e-3, 0.18e-3)
    pixel_shape = (0.36e-3, 0.18e-3)
    slm_dim = (10, 16)

    # create aperture
    ap = None
    if shape == "rect":
        apert_dim = (2, 4)
        ap = RectAperture(apert_dim=apert_dim, slm_dim=slm_dim, pixel_shape=pixel_shape)

    # plot
    ap.plot(show_tick_labels=True)
    plt.show()


if __name__ == "__main__":
    plot_aperture()
