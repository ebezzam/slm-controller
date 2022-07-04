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
    if fname.endswith(".npy"):
        return np.load(fname)
        # TODO possible resizing
    else:
        I_p = Image.open(fname, mode="r")

    # rescale and resize if need be
    if output_shape is None:
        if not keep_aspect_ratio:
            raise ValueError(
                "Must provide [output_shape] if [keep_aspect_ratio] is False."
            )

    elif keep_aspect_ratio:
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
    if grayscale:
        I_p = ImageOps.grayscale(I_p)

    # re-order dimensions
    I = np.asarray(I_p)  # (N_height, N_width [, N_channel])
    if I.ndim > 2:
        I = I.transpose(2, 0, 1)
    return I


# def save_image(I, fname): #TODO not used
#     """
#     Save image to a file.

#     Parameters
#     ----------
#     I : :py:class:`~numpy.ndarray`
#         (N_channel, N_height, N_width) image.
#     fname : str, path-like
#         Valid image file (i.e. JPG, PNG, BMP, TIFF, etc.).
#     """
#     I_max = I.max()
#     I_max = 1 if np.isclose(I_max, 0) else I_max

#     I_f = I / I_max  # float64
#     I_u = np.uint8(255 * I_f)  # uint8

#     if I.ndim == 3:
#         I_u = I_u.transpose(1, 2, 0)

#     I_p = Image.fromarray(I_u)
#     I_p.save(fname)
