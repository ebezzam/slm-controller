from enum import Enum


class DeviceOptions(Enum):
    ADAFRUIT_RGB = "rgb"
    ADAFRUIT_BINARY = "binary"
    NOKIA_5110 = "nokia"
    HOLOEYE_LC_2012 = "holoeye"

    @staticmethod
    def values():
        return [dev.value for dev in DeviceOptions]


class DeviceParam:
    CELL_DIM = "cell_dim"
    SLM_SHAPE = "slm_shape"
    MONOCHROME = "monochrome"
    # TODO Fill factor


devices = {
    # 1.8 inch RGB display by Adafruit: https://learn.adafruit.com/1-8-tft-display/overview
    # datasheet: https://cdn-shop.adafruit.com/datasheets/JD-T1800.pdf
    DeviceOptions.ADAFRUIT_RGB.value: {
        DeviceParam.CELL_DIM: (0.18e-3, 0.18e-3),
        DeviceParam.SLM_SHAPE: (128, 160),
        DeviceParam.MONOCHROME: False,
    },
    # 1.3 inch monochrome display by Adafruit:
    # https://learn.adafruit.com/adafruit-sharp-memory-display-breakout
    # datasheet: https://cdn-shop.adafruit.com/product-files/3502/Data+sheet.pdf
    DeviceOptions.ADAFRUIT_BINARY.value: {
        DeviceParam.CELL_DIM: (0.145e-3, 0.145e-3),
        DeviceParam.SLM_SHAPE: (144, 168),
        DeviceParam.MONOCHROME: True,
    },
    # Graphic LCD 84x48 - Nokia 5110
    # https://www.sparkfun.com/products/10168
    # 1.5 inch diagonal: https://learn.adafruit.com/nokia-5110-3310-monochrome-lcd
    # datasheet: https://www.sparkfun.com/datasheets/LCD/Monochrome/Nokia5110.pdf
    DeviceOptions.NOKIA_5110.value: {
        DeviceParam.CELL_DIM: (0.339e-3, 0.396e-3,),  # TODO: measured by "hand", check elsewhere
        DeviceParam.SLM_SHAPE: (84, 48),
        DeviceParam.MONOCHROME: True,
    },
    # Holoeye SLM - LC 2012
    # https://holoeye.com/lc-2012-spatial-light-modulator/
    # 1.8 inch diagonal #TODO: add documentation, link, lookup values
    # Pixel pitch is defined as the #TODO check pixel pitch -> 36 μm
    # center‐to‐center spacing between adjacent pixels. Interpixel gap describes the
    # edge‐to‐edge spacing between adjacent pixels.
    # 36.9 x 27.6 mm / 1.8”
    DeviceOptions.HOLOEYE_LC_2012.value: {
        DeviceParam.CELL_DIM: (
            0.36e-4,
            0.36e-4,
        ),  # TODO Units in meters, 0.359375e-4, 0.3603515625e-4
        DeviceParam.SLM_SHAPE: (768, 1024),
        DeviceParam.MONOCHROME: True,
    },
}
