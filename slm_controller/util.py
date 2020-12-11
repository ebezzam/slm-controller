import numpy as np
from PIL import Image, ImageOps


def load_image(fname, output_shape=None, keep_aspect_ratio=True, grayscale=False):
    """
    Load an image.

    Parameters
    ----------
    fname : str, path-like
        Valid image file (i.e. JPG, PNG, BMP, TIFF, etc.)
    output_shape : tuple(int)
        [Optional] rescale image to (height, width) pixels.
    keep_aspect_ratio : bool
        Preserve original image aspect-ratio.

    Returns
    -------
    I : :py:class:`~numpy.ndarray`
        ([N_channel,] N_height, N_width) image.
        Output dtype is format-dependent.
    """
    I_p = Image.open(fname, mode="r")

    # rescale and resize if need be
    if output_shape is not None:

        if keep_aspect_ratio:
            height = output_shape[0]
            width = output_shape[1]
            image_ratio = I_p.width / I_p.height
            screen_ratio = width / height
            if screen_ratio < image_ratio:
                scaled_width = I_p.width * height // I_p.height
                scaled_height = height
            else:
                scaled_width = width
                scaled_height = I_p.height * width // I_p.width
            I_p = I_p.resize((scaled_width, scaled_height), Image.BICUBIC)

            # crop and center
            x = scaled_width // 2 - width // 2
            y = scaled_height // 2 - height // 2
            I_p = I_p.crop((x, y, x + width, y + height))
        else:
            I_p = I_p.resize((output_shape[1], output_shape[0]), Image.BICUBIC)
    else:

        if not keep_aspect_ratio:
            raise ValueError("Must provide [output_shape] if [keep_aspect_ratio] is False.")

    if grayscale:
        I_p = ImageOps.grayscale(I_p)

    # re-order dimensions
    I = np.asarray(I_p)  # (N_height, N_width [, N_channel])
    if I.ndim > 2:
        I = I.transpose(2, 0, 1)
    return I


def save_image(I, fname):
    """
    Save image to a file.

    Parameters
    ----------
    I : :py:class:`~numpy.ndarray`
        (N_channel, N_height, N_width) image.
    fname : str, path-like
        Valid image file (i.e. JPG, PNG, BMP, TIFF, etc.).
    """
    I_max = I.max()
    I_max = 1 if np.isclose(I_max, 0) else I_max

    I_f = I / I_max  # float64
    I_u = np.uint8(255 * I_f)  # uint8

    if I.ndim == 3:
        I_u = I_u.transpose(1, 2, 0)

    I_p = Image.fromarray(I_u)
    I_p.save(fname)


def rgb2gray(rgb, weights=None):
    """
    Convert RGB array to grayscale.

    Parameters
    ----------
    rgb : :py:class:`~numpy.ndarray`
        (N_channel, N_height, N_width) image.
    weights : :py:class:`~numpy.ndarray`
        [Optional] (3,) weights to convert from RGB to grayscale.
    """
    if weights is None:
        weights = np.array([0.299, 0.587, 0.144])
    assert len(weights) == 3
    return np.tensordot(rgb, weights, axes=((0,), 0))


def _cell_slice(_slice, cell_m):
    """
    Convert slice indexing in meters to slice indexing in cells.

    Parameters
    ----------
    _slice : slice
        Original slice in meters.
    cell_m : float
        Cell dimension in meters.
    """
    if _slice.start is not None:
        start = _m_to_cell_idx(_slice.start, cell_m)
    else:
        start = None
    if _slice.stop is not None:
        stop = _m_to_cell_idx(_slice.stop, cell_m)
    else:
        stop = None
    if _slice.step is not None:
        step = _m_to_cell_idx(_slice.step, cell_m)
    else:
        step = None
    return slice(start, stop, step)


def _m_to_cell_idx(val, cell_m):
    """
    Convert location to cell index.

    Parameters
    ----------
    val : float
        Location in meters.
    cell_m : float
        Dimension of cell in meters.
    """
    return int(val / cell_m)


def si2cell(val: np.ndarray, cell_m):
    """
    Convert locations to cell index.

    Parameters
    ----------
    val : :py:class:`~numpy.ndarray`
        Locations in meters.
    cell_m : float
        Dimension of cell in meters.
    """
    return np.array(val // cell_m, dtype=int)


def _prepare_index_vals(key, cell_shape):
    """
    Convert indexing object in meters to indexing object in cell indices.

    Parameters
    ----------
    key : int, float, slice, or list
        Indexing operation in meters.
    cell_shape : tuple(float)
        Cell dimensions (height, width) in meters.
    """

    if isinstance(key, float) or isinstance(key, int):
        idx = slice(None), _m_to_cell_idx(key, cell_shape[0])

    elif isinstance(key, slice):
        idx = slice(None), _cell_slice(key, cell_shape[0])

    elif len(key) == 2:
        idx = [slice(None)]
        for k, _slice in enumerate(key):

            if isinstance(_slice, slice):
                idx.append(_cell_slice(_slice, cell_shape[k]))

            elif isinstance(_slice, float) or isinstance(_slice, int):
                idx.append(_m_to_cell_idx(_slice, cell_shape[k]))

            else:
                raise ValueError("Invalid key.")
        idx = tuple(idx)

    elif len(key) == 3:
        raise NotImplementedError("Cannot index individual channels.")

    else:
        raise ValueError("Invalid key.")
    return idx
