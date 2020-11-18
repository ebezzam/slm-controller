import click
from slm_controller.display import create_display
from slm_controller.aperture import (
    create_rect_aperture,
    create_line_aperture,
    create_square_aperture,
    create_circ_aperture,
    ApertureOptions,
)
from slm_controller.hardware import devices, DeviceOptions, DeviceParam


@click.command()
@click.option(
    "--shape", default=ApertureOptions.SQUARE.value, type=click.Choice(ApertureOptions.values())
)
@click.option("--n_cells", default=10, type=int)
@click.option("--rect_shape", default=None, nargs=2, type=int)
@click.option("--vertical", is_flag=True)
@click.option(
    "--device", default=DeviceOptions.ADAFRUIT_RGB.value, type=click.Choice(DeviceOptions.values())
)
def set_aperture(shape, n_cells, rect_shape, vertical, device):
    """
    Set aperture for the 1.8 inch RGB display by Adafruit.

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
    device : "rgb" or "mono"
        Which device to program with aperture.
    """

    # check input parameters
    if len(rect_shape) > 0 and shape is not ApertureOptions.RECT.value:
        raise ValueError("Received [rect_shape], but [shape] parameters is not 'rect'.")
    if vertical and shape is not ApertureOptions.LINE.value:
        raise ValueError("Received [vertical] flag, but [shape] parameters is not 'line'.")

    # print device info
    cell_dim = devices[device][DeviceParam.CELL_DIM]
    slm_shape = devices[device][DeviceParam.SLM_SHAPE]
    print(f"SLM dimension : {slm_shape}")
    print(f"Cell dim (m) : {cell_dim}")
    if shape == ApertureOptions.LINE.value:
        if vertical:
            print("Aperture shape : vertical line")
        else:
            print("Aperture shape : horizontal line")
    else:
        print(f"Aperture shape : {shape}")

    # create aperture mask
    ap = None
    if shape == ApertureOptions.LINE.value:
        print(f"Length : {n_cells}")
        length = n_cells * cell_dim[0] if vertical else n_cells * cell_dim[1]
        ap = create_line_aperture(
            slm_shape=slm_shape, cell_dim=cell_dim, length=length, vertical=vertical
        )
    elif shape == ApertureOptions.SQUARE.value:
        print(f"Side length : {n_cells}")
        ap = create_square_aperture(
            slm_shape=slm_shape, cell_dim=cell_dim, side=n_cells * cell_dim[0]
        )
    elif shape == ApertureOptions.CIRC.value:
        print(f"Radius : {n_cells}")
        ap = create_circ_aperture(
            slm_shape=slm_shape, cell_dim=cell_dim, radius=n_cells * cell_dim[0]
        )
    elif shape == ApertureOptions.RECT.value:
        if len(rect_shape) == 0:
            # not provided
            rect_shape = (n_cells, n_cells)
        print(f"Shape : {rect_shape}")
        apert_dim = rect_shape[0] * cell_dim[0], rect_shape[1] * cell_dim[1]
        ap = create_rect_aperture(slm_shape=slm_shape, cell_dim=cell_dim, apert_dim=apert_dim)
    assert ap is not None

    # set aperture to device
    D = create_display(device_key=device)
    D.imshow(ap.values)


if __name__ == "__main__":
    set_aperture()
