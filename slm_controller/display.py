import abc
import numpy as np
import warnings
from PIL import Image, ImageDraw
import time

from slm_controller.hardware import SlmDevices, SlmParam, slm_devices
import slm_controller.holoeye.detect_heds_module_path  # TODO add in setup
from holoeye import slmdisplaysdk


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
        self, cs_pin=None, dc_pin=None, reset_pin=None, rotation=90, baudrate=24000000,
    ):
        """
        Object to display images on the Adafruit 1.8 inch TFT Display Breakout with a Raspberry Pi:
        https://learn.adafruit.com/1-8-tft-display/overview

        Parameters
        ----------
        cs_pin : :py:class:`~adafruit_blinka.microcontroller.generic_linux.periphery_pin.Pin`
            Raspberry Pi pin connected to TFT_CS pin on the display breakout.
        dc_pin : :py:class:`~adafruit_blinka.microcontroller.generic_linux.periphery_pin.Pin`
            Raspberry Pi pin connected to D/C pin on the display breakout.
        reset_pin : :py:class:`~adafruit_blinka.microcontroller.generic_linux.periphery_pin.Pin`
            Raspberry Pi pin connected to RESET pin on the display breakout.
        rotation : 0, 90, 180, or 270
            Rotation of image on the display.
        baudrate : int
            Baud rate.
        """
        super().__init__()

        if rotation not in (0, 90, 180, 270):
            raise ValueError("Rotation must be 0/90/180/270")
        self._virtual = False

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
            self._virtual = True
            self._height, self._width = slm_devices[SlmDevices.ADAFRUIT_RGB.value][
                SlmParam.SLM_SHAPE
            ]

            warnings.warn("Failed to load display. Using virtual device...")

    def clear(self):
        """
        Clear display.
        """
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

        if not self._virtual:

            self.clear()

            try:
                I_max = I.max()
                I_max = 1 if np.isclose(I_max, 0) else I_max

                I_f = np.broadcast_to(I, (3, *I.shape[-2:])) / I_max  # float64
                I_u = np.uint8(255 * I_f)  # uint8

                I_p = Image.fromarray(I_u.transpose(1, 2, 0), mode="RGB")
                self._disp.image(I_p)
            except:
                raise ValueError("Parameter[I]: unsupported data")

        else:

            import matplotlib.pyplot as plt

            fig, ax = plt.subplots()
            if len(I.shape) == 3:
                # if RGB, put channel dim in right place
                I = I.transpose(1, 2, 0)
                ax.imshow(I)
            else:
                ax.imshow(I, cmap="gray")
            plt.show()


class BinaryDisplay(Display):
    def __init__(self, cs_pin=None, baudrate=2000000):
        """
        Object to display images on the Adafruit 1.3 inch monochrome display with a Raspberry Pi:
        https://learn.adafruit.com/adafruit-sharp-memory-display-breakout

        Parameters
        ----------
        cs_pin : :py:class:`~adafruit_blinka.microcontroller.generic_linux.periphery_pin.Pin`
            Raspberry Pi pin connected to TFT_CS pin on the display breakout.
        baudrate : int
            Baud rate.
        """
        super().__init__()

        try:

            import board
            import busio
            import digitalio
            import adafruit_sharpmemorydisplay

            cs_pin = cs_pin if (cs_pin is not None) else board.D6

            self._height, self._width = slm_devices[SlmDevices.ADAFRUIT_BINARY.value][
                SlmParam.SLM_SHAPE
            ]

            spi = busio.SPI(board.SCK, MOSI=board.MOSI)
            scs = digitalio.DigitalInOut(cs_pin)  # inverted chip select
            self._disp = adafruit_sharpmemorydisplay.SharpMemoryDisplay(
                spi, scs, self._height, self._width, baudrate=baudrate
            )

        except:
            raise IOError("Failed to load display.")

    def clear(self):
        """
        Clear display.
        """
        self._disp.fill(1)
        self._disp.show()

    def imshow(self, I):
        """
        Display monochrome data in binary format.

        Parameters
        ----------
        I : :py:class:`~numpy.ndarray`
            (N_height, N_width) monochrome data.
        """
        assert I.shape == self.shape
        assert isinstance(I, np.ndarray) and (
            np.issubdtype(I.dtype, np.integer) or np.issubdtype(I.dtype, np.floating)
        )
        assert np.all(I >= 0)

        self.clear()

        try:

            I_max = I.max()
            I_max = 1 if np.isclose(I_max, 0) else I_max
            I_u = np.uint8(I / float(I_max) * 255)  # uint8, full range
            I_p = Image.fromarray(I_u.T).convert("1")
            self._disp.image(I_p)
            self._disp.show()

        except:
            raise ValueError("Parameter[I]: unsupported data")


class NokiaDisplay(Display):
    def __init__(
        self,
        dc_pin=None,
        cs_pin=None,
        reset_pin=None,
        contrast=80,
        bias=4,
        baudrate=1000000,
    ):
        """
        Object to display images on the Nokia 5110 monochrome display with a Raspberry Pi:
        https://learn.adafruit.com/nokia-5110-3310-monochrome-lcd

        Parameters
        ----------
        dc_pin : :py:class:`~adafruit_blinka.microcontroller.generic_linux.periphery_pin.Pin`
            Raspberry Pi pin connected to the DC pin on the display breakout.
        cs_pin : :py:class:`~adafruit_blinka.microcontroller.generic_linux.periphery_pin.Pin`
            Raspberry Pi pin connected to the CE pin on the display breakout.
        reset_pin : :py:class:`~adafruit_blinka.microcontroller.generic_linux.periphery_pin.Pin`
            Raspberry Pi pin connected to the RST pin on the display breakout.
        contrast : int
            Display contrast, should be 0-127.
        bias : int
            Display bias.
        baudrate : int
            Baud rate.
        """
        super().__init__()

        try:

            import board
            import busio
            import digitalio
            import adafruit_pcd8544

            dc_pin = dc_pin if dc_pin is not None else board.D6
            cs_pin = cs_pin if cs_pin is not None else board.CE0
            reset_pin = reset_pin if reset_pin is not None else board.D5

            spi = busio.SPI(board.SCK, MOSI=board.MOSI)
            dc_pin = digitalio.DigitalInOut(dc_pin)  # data/command
            cs_pin = digitalio.DigitalInOut(cs_pin)  # Chip select
            reset_pin = digitalio.DigitalInOut(reset_pin)  # reset
            self._disp = adafruit_pcd8544.PCD8544(
                spi=spi,
                dc_pin=dc_pin,
                cs_pin=cs_pin,
                reset_pin=reset_pin,
                contrast=contrast,
                bias=bias,
                baudrate=baudrate,
            )

            self._height, self._width = slm_devices[SlmDevices.NOKIA_5110.value][
                SlmParam.SLM_SHAPE
            ]

        except:
            raise IOError("Failed to load display.")

    def clear(self):
        """
        Clear display.
        """
        self._disp.fill(1)
        self._disp.show()

    def imshow(self, I):
        """
        Display monochrome data in binary format.

        Parameters
        ----------
        I : :py:class:`~numpy.ndarray`
            (N_height, N_width) monochrome data.
        """
        assert I.shape == self.shape
        assert isinstance(I, np.ndarray) and (
            np.issubdtype(I.dtype, np.integer) or np.issubdtype(I.dtype, np.floating)
        )
        assert np.all(I >= 0)

        self.clear()

        try:

            I_max = I.max()
            I_max = 1 if np.isclose(I_max, 0) else I_max
            I_u = 255 - np.uint8(
                I / float(I_max) * 255
            )  # uint8, full range, image is inverted
            I_p = Image.fromarray(I_u.T).convert("1")
            self._disp.image(I_p)
            self._disp.show()

        except:
            raise ValueError("Parameter[I]: unsupported data")


class HoloeyeDisplay(Display):
    def __init__(self, show_time=2):
        """
        Initialize a new holoeye slm instance

        Parameters
        ----------
        show_time : int, optional
            Specifies the amount of time the phase pattern is shown on the slm, by default 2
        """
        super().__init__()

        # Similar to: https://github.com/computational-imaging/neural-holography/blob/d2e399014aa80844edffd98bca34d2df80a69c84/utils/slm_display_module.py#L19
        # TODO check those flags
        self._show_flags = slmdisplaysdk.ShowFlags.PresentAutomatic
        self._show_flags |= slmdisplaysdk.ShowFlags.PresentFitWithBars

        # Initialize parameters of the holoeye slm display
        self._virtual = False
        self._height, self._width = slm_devices[SlmDevices.HOLOEYE_LC_2012.value][
            SlmParam.SLM_SHAPE
        ]

        self._show_time = show_time

        try:
            # Initializes the SLM library
            self._disp = slmdisplaysdk.SLMInstance()
        except RuntimeError as ex:
            # The library initialization failed so a virtual device is used instead
            self._virtual = True
            warnings.warn(f"{ex} Using virtual device...")

        # Check that the holoeye sdk is up to date
        if not self._virtual and not self._disp.requiresVersion(3):
            self._virtual = True
            warnings.warn(
                "Failed to load display because the LC 2012 requires version 3 of its SDK. Using virtual device..."
            )

        # Detect slms and open a window on the selected slm
        error = (
            self._disp.open()
        )  # TODO check if can set max wait time when no SLM is found

        # Check if the opening the window was successful
        if error != slmdisplaysdk.ErrorCode.NoError:
            # Otherwise use again a virtual device
            self._virtual = True
            warnings.warn(
                f"Failed to load display: {self._disp.errorString(error)}. Using virtual device..."
            )

    def __del__(self):
        """
        Destructor
        """
        self._disp.__del__()

    def clear(self):
        """
        Clear display aka show black screen.
        """

        # Configure the blank screen value
        black = 0

        # Show phase map on slm
        error = self._disp.showBlankscreen(black)

        # And check that no error occurred
        assert error == slmdisplaysdk.ErrorCode.NoError, self._disp.errorString(error)

    def imshow(self, I):
        """
        Display monochrome data.

        Parameters
        ----------
        I : np.ndarray
            The phase map to shw on the slm
        """
        # Check that the phase map is valid
        assert isinstance(I, np.ndarray) and (
            np.issubdtype(I.dtype, np.integer) or np.issubdtype(I.dtype, np.floating)
        )
        assert np.all(I >= 0)
        assert I.ndim in (2, 3)
        assert I.shape[-2:] == self.shape

        # If using a physical device
        if not self._virtual:
            # Reset devices phase pattern
            self.clear()

            # Normalize entries of the phase map
            I_max = I.max()
            I_max = 1 if np.isclose(I_max, 0) else I_max
            I_f = I / I_max  # float64

            # Quantize those floats into a bit values
            I_u = np.uint8(255 * I_f)  # uint8

            # Show phase map on slm
            error = self._disp.showData(I_u, self._show_flags)

            # And check that no error occurred
            assert error == slmdisplaysdk.ErrorCode.NoError, self._disp.errorString(
                error
            )

            # sleep for specified time
            time.sleep(self._show_time)
        else:
            # Use a virual device
            import matplotlib.pyplot as plt

            # plot
            _, ax = plt.subplots()
            ax.imshow(I)
            plt.show()


def create_display(slm_device_key):
    """
    Factory method to create `Display` object.

    Parameters
    ----------
    device_key : str
        Option from `SlmDevices`.
    """
    assert slm_device_key in SlmDevices.values()

    slm_display = None
    if slm_device_key == SlmDevices.ADAFRUIT_RGB.value:
        slm_display = RGBDisplay()
    elif slm_device_key == SlmDevices.ADAFRUIT_BINARY.value:
        slm_display = BinaryDisplay()
    elif slm_device_key == SlmDevices.NOKIA_5110.value:
        slm_display = NokiaDisplay()
    elif slm_device_key == SlmDevices.HOLOEYE_LC_2012.value:
        slm_display = HoloeyeDisplay()
    assert slm_display is not None
    return slm_display
