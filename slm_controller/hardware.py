class DeviceOptions:
    ADAFRUIT_RGB = "adafruit_1p8_tft_rgb"
    ADAFRUIT_GRAYSCALE = "adafruit_1p3_lcd_gray"


class DeviceParam:
    PIXEL_SHAPE = "pixel_shape"
    SLM_DIM = "slm_dim"


devices = {
    # 1.8'' RGB display by Adafruit: https://learn.adafruit.com/1-8-tft-display/overview
    # datasheet: https://cdn-shop.adafruit.com/datasheets/JD-T1800.pdf
    DeviceOptions.ADAFRUIT_RGB: {
        DeviceParam.PIXEL_SHAPE: (0.18e-3, 0.18e-3),
        DeviceParam.SLM_DIM: (128, 160),
    },
    # 1.3'' monochrome display by Adafruit: https://learn.adafruit.com/adafruit-sharp-memory-display-breakout
    # datasheet: https://cdn-shop.adafruit.com/product-files/3502/Data+sheet.pdf
    DeviceOptions.ADAFRUIT_GRAYSCALE: {
        DeviceParam.PIXEL_SHAPE: (0.145e-3, 0.145e-3),
        DeviceParam.SLM_DIM: (144, 168),
    },
}
