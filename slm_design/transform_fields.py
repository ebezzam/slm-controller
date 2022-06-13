import torch
import numpy as np
import math

from slm_controller.hardware import (
    SLMDevices,
    SLMParam,
    slm_devices,
)

from slm_design.hardware import (
    physical_params,
    PhysicalParams,
)

import slm_design.neural_holography.utils as utils

slm_device = SLMDevices.HOLOEYE_LC_2012.value


def __compute_H():
    """
    https://github.com/computational-imaging/neural-holography/blob/d2e399014aa80844edffd98bca34d2df80a69c84/propagation_ASM.py

    Compute H which is used in neural holography code, core is imported as is.

    This code and data is released under the Creative Commons Attribution-NonCommercial 4.0 International license (CC BY-NC.) In a nutshell:
        # The license is only for non-commercial use (commercial licenses can be obtained from Stanford).
        # The material is provided as-is, with no warranties whatsoever.
        # If you publish any code, data, or scientific work based on this, please cite our work.

    Technical Paper:
    Y. Peng, S. Choi, N. Padmanaban, G. Wetzstein. Neural Holography with Camera-in-the-loop Training. ACM TOG (SIGGRAPH Asia), 2020.

    Returns
    -------
    torch.Tensor
        H (#TODO probably for homography)
    """

    prop_dist = physical_params[PhysicalParams.PROPAGATION_DISTANCE]
    wavelength = physical_params[PhysicalParams.WAVELENGTH]

    # number of pixels
    num_y, num_x = slm_devices[slm_device][SLMParam.SLM_SHAPE]

    # sampling interval size
    dy, dx = slm_devices[slm_device][SLMParam.CELL_DIM]

    # size of the field
    y, x = (dy * float(num_y), dx * float(num_x))

    # frequency coordinates sampling
    fy = np.linspace(-1 / (2 * dy) + 0.5 / (2 * y), 1 / (2 * dy) - 0.5 / (2 * y), num_y)
    fx = np.linspace(-1 / (2 * dx) + 0.5 / (2 * x), 1 / (2 * dx) - 0.5 / (2 * x), num_x)

    # momentum/reciprocal space
    FX, FY = np.meshgrid(fx, fy)

    # transfer function in numpy (omit distance)
    HH = 2 * math.pi * np.sqrt(1 / wavelength ** 2 - (FX ** 2 + FY ** 2))

    # create tensor & upload to device (GPU)
    H_exp = torch.tensor(HH, dtype=torch.float32)

    # reshape tensor and multiply
    H_exp = torch.reshape(H_exp, (1, 1, *H_exp.size()))

    # multiply by distance
    H_exp = torch.mul(H_exp, prop_dist)

    # band-limited ASM - Matsushima et al. (2009)
    fy_max = 1 / np.sqrt((2 * prop_dist * (1 / y)) ** 2 + 1) / wavelength
    fx_max = 1 / np.sqrt((2 * prop_dist * (1 / x)) ** 2 + 1) / wavelength
    H_filter = torch.tensor(
        ((np.abs(FX) < fx_max) & (np.abs(FY) < fy_max)).astype(np.uint8),
        dtype=torch.float32,
    )

    # get real/img components
    H_real, H_imag = utils.polar_to_rect(H_filter, H_exp)

    H = torch.stack((H_real, H_imag), 4)
    H = utils.ifftshift(H)
    H = torch.view_as_complex(H)

    return H


def lens_to_lensless(holoeye_slm_field):
    """
    Transform from the lens setting (holoeye) to the lensless setting (neural
    holography).

    Parameters
    ----------
    holoeye_slm_field : torch.Tensor
        The phase map that needs to be transformed

    Returns
    -------
    torch.Tensor
        The transformed phase map
    """

    H = __compute_H()

    return utils.fftshift(
        torch.fft.ifftn(
            torch.fft.fftn(
                torch.fft.fftn(holoeye_slm_field, dim=(-2, -1), norm="ortho"),
                dim=(-2, -1),
                norm="ortho",
            )
            / H,
            dim=(-2, -1),
            norm="ortho",
        )
    )


def lensless_to_lens(neural_holography_slm_field):
    """
    Transform from the lensless setting (neural holography) to the lens setting
    (holoeye).

    Parameters
    ----------
    neural_holography_slm_field : torch.Tensor
        The phase map that needs to be transformed

    Returns
    -------
    torch.Tensor
        The transformed phase map
    """
    H = __compute_H()

    return torch.fft.ifftn(
        torch.fft.ifftn(
            H
            * torch.fft.fftn(
                utils.ifftshift(neural_holography_slm_field), dim=(-2, -1), norm="ortho"
            ),
            dim=(-2, -1),
            norm="ortho",
        ),
        dim=(-2, -1),
        norm="ortho",
    )

