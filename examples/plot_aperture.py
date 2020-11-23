import matplotlib.pyplot as plt
import click
from slm_controller.aperture import (
    ApertureOptions,
    rect_aperture,
    line_aperture,
    square_aperture,
    circ_aperture,
)


@click.command()
@click.option(
    "--shape", default=ApertureOptions.RECT.value, type=click.Choice(ApertureOptions.values())
)
@click.option("--n_cells", default=10, type=int)
@click.option("--rect_shape", default=None, nargs=2, type=int)
@click.option("--vertical", is_flag=True)
@click.option("--show_tick_labels", is_flag=True)
@click.option("--cell_dim", default=None, nargs=2, type=float)
@click.option("--slm_shape", default=None, nargs=2, type=int)
def plot_aperture(shape, n_cells, rect_shape, vertical, show_tick_labels, cell_dim, slm_shape):
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
    cell_dim : tuple
        Shape of cell in meters (height, width).
    slm_shape : tuple
        Dimension of SLM in number of cells (height, width).
    """

    if len(cell_dim) == 0:
        cell_dim = (0.18e-3, 0.18e-3)
    if len(slm_shape) == 0:
        slm_shape = (160, 128)

    # create aperture
    ap = None
    if shape == ApertureOptions.RECT.value:
        if len(rect_shape) == 0:
            # not provided
            rect_shape = (n_cells, n_cells)
        print(f"Shape : {rect_shape}")
        apert_dim = rect_shape[0] * cell_dim[0], rect_shape[1] * cell_dim[1]
        ap = rect_aperture(slm_shape=slm_shape, cell_dim=cell_dim, apert_dim=apert_dim)
    elif shape == ApertureOptions.LINE.value:
        print(f"Length : {n_cells}")
        length = n_cells * cell_dim[0] if vertical else n_cells * cell_dim[1]
        ap = line_aperture(slm_shape=slm_shape, cell_dim=cell_dim, length=length, vertical=vertical)
    elif shape == ApertureOptions.SQUARE.value:
        print(f"Side length : {n_cells}")
        ap = square_aperture(slm_shape=slm_shape, cell_dim=cell_dim, side=n_cells * cell_dim[0])
    elif shape == ApertureOptions.CIRC.value:
        print(f"Radius : {n_cells}")
        ap = circ_aperture(slm_shape=slm_shape, cell_dim=cell_dim, radius=n_cells * cell_dim[0])

    assert ap is not None

    # plot
    ap.plot(show_tick_labels=show_tick_labels)
    plt.show()


if __name__ == "__main__":
    plot_aperture()
