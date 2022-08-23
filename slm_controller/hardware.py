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
    MONOCHROME = "monochrome"  # TODO Does this make sense? For Phase etc.?
    FILL_FACTOR = "fill_factor"
    FRAME_RATE = "frame_rate"
    TYPE = "type"
    USEABLE_SHAPE = "useable_shape"


# Actual values of those parameters for all the SLMs
slm_devices = {
    # 1.8 inch RGB SLM by Adafruit: https://learn.adafruit.com/1-8-tft-display/overview
    # datasheet: https://cdn-shop.adafruit.com/datasheets/JD-T1800.pdf
    SLMDevices.ADAFRUIT.value: {
        SLMParam.PIXEL_PITCH: (0.18e-3, 0.18e-3),
        SLMParam.SLM_SHAPE: (128, 160),
        SLMParam.USEABLE_SHAPE: (128, 160),
        SLMParam.MONOCHROME: False,
        SLMParam.TYPE: "Amplitude",
    },
    # Graphic LCD 84x48 - Nokia 5110
    # https://www.sparkfun.com/products/10168
    # 1.5 inch diagonal: https://learn.adafruit.com/nokia-5110-3310-monochrome-lcd
    # datasheet: https://www.sparkfun.com/datasheets/LCD/Monochrome/Nokia5110.pdf
    SLMDevices.NOKIA_5110.value: {
        SLMParam.PIXEL_PITCH: (
            0.339e-3,
            0.396e-3,
        ),  # TODO measured by "hand", check elsewhere
        SLMParam.SLM_SHAPE: (84, 48),
        SLMParam.USEABLE_SHAPE: (84, 48),
        SLMParam.MONOCHROME: True,
        SLMParam.TYPE: "Amplitude",
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
        SLMParam.USEABLE_SHAPE: (  # TODO document this!
            284,
            452,
        ),  # TODO integrate this parameter, or simply pad too small phase maps
        # TODO remove, computations
        # Laser radius = 1cm := r
        # cam ratio = 0.62809917355371900826446280991736 cm := a
        # (w/2)^2 + (w*a/2)^2 <= r^2 <==> w^2(1+a^2)/4 <= 1
        #                            <==> w <= sqrt(4/(1+a^2))
        # ==> w <= 1,6936333680594274148320298206561 cm
        #       <= 470,45371334984094856445272796003 px
        # ==> h <= 295,49 px
        # w = 452
        # h = 284
        SLMParam.MONOCHROME: True,
        SLMParam.TYPE: "Phase",
        SLMParam.FILL_FACTOR: 0.58,
        SLMParam.FRAME_RATE: 60,
    },
}
