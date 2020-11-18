import numpy as np
from enum import Enum

from slm_controller.slm import SLM


class ApertureOptions(Enum):
    RECT = "rect"
    SQUARE = "square"
    LINE = "line"
    CIRC = "circ"

    @staticmethod
    def values():
        return [shape.value for shape in ApertureOptions]


def create_rect_aperture(slm_shape, cell_dim, apert_dim, center=None, monochrome=False):
    """
    Create and return SLM object with rectangular aperture of desired dimensions.

    Parameters
    ----------
    slm_shape : tuple(int)
        Dimensions (height, width) of SLM in cells.
    cell_dim : tuple(float)
        Dimensions (height, width) of each cell in meters.
    apert_dim : tuple(float)
        Dimensions (height, width) of each aperture in meters.
    center : tuple(float)
        [Optional] center of aperture along (SLM) coordinates, indexing starts in top-left corner.
        Default is to place center of aperture at center of SLM.
    monochrome : bool
        [Optional] Whether SLM is monochrome.

    Returns
    -------
    slm : :py:class:`~slm_controller.slm.SLM`
        SLM object with cells programmed to desired rectangular aperture.

    """
    # check input values
    assert np.all(apert_dim) > 0

    # initialize SLM
    slm = SLM(shape=slm_shape, cell_dim=cell_dim, monochrome=monochrome)

    # check / compute center
    if center is None:
        center = slm.center
    else:
        assert (
            0 <= center[0] < slm.height
        ), f"Center {center} must lie within SLM dimensions {slm.dim}."
        assert (
            0 <= center[1] < slm.width
        ), f"Center {center} must lie within SLM dimensions {slm.dim}."

    # compute mask
    apert_dim = np.array(apert_dim)
    top_left = center - apert_dim / 2
    bottom_right = top_left + apert_dim
    if (
        top_left[0] < 0
        or top_left[1] < 0
        or bottom_right[0] >= slm.dim[0]
        or bottom_right[1] >= slm.dim[1]
    ):
        raise ValueError(
            f"Aperture ({top_left[0]}:{bottom_right[0]}, "
            f"{top_left[1]}:{bottom_right[1]}) extends past valid "
            f"SLM dimensions {slm.dim}"
        )
    slm[top_left[0] : bottom_right[0], top_left[1] : bottom_right[1]] = 1

    return slm


def create_line_aperture(slm_shape, cell_dim, length, vertical=True, center=None, monochrome=False):
    """
    Create and return SLM object with a line aperture of desired length.

    Parameters
    ----------
    slm_shape : tuple(int)
        Dimensions (height, width) of SLM in cells.
    cell_dim : tuple(float)
        Dimensions (height, width) of each cell in meters.
    length : float
        Length of aperture in meters.
    center : tuple(float)
        [Optional] center of aperture along (SLM) coordinates, indexing starts in top-left corner.
        Default is to place center of aperture at center of SLM.
    monochrome : bool
        [Optional] Whether SLM is monochrome.

    Returns
    -------
    slm : :py:class:`~slm_controller.slm.SLM`
        SLM object with cells programmed to desired line aperture.

    """

    # call `create_rect_aperture`
    if vertical:
        apert_dim = (length, cell_dim[1])
    else:
        apert_dim = (cell_dim[0], length)
    return create_rect_aperture(slm_shape, cell_dim, apert_dim, center, monochrome)


def create_square_aperture(slm_shape, cell_dim, side, center=None, monochrome=False):
    """
    Create and return SLM object with a square aperture of desired shape.

    Parameters
    ----------
    slm_shape : tuple(int)
        Dimensions (height, width) of SLM in cells.
    cell_dim : tuple(float)
        Dimensions (height, width) of each cell in meters.
    side : float
        Side length of square in meters.
    center : tuple(float)
        [Optional] center of aperture along (SLM) coordinates, indexing starts in top-left corner.
        Default is to place center of aperture at center of SLM.
    monochrome : bool
        [Optional] Whether SLM is monochrome.

    Returns
    -------
    slm : :py:class:`~slm_controller.slm.SLM`
        SLM object with cells programmed to desired square aperture.

    """
    return create_rect_aperture(slm_shape, cell_dim, (side, side), center, monochrome)


def create_circ_aperture(slm_shape, cell_dim, radius, center=None, monochrome=False):
    """
    Create and return SLM object with a circle aperture of desired shape.

    Parameters
    ----------
    slm_shape : tuple(int)
        Dimensions (height, width) of SLM in cells.
    cell_dim : tuple(float)
        Dimensions (height, width) of each cell in meters.
    radius : float
        Radius in meters.
    center : tuple(float)
        [Optional] center of aperture along (SLM) coordinates, indexing starts in top-left corner.
        Default is to place center of aperture at center of SLM.
    monochrome : bool
        [Optional] Whether SLM is monochrome.

    Returns
    -------
    slm : :py:class:`~slm_controller.slm.SLM`
        SLM object with cells programmed to desired circle aperture.

    """
    # check input values
    assert radius > 0

    # initialize SLM
    slm = SLM(shape=slm_shape, cell_dim=cell_dim, monochrome=monochrome)

    # check / compute center
    if center is None:
        center = slm.center
    else:
        assert (
            0 <= center[0] < slm.height
        ), f"Center {center} must lie within SLM dimensions {slm.dim}."
        assert (
            0 <= center[1] < slm.width
        ), f"Center {center} must lie within SLM dimensions {slm.dim}."

    # compute mask
    i, j = np.meshgrid(
        np.arange(slm.dim[0], step=slm.cell_dim[0]),
        np.arange(slm.dim[1], step=slm.cell_dim[1]),
        sparse=True,
        indexing="ij",
    )
    x2 = (i - center[0]) ** 2
    y2 = (j - center[1]) ** 2
    slm.values[:, ] = x2 + y2 < radius ** 2


    # # compute mask
    # top_left = center - radius
    # bottom_right = top_left + 2 * radius + slm.cell_dim
    # r2 = radius ** 2
    # i, j = np.meshgrid(
    #     np.arange(top_left[0], bottom_right[0], slm.cell_dim[0]),
    #     np.arange(top_left[1], bottom_right[1], slm.cell_dim[1]),
    #     sparse=True,
    #     indexing="ij",
    # )
    # x2 = (i - center[0]) ** 2
    # y2 = (j - center[1]) ** 2
    #
    # slm[top_left[0] : bottom_right[0], top_left[1] : bottom_right[1]] = x2 + y2 < r2
    return slm
