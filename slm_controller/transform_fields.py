import torch
import numpy as np
from PIL import Image
import math

from slm_controller.hardware import (
    SlmDevices,
    SlmParam,
    slm_devices,
    physical_params,
    PhysicalParams,
)
import slm_controller.neural_holography.utils as utils


def load_holoeye_slm_pattern(
    path="images/holoeye_outputs/holoeye_logo_slm_pattern.png",
):
    """
    Load a phase map generate with holoeye software and transform it into a
    compliant form.

    Parameters
    ----------
    path : str, optional
        The path to the phase map to load, by default
        "images/holoeye_outputs/holoeye_logo_slm_pattern.png"

    Returns
    -------
    torch.Tensor
        The phase map transformed into a compliant form
    """
    im = Image.open(path)
    im = torch.from_numpy(np.array(im)).type(torch.FloatTensor)
    im = torch.mean(im, axis=2)

    max_val = torch.max(im)
    angles = (im / max_val) * (2 * np.pi) - np.pi

    holoeye_slm_field = extend_to_complex(angles)

    return holoeye_slm_field[None, None, :, :]


def extend_to_complex(angles):
    """
    Extend a tensor of angles into a complex tensor where the angles are used in
    the polar form for complex numbers and the respective magnitudes are set to
    1.

    Parameters
    ----------
    angles : torch.Tensor
        The tensor of angles to be used in the polar form

    Returns
    -------
    torch.Tensor
        The extended complex tensor
    """
    mags = torch.ones_like(angles)
    return torch.polar(mags, angles)


def compute_H():
    """
    Compute H which is used in neural holography code and is needed to undo
    certain operations.

    Returns
    -------
    torch.Tensor
        H (#TODO probably for homography)
    """
    prop_dist = physical_params[PhysicalParams.PROPAGATION_DISTANCE]
    wavelength = physical_params[PhysicalParams.WAVELENGTH]

    # number of pixels
    num_y, num_x = slm_devices[SlmDevices.HOLOEYE_LC_2012.value][SlmParam.SLM_SHAPE]

    # sampling interval size
    dy, dx = slm_devices[SlmDevices.HOLOEYE_LC_2012.value][SlmParam.CELL_DIM]

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
    H = compute_H()

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
    H = compute_H()

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

