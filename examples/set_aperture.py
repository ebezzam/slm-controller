"""
Set aperture example.
"""

import click
from slm_controller.display import create_display
from slm_controller.aperture import (
    rect_aperture,
    line_aperture,
    square_aperture,
    circ_aperture,
    ApertureOptions,
)
from slm_controller.hardware import slm_display_devices, SlmDisplayDevices, SlmParam


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
    "--center", default=None, nargs=2, type=int, help="Coordinate for center.",
)
@click.option(
    "--vertical",
    is_flag=True,
    help="Whether line should be vertical (True) or horizontal (False).",
)
@click.option(
    "--device",
    type=click.Choice(SlmDisplayDevices.values()),
    help="Which device to program with aperture.",
)
def set_aperture(shape, n_cells, rect_shape, center, vertical, device):
    """
    Set aperture on a physical device.
    """

    # TODO handle device == null

    if rect_shape is None:
        rect_shape = []
    if center is None:
        center = []

    # check input parameters
    if len(rect_shape) > 0 and shape is not ApertureOptions.RECT.value:
        raise ValueError("Received [rect_shape], but [shape] parameters is not 'rect'.")
    if vertical and shape is not ApertureOptions.LINE.value:
        raise ValueError("Received [vertical] flag, but [shape] parameters is not 'line'.")

    # print device info
    device_config = slm_display_devices[device]
    cell_dim = device_config[SlmParam.CELL_DIM]
    print(f"SLM dimension : {device_config[SlmParam.SLM_SHAPE]}")
    print(f"Cell dim (m) : {cell_dim}")
    if shape == ApertureOptions.LINE.value:
        if vertical:
            print("Aperture shape : vertical line")
        else:
            print("Aperture shape : horizontal line")
    else:
        print(f"Aperture shape : {shape}")
    if len(center) > 0:
        center = (center[0] * cell_dim[0], center[1] * cell_dim[1])
    else:
        center = None

    # create aperture mask
    ap = None
    if shape == ApertureOptions.LINE.value:
        print(f"Length : {n_cells}")
        length = n_cells * cell_dim[0] if vertical else n_cells * cell_dim[1]
        ap = line_aperture(
            length=length,
            vertical=vertical,
            slm_shape=device_config[SlmParam.SLM_SHAPE],
            cell_dim=device_config[SlmParam.CELL_DIM],
            center=center,
        )
    elif shape == ApertureOptions.SQUARE.value:
        print(f"Side length : {n_cells}")
        ap = square_aperture(
            side=n_cells * cell_dim[0],
            slm_shape=device_config[SlmParam.SLM_SHAPE],
            cell_dim=device_config[SlmParam.CELL_DIM],
            center=center,
        )
    elif shape == ApertureOptions.CIRC.value:
        print(f"Radius : {n_cells}")
        ap = circ_aperture(
            radius=n_cells * cell_dim[0],
            slm_shape=device_config[SlmParam.SLM_SHAPE],
            cell_dim=device_config[SlmParam.CELL_DIM],
            center=center,
        )
    elif shape == ApertureOptions.RECT.value:
        if len(rect_shape) == 0:
            # not provided
            rect_shape = (n_cells, n_cells)
        print(f"Shape : {rect_shape}")
        apert_dim = rect_shape[0] * cell_dim[0], rect_shape[1] * cell_dim[1]
        ap = rect_aperture(
            apert_dim=apert_dim,
            slm_shape=device_config[SlmParam.SLM_SHAPE],
            cell_dim=device_config[SlmParam.CELL_DIM],
            center=center,
        )
    assert ap is not None

    # set aperture to device
    D = create_display(device_key=device)
    if device_config[SlmParam.MONOCHROME]:
        D.imshow(ap.grayscale_values)
    else:
        D.imshow(ap.values)


if __name__ == "__main__":
    set_aperture()
