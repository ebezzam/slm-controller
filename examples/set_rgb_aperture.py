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
@click.option("--vertical", is_flag=True)
def set_rgb_aperture(shape, n_pixels, rect_shape, vertical):

    # check input parameters
    if len(rect_shape) > 0 and shape is not ApertureOptions.RECT.value:
        raise ValueError("Received [rect_shape], but [shape] parameters is not 'rect'.")
    if vertical and shape is not ApertureOptions.LINE.value:
        raise ValueError("Received [vertical] flag, but [shape] parameters is not 'line'.")

    # prepare display
    D = display.RGBDisplay()

    # print device info
    pixel_shape = devices[DeviceOptions.ADAFRUIT_RGB][DeviceParam.PIXEL_SHAPE]
    print(f"SLM dimension : {D.shape}")
    print(f"Pixel shape (m) : {pixel_shape}")
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
        print(f"Length : {n_pixels}")
        ap = LineAperture(
            n_pixels=n_pixels, slm_dim=D.shape, pixel_shape=pixel_shape, vertical=vertical
        )
    elif shape == ApertureOptions.SQUARE.value:
        print(f"Side length : {n_pixels}")
        ap = SquareAperture(side=n_pixels, slm_dim=D.shape, pixel_shape=pixel_shape)
    elif shape == ApertureOptions.CIRC.value:
        print(f"Radius : {n_pixels}")
        ap = CircAperture(radius=n_pixels, slm_dim=D.shape, pixel_shape=pixel_shape)
    elif shape == ApertureOptions.RECT.value:
        if len(rect_shape) == 0:
            # not provided
            rect_shape = (n_pixels, n_pixels)
        print(f"Shape : {rect_shape}")
        ap = RectAperture(apert_dim=rect_shape, slm_dim=D.shape, pixel_shape=pixel_shape)
    assert ap is not None

    # set aperture
    D.imshow(ap.mask)


if __name__ == "__main__":
    set_rgb_aperture()
