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
@click.option("--n_pixels", default=10, type=int)
@click.option("--rect_shape", default=None, nargs=2, type=int)
@click.option("--vertical", is_flag=True)
@click.option("--show_tick_labels", is_flag=True)
@click.option("--pixel_shape", default=None, nargs=2, type=float)
@click.option("--slm_dim", default=None, nargs=2, type=int)
def plot_aperture(shape, n_pixels, rect_shape, vertical, show_tick_labels, pixel_shape, slm_dim):
    """
    Plot SLM aperture.

    Parameters
    ----------
    shape : "rect", "square", "line", or "circ"
        Shape of aperture.
    n_pixels : int
        Side length for "square", length for "line", radius for "circ". To set shape for "rect", use
        `rect_shape`.
    rect_shape : tuple
        Shape for "rect"; `shape` must be set to "rect".
    vertical : bool
        Whether line should be vertical (True) or horizontal (False).
    show_tick_labels : bool
        Whether or not to show pixel values along axes.
    pixel_shape : tuple
        Shape of pixel in meters (height, width).
    slm_dim : tuple
        Dimension of SLM in number of pixels (height, width).
    """

    if len(pixel_shape) == 0:
        pixel_shape = (0.18e-3, 0.18e-3)
    if len(slm_dim) == 0:
        slm_dim = (160, 128)

    # create aperture
    ap = None
    if shape == ApertureOptions.RECT.value:
        if len(rect_shape) == 0:
            # not provided
            rect_shape = (n_pixels, n_pixels)
        print(f"Shape : {rect_shape}")
        ap = RectAperture(apert_dim=rect_shape, slm_dim=slm_dim, pixel_shape=pixel_shape)
    elif shape == ApertureOptions.LINE.value:
        print(f"Length : {n_pixels}")
        ap = LineAperture(
            n_pixels=n_pixels, slm_dim=slm_dim, pixel_shape=pixel_shape, vertical=vertical
        )
    elif shape == ApertureOptions.SQUARE.value:
        print(f"Side length : {n_pixels}")
        ap = SquareAperture(side=n_pixels, slm_dim=slm_dim, pixel_shape=pixel_shape)
    elif shape == ApertureOptions.CIRC.value:
        print(f"Radius : {n_pixels}")
        ap = CircAperture(radius=n_pixels, slm_dim=slm_dim, pixel_shape=pixel_shape)
    assert ap is not None

    # plot
    ap.plot(show_tick_labels=show_tick_labels)
    plt.show()


if __name__ == "__main__":
    plot_aperture()
