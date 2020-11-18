from enum import Enum


class DeviceOptions(Enum):
    ADAFRUIT_RGB = "rgb"
    ADAFRUIT_MONOCHROME = "mono"

    @staticmethod
    def values():
        return [dev.value for dev in DeviceOptions]


class DeviceParam:
    CELL_DIM = "cell_dim"
    SLM_SHAPE = "slm_shape"
    MONOCHROME = "monochrome"


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
    DeviceOptions.ADAFRUIT_MONOCHROME.value: {
        DeviceParam.CELL_DIM: (0.145e-3, 0.145e-3),
        DeviceParam.SLM_SHAPE: (144, 168),
        DeviceParam.MONOCHROME: True,
    },
}
