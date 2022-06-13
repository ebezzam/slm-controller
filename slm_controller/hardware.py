from enum import Enum

# Slm display devices that are implemented in this project
class SLMDevices(Enum):
    ADAFRUIT_RGB = "rgb"
    ADAFRUIT_BINARY = "binary"
    NOKIA_5110 = "nokia"
    HOLOEYE_LC_2012 = "holoeye"

    @staticmethod
    def values():
        return [device.value for device in SLMDevices]


# Parameters of those display slms
class SLMParam:
    CELL_DIM = "cell_dim"
    SLM_SHAPE = "slm_shape"
    MONOCHROME = "monochrome"
    FILL_FACTOR = "fill_factor"
    FRAME_RATE = "frame_rate"


# Actual values of those parameters for all the slms
slm_devices = {
    # 1.8 inch RGB display by Adafruit: https://learn.adafruit.com/1-8-tft-display/overview
    # datasheet: https://cdn-shop.adafruit.com/datasheets/JD-T1800.pdf
    SLMDevices.ADAFRUIT_RGB.value: {
        SLMParam.CELL_DIM: (0.18e-3, 0.18e-3),
        SLMParam.SLM_SHAPE: (128, 160),
        SLMParam.MONOCHROME: False,
    },
    # 1.3 inch monochrome display by Adafruit:
    # https://learn.adafruit.com/adafruit-sharp-memory-display-breakout
    # datasheet: https://cdn-shop.adafruit.com/product-files/3502/Data+sheet.pdf
    SLMDevices.ADAFRUIT_BINARY.value: {
        SLMParam.CELL_DIM: (0.145e-3, 0.145e-3),
        SLMParam.SLM_SHAPE: (144, 168),
        SLMParam.MONOCHROME: True,
    },
    # Graphic LCD 84x48 - Nokia 5110
    # https://www.sparkfun.com/products/10168
    # 1.5 inch diagonal: https://learn.adafruit.com/nokia-5110-3310-monochrome-lcd
    # datasheet: https://www.sparkfun.com/datasheets/LCD/Monochrome/Nokia5110.pdf
    SLMDevices.NOKIA_5110.value: {
        SLMParam.CELL_DIM: (
            0.339e-3,
            0.396e-3,
        ),  # TODO: measured by "hand", check elsewhere
        SLMParam.SLM_SHAPE: (84, 48),
        SLMParam.MONOCHROME: True,
    },
    # Holoeye SLM - LC 2012
    # https://holoeye.com/lc-2012-spatial-light-modulator/
    # 1.8 inch diagonal, 36.9 x 27.6 mm
    # datasheet: same link
    SLMDevices.HOLOEYE_LC_2012.value: {
        SLMParam.CELL_DIM: (
            0.36e-4,
            0.36e-4,
        ),  # Computed: 0.359375e-4, 0.3603515625e-4
        SLMParam.SLM_SHAPE: (768, 1024),
        SLMParam.MONOCHROME: True,
        SLMParam.FILL_FACTOR: 0.58,
        SLMParam.FRAME_RATE: 60,
    },
}

