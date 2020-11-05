import abc

import numpy as np
from PIL import Image, ImageDraw


def load_image(fname):
    """
    Load an image.

    Parameters
    ----------
    fname : str, path-like
        Valid image file (i.e. JPG, PNG, BMP, TIFF, etc.)

    Returns
    -------
    I : :py:class:`~numpy.ndarray`
        ([N_channel,] N_height, N_width) image.
        Output dtype is format-dependent.
    """
    I_p = Image.open(fname, mode='r')
    I = np.asarray(I_p)  # (N_height, N_width [, N_channel])
    if I.ndim > 2:
        I = I.transpose(2, 0, 1)
    return I


def save_image(I, fname):
    """
    Save image to a file.

    Parameters
    ----------
    I : :py:class:`~numpy.ndarray`
        (N_channel, N_height, N_width) image.
    """
    I_max = I.max()
    I_max = 1 if np.isclose(I_max, 0) else I_max

    I_f = I / I_max  # float64
    I_u = np.uint8(255 * I_f)  # uint8

    if I.ndim == 3:
        I_u = I_u.transpose(1, 2, 0)

    I_p = Image.fromarray(I_u)
    I_p.save(fname)


class Display:
    def __init__(self):
        pass

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def shape(self):
        """
        Returns
        -------
        sh : tuple(int)
            (N_height, N_width) display dimensions [pixels]
        """
        return self._height, self._width

    @abc.abstractmethod
    def clear(self):
        """
        Show blank screen.
        """
        pass

    @abc.abstractmethod
    def imshow(self, I):
        """
        Display data as an image, i.e., on a 2D regular raster.

        Parameters
        ----------
        I : :py:class:`~numpy.ndarray`
            ([3,] N_height, N_width) non-negative reals.
            Interpretation of the optional 0-th dimension is class-dependent.
        """
        pass


class RGBDisplay(Display):
    def __init__(
        self,
        cs_pin=None,
        dc_pin=None,
        reset_pin=None,
        rotation=90,
        baudrate=24000000,
    ):
        super().__init__()

        try:
            import board
            import adafruit_rgb_display.st7735 as st7735
            import digitalio

            cs_pin = cs_pin if (cs_pin is not None) else board.CE0
            dc_pin = dc_pin if (dc_pin is not None) else board.D25
            reset_pin = reset_pin if (reset_pin is not None) else board.D24

            # Configuration for CS and DC pins (these are PiTFT defaults)
            cs_pin = digitalio.DigitalInOut(cs_pin)
            dc_pin = digitalio.DigitalInOut(dc_pin)
            reset_pin = digitalio.DigitalInOut(reset_pin)

            # Setup SPI bus using hardware SPI:
            spi = board.SPI()

            # Create interface with board
            self._disp = st7735.ST7735R(
                spi,
                rotation=rotation,
                cs=cs_pin,
                dc=dc_pin,
                rst=reset_pin,
                baudrate=baudrate,
            )

            if self._disp.rotation % 180 == 90:
                self._width = self._disp.height
                self._height = self._disp.width
            else:
                self._width = self._disp.width
                self._height = self._disp.height
        except:
            raise IOError("Failed to load display.")

    def clear(self):
        I = Image.new("RGB", (self.width, self.height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(I)

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, self.width, self.height), outline=0, fill=(0, 0, 0))
        self._disp.image(I)

    def imshow(self, I):
        """
        Display RGB or Grayscale data as an image.

        Parameters
        ----------
        I : :py:class:`~numpy.ndarray`
            ([3,] N_height, N_width) non-negative reals.

            2D inputs are interpreted as grayscale.
            3D inputs are interpreted as RGB.
        """
        assert isinstance(I, np.ndarray) and (
            np.issubdtype(I.dtype, np.integer) or np.issubdtype(I.dtype, np.floating)
        )
        assert np.all(I >= 0)
        assert I.ndim in (2, 3)
        assert I.shape[-2:] == self.shape

        self.clear()

        try:
            I_max = I.max()
            I_max = 1 if np.isclose(I_max, 0) else I_max

            I_f = np.broadcast_to(I, (3, *I.shape[-2:])) / I_max  # float64
            I_u = np.uint8(255 * I_f)  # uint8

            I_p = Image.fromarray(I_u.transpose(1, 2, 0), mode="RGB")
            self._disp.image(I_p)
        except:
            raise ValueError("Parameter[I]: unsupported shape")
