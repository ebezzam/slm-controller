import click
from slm_controller import display, hardware
from slm_controller.aperture import LineAperture, SquareAperture, CircAperture


aperture_options = ["square", "circ", "line"]


@click.command()
@click.option("--shape", default="rect", type=click.Choice(aperture_options))
@click.option("--n_pixels", default=10, type=int)
def set_rgb_aperture(shape, n_pixels):

    pixel_shape = hardware["adafruit_1p8_tft_rgb"]["pixel_shape"]

    # instantiate display object
    D = display.RGBDisplay()
    print(f"SLM dimension : {D.shape}")

    # create aperture mask
    ap = None
    if shape == "line":
        ap = LineAperture(
            n_pixels=n_pixels, slm_dim=D.shape, pixel_shape=pixel_shape, vertical=False
        )
    elif shape == "square":
        ap = SquareAperture(side=n_pixels, slm_dim=D.shape, pixel_shape=pixel_shape)
    elif shape == "circ":
        ap = CircAperture(radius=n_pixels, slm_dim=D.shape, pixel_shape=pixel_shape)
    assert ap is not None

    # set aperture
    D.imshow(ap.mask)


if __name__ == "__main__":
    set_rgb_aperture()
