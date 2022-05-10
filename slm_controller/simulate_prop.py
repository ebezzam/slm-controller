import torch

from slm_controller.hardware import (
    DeviceOptions,
    DeviceParam,
    devices,
    physical_params,
    PhysicalParams,
)
import slm_controller.neural_holography.utils as utils
from slm_controller.neural_holography.propagation_ASM import propagation_ASM


def lens_prop(slm_field):
    return utils.fftshift(torch.fft.fftn(slm_field, dim=(-2, -1), norm="ortho"))


def lensless_prop(slm_field):
    return utils.propagate_field(
        slm_field,
        propagation_ASM,
        physical_params[PhysicalParams.PROPAGATION_DISTANCE],
        physical_params[PhysicalParams.WAVELENGTH],
        devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.CELL_DIM],
        "ASM",
        torch.float32,
        None,
    )
