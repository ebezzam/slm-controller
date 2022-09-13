from enum import Enum


# SLM devices that are implemented in this project
class SLMDevices(Enum):
    ADAFRUIT = "adafruit"
    NOKIA_5110 = "nokia"
    HOLOEYE_LC_2012 = "holoeye"

    @staticmethod
    def values():
        return [device.value for device in SLMDevices]


# Parameters of those SLMs
class SLMParam:
    PIXEL_PITCH = "pixel_pitch"
    SLM_SHAPE = "slm_shape"
    MONOCHROME = "monochrome"
    FILL_FACTOR = "fill_factor"
    FRAME_RATE = "frame_rate"
    AMPLITUDE = "amplitude_or_phase"


# Actual values of those parameters for all the SLMs
slm_devices = {
    # 1.8 inch RGB SLM by Adafruit: https://learn.adafruit.com/1-8-tft-display/overview
    # datasheet: https://cdn-shop.adafruit.com/datasheets/JD-T1800.pdf
    SLMDevices.ADAFRUIT.value: {
        SLMParam.PIXEL_PITCH: (0.18e-3, 0.18e-3),
        SLMParam.SLM_SHAPE: (128, 160),
        SLMParam.MONOCHROME: False,
        SLMParam.AMPLITUDE: True,
    },
    # Graphic LCD 84x48 - Nokia 5110
    # https://www.sparkfun.com/products/10168
    # 1.5 inch diagonal: https://learn.adafruit.com/nokia-5110-3310-monochrome-lcd
    # datasheet: https://www.sparkfun.com/datasheets/LCD/Monochrome/Nokia5110.pdf
    SLMDevices.NOKIA_5110.value: {
        SLMParam.PIXEL_PITCH: (
            0.339e-3,
            0.396e-3,
        ),  # no official docs on this; deduced from specs
        SLMParam.SLM_SHAPE: (84, 48),
        SLMParam.MONOCHROME: True,
        SLMParam.AMPLITUDE: True,
    },
    # Holoeye SLM - LC 2012
    # https://holoeye.com/lc-2012-spatial-light-modulator/
    # 1.8 inch diagonal, 36.9 x 27.6 mm
    # datasheet: same link
    SLMDevices.HOLOEYE_LC_2012.value: {
        SLMParam.PIXEL_PITCH: (
            0.36e-4,
            0.36e-4,
        ),  # Computed: 0.359375e-4, 0.3603515625e-4
        SLMParam.SLM_SHAPE: (768, 1024),
        SLMParam.MONOCHROME: True,
        SLMParam.AMPLITUDE: False,
        SLMParam.FILL_FACTOR: 0.58,
        SLMParam.FRAME_RATE: 60,
    },
}
