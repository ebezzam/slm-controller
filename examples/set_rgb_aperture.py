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


@click.command()
@click.option(
    "--shape", default=ApertureOptions.SQUARE.value, type=click.Choice(ApertureOptions.values())
)
@click.option("--n_pixels", default=10, type=int)
@click.option("--rect_shape", default=None, nargs=2, type=int)
@click.option("--horizontal", is_flag=True)
def set_rgb_aperture(shape, n_pixels, rect_shape, horizontal):

    # check input parameters
    if len(rect_shape) > 0 and shape is not ApertureOptions.RECT.value:
        raise ValueError("Received [rect_shape], but [shape] parameters is not 'rect'.")
    if horizontal and shape is not ApertureOptions.LINE.value:
        raise ValueError("Received [horizontal] flag, but [shape] parameters is not 'line'.")

    # prepare display
    pixel_shape = devices[DeviceOptions.ADAFRUIT_RGB][DeviceParam.PIXEL_SHAPE]
    print(f"Pixel shape (m) : {pixel_shape}")
    D = display.RGBDisplay()

    # print device info
    print(f"SLM dimension : {D.shape}")

    # create aperture mask
    ap = None
    if shape == ApertureOptions.LINE.value:
        ap = LineAperture(
            n_pixels=n_pixels, slm_dim=D.shape, pixel_shape=pixel_shape, vertical=False
        )
    elif shape == ApertureOptions.SQUARE.value:
        ap = SquareAperture(side=n_pixels, slm_dim=D.shape, pixel_shape=pixel_shape)
    elif shape == ApertureOptions.CIRC.value:
        ap = CircAperture(radius=n_pixels, slm_dim=D.shape, pixel_shape=pixel_shape)
    elif shape == ApertureOptions.RECT.value:
        ap = RectAperture(apert_dim=rect_shape, slm_dim=D.shape, pixel_shape=pixel_shape)
    assert ap is not None

    # set aperture
    D.imshow(ap.mask)


if __name__ == "__main__":
    set_rgb_aperture()
