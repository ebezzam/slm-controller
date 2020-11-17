import click
from slm_controller import display
from slm_controller.aperture import (
    LineAperture,
    SquareAperture,
    CircAperture,
    RectAperture,
    ApertureOptions,
)
from slm_controller.hardware import devices, DeviceOptions, DeviceParam
from slm_controller.slm import SLM


@click.command()
@click.option(
    "--shape", default=ApertureOptions.SQUARE.value, type=click.Choice(ApertureOptions.values())
)
@click.option("--n_cels", default=10, type=int)
@click.option("--rect_shape", default=None, nargs=2, type=int)
@click.option("--vertical", is_flag=True)
def set_rgb_aperture(shape, n_cells, rect_shape, vertical):
    """
    Set aperture for the 1.8'' RGB display by Adafruit.

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
    """

    # check input parameters
    if len(rect_shape) > 0 and shape is not ApertureOptions.RECT.value:
        raise ValueError("Received [rect_shape], but [shape] parameters is not 'rect'.")
    if vertical and shape is not ApertureOptions.LINE.value:
        raise ValueError("Received [vertical] flag, but [shape] parameters is not 'line'.")

    # prepare display
    rgb_device = DeviceOptions.ADAFRUIT_RGB
    D = display.RGBDisplay(rotation=0)

    # print device info
    cell_shape = devices[rgb_device][DeviceParam.CELL_SHAPE]
    print(f"SLM dimension : {D.shape}")
    print(f"Cell shape (m) : {cell_shape}")
    if shape == ApertureOptions.LINE.value:
        if vertical:
            print("Aperture shape : vertical line")
        else:
            print("Aperture shape : horizontal line")
    else:
        print(f"Aperture shape : {shape}")

    # create slm
    slm = SLM(shape=D.shape, cell_dim=cell_shape)

    # create aperture mask
    ap = None
    if shape == ApertureOptions.LINE.value:
        print(f"Length : {n_cells}")
        length = n_cells * cell_shape[0] if vertical else n_cells * cell_shape[1]
        ap = LineAperture(length=length, slm=slm, vertical=vertical)
    elif shape == ApertureOptions.SQUARE.value:
        print(f"Side length : {n_cells}")
        ap = SquareAperture(side=n_cells * cell_shape[0], slm=slm)
    elif shape == ApertureOptions.CIRC.value:
        print(f"Radius : {n_cells}")
        ap = CircAperture(radius=n_cells * cell_shape[0], slm=slm)
    elif shape == ApertureOptions.RECT.value:
        if len(rect_shape) == 0:
            # not provided
            rect_shape = (n_cells, n_cells)
        print(f"Shape : {rect_shape}")
        ap = RectAperture(
            apert_dim=(rect_shape[0] * cell_shape[0], rect_shape[1] * cell_shape[1]), slm=slm
        )
    assert ap is not None

    # set aperture
    D.imshow(ap.mask)


if __name__ == "__main__":
    set_rgb_aperture()
