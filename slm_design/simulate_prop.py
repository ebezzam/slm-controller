import torch

from slm_controller.hardware import (
    DisplayDevices,
    SlmParam,
    display_devices,
)

from slm_design.hardware import (
    physical_params,
    PhysicalParams,
)
import slm_design.neural_holography.utils as utils
from slm_design.neural_holography.propagation_ASM import propagation_ASM

slm_device = DisplayDevices.HOLOEYE_LC_2012.value


def lens_prop(slm_field):
    """
    Simulated propagation with a lens (holoeye setting) between slm and target plane.

    Parameters
    ----------
    slm_field : torch.Tensor
        The phase map to be propagated

    Returns
    -------
    torch.Tensor
        The result of the propagation at the target plane
    """
    return utils.fftshift(torch.fft.fftn(slm_field, dim=(-2, -1), norm="ortho"))


def lensless_prop(slm_field):
    """
    Simulated propagation with a no lens (neural holography setting) between slm and target plane.

    Parameters
    ----------
    slm_field : torch.Tensor
        The phase map to be propagated

    Returns
    -------
    torch.Tensor
        The result of the propagation at the target plane
    """
    return utils.propagate_field(
        slm_field,
        propagation_ASM,
        physical_params[PhysicalParams.PROPAGATION_DISTANCE],
        physical_params[PhysicalParams.WAVELENGTH],
        display_devices[slm_device][SlmParam.CELL_DIM],
        "ASM",
        torch.float32,
        None,
    )
