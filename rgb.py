from PIL import Image, ImageDraw
import warnings
import numpy as np
import digitalio
import adafruit_rgb_display.st7735 as st7735

try:
    import board

    board_available = True
except:
    board_available = False


class RGBDisplay(object):
    def __init__(
        self,
        cs_pin=None,
        dc_pin=None,
        reset_pin=None,
        rotation=90,
        baudrate=24000000,
    ):

        if board_available:
            cs_pin = cs_pin if cs_pin is not None else board.CE0
            dc_pin = dc_pin if dc_pin is not None else board.D25
            reset_pin = reset_pin if reset_pin is not None else board.D24

            # Configuration for CS and DC pins (these are PiTFT defaults)
            cs_pin = digitalio.DigitalInOut(cs_pin)
            dc_pin = digitalio.DigitalInOut(dc_pin)
            reset_pin = digitalio.DigitalInOut(reset_pin)

            # Setup SPI bus using hardware SPI:
            spi = board.SPI()

            # create interface with board
            self._disp = st7735.ST7735R(
                spi,
                rotation=rotation,
                cs=cs_pin,
                dc=dc_pin,
                rst=reset_pin,
                baudrate=baudrate,
            )

        else:
            warnings.warn("Failed to load display!")
            self._disp = None

    def get_width(self):
        if self._disp is not None:
            if self._disp.rotation % 180 == 90:
                return self._disp.height
            else:
                return self._disp.width
        else:
            return np.random.randint(100)

    def get_height(self):
        if self._disp is not None:
            if self._disp.rotation % 180 == 90:
                return self._disp.width
            else:
                return self._disp.height
        else:
            return np.random.randint(100)

    def clear_display(self):
        width = self.get_width()
        height = self.get_height()

        image = Image.new("RGB", (width, height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        self._disp.image(image)

    def display_pillow(self, image):
        """
        Parameters
        ----------
        image : PIL.Image.Image object
        """
        assert isinstance(image, Image.Image)
        if self._disp is not None:
            assert image.height == self.get_height()
            assert image.width == self.get_width()
            self.clear_display()
            self._disp.image(image)

    def display_image_file(self, image_path):
        """
        Load with Pillow and rescale.

        Parameters
        ----------
        image_path : str
        """
        image = Image.open(image_path)

        # rescale
        width = self.get_width()
        height = self.get_height()
        image_ratio = image.width / image.height
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width = width
            scaled_height = image.height * width // image.width
        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

        # crop and center
        x = scaled_width // 2 - width // 2
        y = scaled_height // 2 - height // 2
        image = image.crop((x, y, x + width, y + height))

        if self._disp is not None:
            self.clear_display()
            self._disp.image(image)

    def display_numpy(self, image):
        """
        Parameters
        ----------
        image : numpy array
            Height x width
        """
        assert isinstance(image, np.ndarray)
        if self._disp is not None:
            assert image.shape[0] == self.get_height()
            assert image.shape[1] == self.get_width()
            self.clear_display()
            PIL_image = Image.fromarray(np.uint8(image)).convert("RGB")
            self._disp.image(PIL_image)
