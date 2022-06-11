import torch

from slm_controller.hardware import (
    DisplayDevices,
    DisplayParam,
    display_devices,
)

from slm_design.hardware import (
    physical_params,
    PhysicalParams,
)
import slm_design.neural_holography.utils as utils
from slm_design.neural_holography.propagation_ASM import propagation_ASM
from waveprop.waveprop.fraunhofer import fraunhofer
from waveprop.waveprop.fresnel import (
    fresnel_multi_step,
    fresnel_one_step,
    fresnel_two_step,
)
from waveprop.waveprop.rs import angular_spectrum, direct_integration
from waveprop.waveprop.util import ift2

display_device = DisplayDevices.HOLOEYE_LC_2012.value


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
        display_devices[display_device][DisplayParam.CELL_DIM],
        "ASM",
        torch.float32,
        None,
    )


def wave_prop_fraunhofer(slm_field):
    slm_field = slm_field[0, 0, :, :]

    res, _, _ = fraunhofer(
        u_in=slm_field.numpy(),
        wv=physical_params[PhysicalParams.WAVELENGTH],
        d1=display_devices[display_device][DisplayParam.CELL_DIM][0],
        dz=1,
    )

    return torch.from_numpy(res)[None, None, :, :]


def wave_prop_angular_spectrum(slm_field):
    slm_field = slm_field[0, 0, :, :]

    res, _, _ = angular_spectrum(  # TODO flipped
        u_in=slm_field.numpy(),
        wv=physical_params[PhysicalParams.WAVELENGTH],
        d1=display_devices[display_device][DisplayParam.CELL_DIM][0],
        dz=1,
        # out_shift=1,  # TODO check this
    )

    return torch.from_numpy(ift2(res, delta_f=1))[None, None, :, :]
    # return torch.from_numpy(res)[None, None, :, :]


def wave_prop_fresnel(slm_field):
    slm_field = slm_field[0, 0, :, :]

    res, _, _ = fresnel_one_step(  # TODO Too small
        u_in=slm_field.numpy(),
        wv=physical_params[PhysicalParams.WAVELENGTH],
        d1=display_devices[display_device][DisplayParam.CELL_DIM][0],
        dz=1,
    )

    return torch.from_numpy(ift2(res, delta_f=1))[None, None, :, :]


def wave_prop_direct_integration(slm_field):
    slm_field = slm_field[0, 0, :, :]

    res = direct_integration(
        u_in=slm_field.numpy(),
        wv=physical_params[PhysicalParams.WAVELENGTH],
        d1=display_devices[display_device][DisplayParam.CELL_DIM][0],
        dz=1,
        x=[0],  # TODO wrong
        y=[0],  # TODO wrong
    )

    return torch.from_numpy(res)[None, None, :, :]

