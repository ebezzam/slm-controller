import click
from slm_controller import display
from slm_controller.aperture import LineAperture, SquareAperture, CircAperture
from slm_controller.hardware import devices


aperture_options = ["square", "circ", "line"]


@click.command()
@click.option("--shape", default=aperture_options[0], type=click.Choice(aperture_options))
@click.option("--n_pixels", default=10, type=int)
def set_rgb_aperture(shape, n_pixels):

    pixel_shape = devices["adafruit_1p8_tft_rgb"]["pixel_shape"]

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
