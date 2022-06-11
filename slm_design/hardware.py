from enum import Enum

# Physical parameters relevant for the propagation
class PhysicalParams(Enum):  # TODO better place?
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

# Camera devices that are implemented in this project
class CamDevices(Enum):
    DUMMY = "dummy"  # TODO for development only! Remove!
    IDS = "ids"

    @staticmethod
    def values():
        return [cam.value for cam in CamDevices]


# Parameters of those cameras
class CamParam:
    IMG_SHAPE = "img_shape"


# Actual values of those parameters for all the cameras
cam_devices = {
    CamDevices.DUMMY.value: {
        # CamParam.IMG_SHAPE: slm_display_devices[
        #     SlmDisplayDevices.HOLOEYE_LC_2012.value
        # ][SlmParam.SLM_SHAPE]
        CamParam.IMG_SHAPE: (1216, 1936)
    },
    CamDevices.IDS.value: {CamParam.IMG_SHAPE: (1216, 1936)},
}
