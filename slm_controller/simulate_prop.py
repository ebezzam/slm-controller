import torch

from slm_controller.hardware import (
    SlmDevices,
    SlmParam,
    slm_devices,
    physical_params,
    PhysicalParams,
)
import slm_controller.neural_holography.utils as utils
from slm_controller.neural_holography.propagation_ASM import propagation_ASM


def lens_prop(slm_field):
    """
    Simulated propagation with a lens (holoeye setting) between slm and target plane.

    Parameters #TODO
    ----------
    slm_field : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    return utils.fftshift(torch.fft.fftn(slm_field, dim=(-2, -1), norm="ortho"))


def lensless_prop(slm_field):
    """
    Simulated propagation with a no lens (neural holography setting) between slm and target plane.

    Parameters #TODO
    ----------
    slm_field : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    return utils.propagate_field(
        slm_field,
        propagation_ASM,
        physical_params[PhysicalParams.PROPAGATION_DISTANCE],
        physical_params[PhysicalParams.WAVELENGTH],
        slm_devices[SlmDevices.HOLOEYE_LC_2012.value][SlmParam.CELL_DIM],
        "ASM",
        torch.float32,
        None,
    )
