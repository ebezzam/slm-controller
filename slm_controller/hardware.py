from enum import Enum

# Physical parameters relevant for the propagation
class PhysicalParams(Enum):
    WAVELENGTH = "wavelength"
    PROPAGATION_DISTANCE = "prop_distance"

    @staticmethod
    def values():
        return [param.value for param in PhysicalParams]


# Actual values of those physical parameters
physical_params = {
    PhysicalParams.WAVELENGTH: 532e-9,
    PhysicalParams.PROPAGATION_DISTANCE: 0.34,
}

# Slm devices that are implemented in this project
class SlmDevices(Enum):
    ADAFRUIT_RGB = "rgb"
    ADAFRUIT_BINARY = "binary"
    NOKIA_5110 = "nokia"
    HOLOEYE_LC_2012 = "holoeye"

    @staticmethod
    def values():
        return [slm.value for slm in SlmDevices]


# Parameters of those slms
class SlmParam:
    CELL_DIM = "cell_dim"
    SLM_SHAPE = "slm_shape"
    MONOCHROME = "monochrome"
    FILL_FACTOR = "fill_factor"
    FRAME_RATE = "frame_rate"


# Actual values of those parameters for all the slms
slm_devices = {
    # 1.8 inch RGB display by Adafruit: https://learn.adafruit.com/1-8-tft-display/overview
    # datasheet: https://cdn-shop.adafruit.com/datasheets/JD-T1800.pdf
    SlmDevices.ADAFRUIT_RGB.value: {
        SlmParam.CELL_DIM: (0.18e-3, 0.18e-3),
        SlmParam.SLM_SHAPE: (128, 160),
        SlmParam.MONOCHROME: False,
    },
    # 1.3 inch monochrome display by Adafruit:
    # https://learn.adafruit.com/adafruit-sharp-memory-display-breakout
    # datasheet: https://cdn-shop.adafruit.com/product-files/3502/Data+sheet.pdf
    SlmDevices.ADAFRUIT_BINARY.value: {
        SlmParam.CELL_DIM: (0.145e-3, 0.145e-3),
        SlmParam.SLM_SHAPE: (144, 168),
        SlmParam.MONOCHROME: True,
    },
    # Graphic LCD 84x48 - Nokia 5110
    # https://www.sparkfun.com/products/10168
    # 1.5 inch diagonal: https://learn.adafruit.com/nokia-5110-3310-monochrome-lcd
    # datasheet: https://www.sparkfun.com/datasheets/LCD/Monochrome/Nokia5110.pdf
    SlmDevices.NOKIA_5110.value: {
        SlmParam.CELL_DIM: (
            0.339e-3,
            0.396e-3,
        ),  # TODO: measured by "hand", check elsewhere
        SlmParam.SLM_SHAPE: (84, 48),
        SlmParam.MONOCHROME: True,
    },
    # Holoeye SLM - LC 2012
    # https://holoeye.com/lc-2012-spatial-light-modulator/
    # 1.8 inch diagonal, 36.9 x 27.6 mm
    # datasheet: same link
    SlmDevices.HOLOEYE_LC_2012.value: {
        SlmParam.CELL_DIM: (
            0.36e-4,
            0.36e-4,
        ),  # Computed: 0.359375e-4, 0.3603515625e-4
        SlmParam.SLM_SHAPE: (768, 1024),
        SlmParam.MONOCHROME: True,
        SlmParam.FILL_FACTOR: 0.58,
        SlmParam.FRAME_RATE: 60,
    },
}

# Camera devices that are implemented in this project
class CamDevices(Enum):
    IDS = "ids"

    @staticmethod
    def values():
        return [cam.value for cam in CamDevices]


# Parameters of those cameras
class CamParam:
    IMG_SHAPE = "img_shape"


# Actual values of those parameters for all the cameras
cam_devices = {
    CamDevices.IDS.value: {CamParam.IMG_SHAPE: (1216, 1936)},
}
