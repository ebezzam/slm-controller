import matplotlib.pyplot as plt
import click
from slm_controller.aperture import (
    ApertureOptions,
    RectAperture,
    LineAperture,
    SquareAperture,
    CircAperture,
)


@click.command()
@click.option(
    "--shape", default=ApertureOptions.RECT.value, type=click.Choice(ApertureOptions.values())
)
def plot_aperture(shape):

    pixel_shape = (0.36e-3, 0.18e-3)
    slm_dim = (10, 16)

    # create aperture
    ap = None
    show_tick_labels = True
    if shape == ApertureOptions.RECT.value:
        ap = RectAperture(apert_dim=(2, 4), slm_dim=slm_dim, pixel_shape=pixel_shape)
    elif shape == ApertureOptions.LINE.value:
        ap = LineAperture(n_pixels=6, slm_dim=slm_dim, pixel_shape=pixel_shape, vertical=False)
    elif shape == ApertureOptions.SQUARE.value:
        ap = SquareAperture(side=4, slm_dim=slm_dim, pixel_shape=pixel_shape)
    elif shape == ApertureOptions.CIRC.value:
        pixel_shape = (0.18e-3, 0.18e-3)
        slm_dim = (100, 120)
        show_tick_labels = False
        ap = CircAperture(radius=20, slm_dim=slm_dim, pixel_shape=pixel_shape)
    assert ap is not None

    # plot
    ap.plot(show_tick_labels=show_tick_labels)
    plt.show()


if __name__ == "__main__":
    plot_aperture()
