import torch
import numpy as np
from PIL import Image
import math

from slm_controller.hardware import DeviceOptions, DeviceParam, devices
import slm_controller.neural_holography.utils as utils

prop_dist = 0.34
wavelength = 532e-9
feature_size = devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.CELL_DIM]
dtype = torch.float32


def load_holoeye():
    im = Image.open("examples/holoeye_slm_pattern.png")
    im = torch.from_numpy(np.array(im)).type(torch.FloatTensor)
    im = torch.mean(im, axis=2)

    # print(torch.min(im), torch.max(im))  # TODO max only 254 ??

    max_val = torch.max(im)
    angles = (im / max_val) * (2 * np.pi) - np.pi
    mags = torch.ones_like(im)

    holoeye_slm_field = torch.polar(mags, angles)

    torch.save(holoeye_slm_field, "examples/slm_field_holoeye.pt")

    return holoeye_slm_field


def load_neural():
    return torch.load("examples/slm_field_neural.pt")


def compute_H():
    # number of pixels
    num_y, num_x = devices[DeviceOptions.HOLOEYE_LC_2012.value][DeviceParam.SLM_SHAPE]

    # sampling inteval size
    dy, dx = feature_size

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
    H_exp = torch.tensor(HH, dtype=dtype)

    # reshape tensor and multiply
    H_exp = torch.reshape(H_exp, (1, 1, *H_exp.size()))

    # multiply by distance
    H_exp = torch.mul(H_exp, prop_dist)

    # band-limited ASM - Matsushima et al. (2009)
    fy_max = 1 / np.sqrt((2 * prop_dist * (1 / y)) ** 2 + 1) / wavelength
    fx_max = 1 / np.sqrt((2 * prop_dist * (1 / x)) ** 2 + 1) / wavelength
    H_filter = torch.tensor(
        ((np.abs(FX) < fx_max) & (np.abs(FY) < fy_max)).astype(np.uint8), dtype=dtype,
    )

    # get real/img components
    H_real, H_imag = utils.polar_to_rect(H_filter, H_exp)

    H = torch.stack((H_real, H_imag), 4)
    H = utils.ifftshift(H)
    H = torch.view_as_complex(H)

    return H


def holoeye_with_lens():
    return load_holoeye()


def holoeye_without_lens():
    holoeye_slm_field = load_holoeye()
    holoeye_slm_field = holoeye_slm_field[None, None, :, :]
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
    )[0, 0, :, :]


def neural_with_lens():
    neural_slm_field = load_neural()
    neural_slm_field = neural_slm_field[None, None, :, :]
    H = compute_H()

    return torch.fft.ifftn(
        torch.fft.ifftn(
            H
            * torch.fft.fftn(
                utils.ifftshift(neural_slm_field), dim=(-2, -1), norm="ortho"
            ),
            dim=(-2, -1),
            norm="ortho",
        ),
        dim=(-2, -1),
        norm="ortho",
    )[0, 0, :, :]


def neural_without_lens():
    return load_neural()
