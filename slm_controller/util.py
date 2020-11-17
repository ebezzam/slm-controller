import numpy as np
from PIL import Image


def load_image(fname, output_shape=None, keep_aspect_ratio=True):
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


def _pixel_slice(_slice, pixel_m):
    """
    Convert slice indexing in meters to slice indexing in pixels.

    Parameters
    ----------
    _slice : slice
        Original slice in meters.
    pixel_m : float
        Pixel dimension in meters.
    """
    if _slice.start is not None:
        start = _m_to_pixel(_slice.start, pixel_m)
    else:
        start = None
    if _slice.stop is not None:
        stop = _m_to_pixel(_slice.stop, pixel_m)
    else:
        stop = None
    if _slice.step is not None:
        step = _m_to_pixel(_slice.step, pixel_m)
    else:
        step = None
    return slice(start, stop, step)


def _m_to_pixel(val, pixel_m):
    """
    Convert location to pixel index.

    Parameters
    ----------
    val : float
        Location in meters.
    pixel_m : float
        Dimension of pixel in meters.
    """
    return int(val / pixel_m)


def _prepare_index_vals(key, pixel_shape):
    """
    Convert indexing object in meters to indexing object in pixels.

    Parameters
    ----------
    key : int, float, slice, or list
        Indexing operation in meters.
    pixel_shape : tuple(float)
        Pixel dimensions (height, width) in meters.
    """

    if isinstance(key, float) or isinstance(key, int):
        idx = tuple([slice(None), _m_to_pixel(key, pixel_shape[0])])

    elif isinstance(key, slice):
        idx = tuple([slice(None), _pixel_slice(key, pixel_shape[0])])

    elif len(key) == 2:
        idx = [slice(None)]
        for k, _slice in enumerate(key):

            if isinstance(_slice, slice):
                idx.append(_pixel_slice(_slice, pixel_shape[k]))

            elif isinstance(_slice, float) or isinstance(_slice, int):
                idx.append(_m_to_pixel(_slice, pixel_shape[k]))

            else:
                raise ValueError("Invalid key.")
        idx = tuple(idx)

    elif len(key) == 3:
        raise NotImplementedError("Cannot index individual channels.")

    else:
        raise ValueError("Invalid key.")
    return idx
