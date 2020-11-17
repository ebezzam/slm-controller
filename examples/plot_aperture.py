import matplotlib.pyplot as plt
import click
from slm_controller.slm import SLM
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
@click.option("--n_cells", default=10, type=int)
@click.option("--rect_shape", default=None, nargs=2, type=int)
@click.option("--vertical", is_flag=True)
@click.option("--show_tick_labels", is_flag=True)
@click.option("--cell_shape", default=None, nargs=2, type=float)
@click.option("--slm_dim", default=None, nargs=2, type=int)
def plot_aperture(shape, n_cells, rect_shape, vertical, show_tick_labels, cell_shape, slm_dim):
    """
    Plot SLM aperture.

    Parameters
    ----------
    shape : "rect", "square", "line", or "circ"
        Shape of aperture.
    n_cells : int
        Side length for "square", length for "line", radius for "circ". To set shape for "rect", use
        `rect_shape`.
    rect_shape : tuple(int)
        Shape for "rect" in number of cells; `shape` must be set to "rect".
    vertical : bool
        Whether line should be vertical (True) or horizontal (False).
    show_tick_labels : bool
        Whether or not to show cell values along axes.
    cell_shape : tuple
        Shape of cell in meters (height, width).
    slm_dim : tuple
        Dimension of SLM in number of cells (height, width).
    """

    if len(cell_shape) == 0:
        cell_shape = (0.18e-3, 0.18e-3)
    if len(slm_dim) == 0:
        slm_dim = (160, 128)

    # create SLM
    slm = SLM(shape=slm_dim, cell_dim=cell_shape)

    # create aperture
    ap = None
    if shape == ApertureOptions.RECT.value:
        if len(rect_shape) == 0:
            # not provided
            rect_shape = (n_cells, n_cells)
        print(f"Shape : {rect_shape}")
        ap = RectAperture(
            apert_dim=(rect_shape[0] * cell_shape[0], rect_shape[1] * cell_shape[1]), slm=slm
        )
    elif shape == ApertureOptions.LINE.value:
        print(f"Length : {n_cells}")
        length = n_cells * cell_shape[0] if vertical else n_cells * cell_shape[1]
        ap = LineAperture(length=length, slm=slm, vertical=vertical)
    elif shape == ApertureOptions.SQUARE.value:
        print(f"Side length : {n_cells}")
        ap = SquareAperture(side=n_cells * cell_shape[0], slm=slm)
    elif shape == ApertureOptions.CIRC.value:
        print(f"Radius : {n_cells}")
        ap = CircAperture(radius=n_cells * cell_shape[0], slm=slm)
    assert ap is not None

    # plot
    ap.plot(show_tick_labels=show_tick_labels)
    plt.show()


if __name__ == "__main__":
    plot_aperture()
