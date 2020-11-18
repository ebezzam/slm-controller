import matplotlib.pyplot as plt
import click
from slm_controller.aperture import (
    ApertureOptions,
    create_rect_aperture,
    create_line_aperture,
    create_square_aperture,
    create_circ_aperture,
)
from slm_controller.hardware import DeviceOptions, devices, DeviceParam


@click.command()
@click.option(
    "--shape",
    default=ApertureOptions.RECT.value,
    type=click.Choice(ApertureOptions.values()),
    help="Shape of aperture.",
)
@click.option(
    "--n_cells",
    default=10,
    type=int,
    help="Side length for 'square', length for 'line', radius for 'circ'. To set shape for "
    "'rect', use`rect_shape`.",
)
@click.option(
    "--rect_shape",
    default=None,
    nargs=2,
    type=int,
    help="Shape for 'rect' in number of cells; `shape` must be set to 'rect'.",
)
@click.option(
    "--vertical", is_flag=True, help="Whether line should be vertical (True) or horizontal (False)."
)
@click.option(
    "--show_tick_labels", is_flag=True, help="Whether or not to show cell values along axes."
)
@click.option(
    "--cell_dim", default=None, nargs=2, type=float, help="Shape of cell in meters (height, width)."
)
@click.option(
    "--slm_shape",
    default=None,
    nargs=2,
    type=int,
    help="Dimension of SLM in number of cells (height, width).",
)
@click.option("--monochrome", is_flag=True, help="Whether SLM is monochrome.")
@click.option(
    "--device",
    type=click.Choice(DeviceOptions.values()),
    help="Which device to program with aperture.",
)
def plot_aperture(
    shape, n_cells, rect_shape, vertical, show_tick_labels, cell_dim, slm_shape, monochrome, device
):
    """
    Plot SLM aperture.
    """

    if device is None:
        device_config = {
            DeviceParam.CELL_DIM: (0.18e-3, 0.18e-3) if len(cell_dim) == 0 else cell_dim,
            DeviceParam.SLM_SHAPE: (128, 160) if len(slm_shape) == 0 else slm_shape,
            DeviceParam.MONOCHROME: monochrome,
        }
    else:
        device_config = devices[device]

    # create aperture
    ap = None
    if shape == ApertureOptions.RECT.value:
        if len(rect_shape) == 0:
            # not provided
            rect_shape = (n_cells, n_cells)
        print(f"Shape : {rect_shape}")
        apert_dim = (
            rect_shape[0] * device_config[DeviceParam.CELL_DIM][0],
            rect_shape[1] * device_config[DeviceParam.CELL_DIM][1],
        )
        ap = create_rect_aperture(apert_dim=apert_dim, **device_config)
    elif shape == ApertureOptions.LINE.value:
        print(f"Length : {n_cells}")
        length = (
            n_cells * device_config[DeviceParam.CELL_DIM][0]
            if vertical
            else n_cells * device_config[DeviceParam.CELL_DIM][1]
        )
        ap = create_line_aperture(length=length, vertical=vertical, **device_config)
    elif shape == ApertureOptions.SQUARE.value:
        print(f"Side length : {n_cells}")
        ap = create_square_aperture(
            side=n_cells * device_config[DeviceParam.CELL_DIM][0], **device_config
        )
    elif shape == ApertureOptions.CIRC.value:
        print(f"Radius : {n_cells}")
        ap = create_circ_aperture(
            radius=n_cells * device_config[DeviceParam.CELL_DIM][0], **device_config
        )

    assert ap is not None

    # plot
    ap.plot(show_tick_labels=show_tick_labels)
    plt.show()


if __name__ == "__main__":
    plot_aperture()
