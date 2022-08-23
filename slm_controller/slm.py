import abc
import numpy as np
import warnings
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

from slm_controller.hardware import SLMDevices, SLMParam, slm_devices

try:
    import slm_controller.holoeye.detect_heds_module_path
    from holoeye import slmdisplaysdk
except ImportError:
    warnings.warn(
        "Failed to import Holoeye SLM SDK."
    )  # TODO triggers when this file is run separately, test


class SLM:
    def __init__(self):
        self._slm = None

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
            (N_height, N_width) SLM dimensions [pixels]
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


class AdafruitSLM(SLM):
    def __init__(
        self,
        cs_pin=None,
        dc_pin=None,
        reset_pin=None,
        rotation=90,
        baudrate=24000000,
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

        self._height, self._width = slm_devices[SLMDevices.ADAFRUIT.value][SLMParam.SLM_SHAPE]

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
            self._slm = st7735.ST7735R(
                spi,
                rotation=rotation,
                cs=cs_pin,
                dc=dc_pin,
                rst=reset_pin,
                baudrate=baudrate,
            )

            if self._slm.rotation % 180 == 90:
                self._width = self._slm.height
                self._height = self._slm.width
            else:
                self._width = self._slm.width
                self._height = self._slm.height
        except Exception:
            self._slm = None
            warnings.warn("Failed to load SLM. Using virtual device...")

    def clear(self):
        """
        Clear SLM.
        """
        if self._slm:
            I = Image.new("RGB", (self.width, self.height))

            # Get drawing object to draw on image.
            draw = ImageDraw.Draw(I)

            # Draw a black filled box to clear the image.
            draw.rectangle((0, 0, self.width, self.height), outline=0, fill=(0, 0, 0))
            self._slm.image(I)

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
        assert isinstance(
            I, np.ndarray
        ) and (  # TODO adapt assert to preprocessing being done by caller
            np.issubdtype(I.dtype, np.integer) or np.issubdtype(I.dtype, np.floating)
        )
        assert np.all(I >= 0)
        assert I.ndim in (2, 3)
        assert I.shape[-2:] == self.shape

        if self._slm:
            self.clear()

            try:
                # --------------------------------------------------------------
                # TODO remove preprocessing, should be done by caller
                I_max = I.max()
                I_max = 1 if np.isclose(I_max, 0) else I_max

                I_f = np.broadcast_to(I, (3, *I.shape[-2:])) / I_max  # float64
                I_u = np.uint8(255 * I_f)  # uint8
                # --------------------------------------------------------------

                I_p = Image.fromarray(I_u.transpose(1, 2, 0), mode="RGB")
                self._slm.image(I_p)
            except Exception as e:
                raise ValueError("Parameter[I]: unsupported data") from e

        else:
            _, ax = plt.subplots()
            if len(I.shape) == 3:
                # if RGB, put channel dim in right place
                I = I.transpose(1, 2, 0)
                ax.imshow(I)
            else:
                ax.imshow(I, cmap="gray")
            plt.show()


class NokiaSLM(SLM):
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

        self._height, self._width = slm_devices[SLMDevices.NOKIA_5110.value][SLMParam.SLM_SHAPE]

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
            self._slm = adafruit_pcd8544.PCD8544(
                spi=spi,
                dc_pin=dc_pin,
                cs_pin=cs_pin,
                reset_pin=reset_pin,
                contrast=contrast,
                bias=bias,
                baudrate=baudrate,
            )

        except Exception:
            self._slm = None
            warnings.warn("Failed to load SLM. Using virtual device...")

    def clear(self):
        """
        Clear SLM.
        """
        if self._slm:
            self._slm.fill(1)
            self._slm.show()

    def imshow(self, I):
        """
        Display monochrome data in binary format.

        Parameters
        ----------
        I : :py:class:`~numpy.ndarray`
            (N_height, N_width) monochrome data.
        """
        assert I.shape == self.shape  # TODO adapt assert to preprocessing being done by caller
        assert isinstance(I, np.ndarray) and (
            np.issubdtype(I.dtype, np.integer) or np.issubdtype(I.dtype, np.floating)
        )
        assert np.all(I >= 0)

        if self._slm:
            self.clear()

            try:
                # --------------------------------------------------------------
                # TODO remove preprocessing, should be done by caller
                I_max = I.max()
                I_max = 1 if np.isclose(I_max, 0) else I_max
                I_u = 255 - np.uint8(I / float(I_max) * 255)  # uint8, full range, image is inverted
                # --------------------------------------------------------------
                I_p = Image.fromarray(I_u.T).convert("1")
                self._slm.image(I_p)
                self._slm.show()

            except Exception as e:
                raise ValueError("Parameter[I]: unsupported data") from e

        else:
            _, ax = plt.subplots()
            ax.imshow(I, cmap="gray")
            plt.show()


class HoloeyeSLM(SLM):
    def __init__(self):
        """
        Initialize a new holoeye SLM instance
        """
        super().__init__()

        # Initialize parameters of the holoeye SLM display
        self._height, self._width = slm_devices[SLMDevices.HOLOEYE_LC_2012.value][
            SLMParam.SLM_SHAPE
        ]

        self._show_time = None

        try:
            # Similar to: https://github.com/computational-imaging/neural-holography/blob/d2e399014aa80844edffd98bca34d2df80a69c84/utils/slm_display_module.py#L19
            # TODO check those flags
            self._show_flags = slmdisplaysdk.ShowFlags.PresentAutomatic
            self._show_flags |= slmdisplaysdk.ShowFlags.PresentFitWithBars

            try:
                # Initializes the SLM library
                self._slm = slmdisplaysdk.SLMInstance()
            except RuntimeError as ex:
                # The library initialization failed so a virtual device is used instead
                self._slm = None
                warnings.warn(f"Failed to load SLM: {ex}. Using virtual device...")
        except Exception:
            self._slm = None
            warnings.warn("Failed to load SLM. Using virtual device...")

        # Check that the holoeye sdk is up to date
        if self._slm and not self._slm.requiresVersion(3):
            self._slm = None
            warnings.warn(
                "Failed to load SLM because the LC 2012 requires version 3 of its SDK. Using virtual device..."
            )

        if self._slm:
            # Detect SLMs and open a window on the selected SLM
            error = self._slm.open()  # TODO check if can set max wait time when no SLM is found

            # Check if the opening the window was successful
            if error != slmdisplaysdk.ErrorCode.NoError:
                # Otherwise use again a virtual device
                warnings.warn(
                    f"Failed to load SLM: {self._slm.errorString(error)}. Using virtual device..."
                )
                self._slm = None

    def __del__(self):
        """
        Destructor
        """
        if self._slm:
            del self._slm

    def set_show_time(self, time=None):
        """
        Set the time a mask is shown.

        Parameters
        ----------
        show_time : float, optional
            Specifies the amount of time in seconds that the phase mask is shown
            on the SLM, by default None which means that the mask is shown until
            the user kills the script.
        """
        self._show_time = time

    def clear(self):
        """
        Clear SLM aka show black screen.
        """
        if self._slm:
            # Configure the blank screen value
            black = 0

            # Show phase map on SLM
            error = self._slm.showBlankscreen(black)

            # And check that no error occurred
            assert error == slmdisplaysdk.ErrorCode.NoError, self._slm.errorString(error)

    # TODO yeah a flag to allow preview would be nice. And either printing in the
    # command line and/or placing in the title of the figure if the pattern has been
    # programmed on the SLM (or if there was an issue connecting)
    def imshow(self, I):
        """
        Display monochrome data.

        Parameters
        ----------
        I : np.ndarray
            The phase map to show on the SLM.
        """
        # Check that the phase map is valid
        assert isinstance(I, np.ndarray) and np.issubdtype(I.dtype, np.uint8)
        assert I.shape == self.shape

        # If using a physical device
        if self._slm:
            # Reset devices mask
            self.clear()

            # Show phase map on SLM
            # TODO test self._slm.showPhasevalues(I_u)
            error = self._slm.showData(I, self._show_flags)

            # And check that no error occurred
            assert error == slmdisplaysdk.ErrorCode.NoError, self._slm.errorString(error)

            if self._show_time is None:
                # Wait until the SLM process is closed:
                print(
                    "Waiting for SDK process to close. Please close the tray icon to continue ..."
                )
                error = self._slm.utilsWaitUntilClosed()
                assert error == slmdisplaysdk.ErrorCode.NoError, self._slm.errorString(error)
            else:
                # sleep for specified time
                # import time
                # time.sleep(self._show_time)  # TODO check this native version
                # of wait

                error = self._slm.utilsWaitForCheckedS(self._show_time)
                assert error == slmdisplaysdk.ErrorCode.NoError, self._slm.errorString(error)
        else:
            # Use a virtual device, plot
            fig, ax = plt.subplots()

            if self._show_time is not None:

                def on_timeout():
                    plt.close()

                timer = fig.canvas.new_timer(interval=self._show_time * 1000)
                timer.add_callback(on_timeout)

                ax.imshow(I, cmap="gray")
                timer.start()
                plt.show()

            else:
                ax.imshow(I, cmap="gray")
                plt.show()


def create(device_key):
    """
    Factory method to create `SLM` object.

    Parameters
    ----------
    device_key : str
        Option from `SlmDevices`.
    """
    assert device_key in SLMDevices.values()

    slm_device = None
    if device_key == SLMDevices.ADAFRUIT.value:
        slm_device = AdafruitSLM()
    elif device_key == SLMDevices.NOKIA_5110.value:
        slm_device = NokiaSLM()
    elif device_key == SLMDevices.HOLOEYE_LC_2012.value:
        slm_device = HoloeyeSLM()
    assert slm_device is not None
    return slm_device
