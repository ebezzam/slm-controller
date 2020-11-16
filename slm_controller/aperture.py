import numpy as np
from enum import Enum


class ApertureOptions(Enum):
    RECT = "rect"
    SQUARE = "square"
    LINE = "line"
    CIRC = "circ"

    @staticmethod
    def values():
        return [shape.value for shape in ApertureOptions]


class DigitalAperture:
    def __init__(self, mask, pixel_shape):
        """
        Abstract class for digital apertures with a spatial light modulator.

        Parameters
        ----------
        mask : :py:class:`~numpy.ndarray`
            ([3,] N_height, N_width) non-negative reals.
        pixel_shape : tuple(float)
            Pixel dimensions (height, width) in meters.
        """
        self._mask = mask
        self._slm_dim = (mask.shape[-2], mask.shape[-1])
        assert len(pixel_shape) == 2
        assert pixel_shape[0] > 0
        assert pixel_shape[1] > 0
        self._pixel_shape = pixel_shape

    @property
    def size(self):
        return np.prod(self._slm_dim)

    @property
    def shape(self):
        return self._slm_dim

    @property
    def mask(self):
        """
        Return mask as an :py:class:`~numpy.ndarray` object with shape (3, height, width).
        """
        return self._mask

    def plot(self, show_tick_labels=False):

        import matplotlib.pyplot as plt

        # prepare mask data for `imshow`, expects the input data array size to be (width, height, 3)
        Z = self.mask.transpose(1, 2, 0)

        # plot
        fig, ax = plt.subplots()
        # ax.imshow(Z)
        extent = [
            -0.5 * self._pixel_shape[1],
            (self._slm_dim[1] - 0.5) * self._pixel_shape[1],
            (self._slm_dim[0] - 0.5) * self._pixel_shape[0],
            -0.5 * self._pixel_shape[0],
        ]
        ax.imshow(Z, extent=extent)
        ax.grid(which="major", axis="both", linestyle="-", color="0.5", linewidth=0.25)

        x_ticks = np.arange(-0.5, self._slm_dim[1], 1) * self._pixel_shape[1]
        ax.set_xticks(x_ticks)
        if show_tick_labels:
            x_tick_labels = (np.arange(-0.5, self._slm_dim[1], 1) + 0.5).astype(int)
        else:
            x_tick_labels = [None] * len(x_ticks)
        ax.set_xticklabels(x_tick_labels)

        y_ticks = np.arange(-0.5, self._slm_dim[0], 1) * self._pixel_shape[0]
        ax.set_yticks(y_ticks)
        if show_tick_labels:
            y_tick_labels = (np.arange(-0.5, self._slm_dim[0], 1) + 0.5).astype(int)
        else:
            y_tick_labels = [None] * len(y_ticks)
        ax.set_yticklabels(y_tick_labels)


class RectAperture(DigitalAperture):
    def __init__(self, apert_dim, slm_dim, pixel_shape, center=None):
        """
        Object to create rectangular aperture.

        Parameters
        ----------
        apert_dim : tuple(int)
            Dimensions (height, width) of aperture.
        slm_dim : tuple(int)
            Dimensions (height, width) of the spatial light modulator (SLM).
        pixel_shape : tuple(float)
            Pixel dimensions (height, width) in meters.
        center : tuple(int)
            [Optional] center of aperture along (SLM) coordinates, indexing starts in top-left
            corner. Default is to place center of aperture at center of SLM.
        """

        # check input values
        assert apert_dim[0] > 0
        assert apert_dim[1] > 0
        assert slm_dim[0] > 0
        assert slm_dim[1] > 0

        # check / compute center
        if center is None:
            center = (slm_dim[0] // 2, slm_dim[1] // 2)
        else:
            assert (
                0 <= center[0] < slm_dim[0]
            ), f"Center {center} must lie within SLM dimensions {slm_dim}."
            assert (
                0 <= center[1] < slm_dim[1]
            ), f"Center {center} must lie within SLM dimensions {slm_dim}."
        self._center = center

        # compute mask
        self._apert_dim = apert_dim
        top_left = (
            self._center[0] - self._apert_dim[0] // 2,
            self._center[1] - self._apert_dim[1] // 2,
        )
        bottom_right = (top_left[0] + self._apert_dim[0], top_left[1] + self._apert_dim[1])
        if (
            top_left[0] < 0
            or top_left[1] < 0
            or bottom_right[0] >= slm_dim[0]
            or bottom_right[1] >= slm_dim[1]
        ):
            raise ValueError(
                f"Aperture ({top_left[0]}:{bottom_right[0]}, "
                f"{top_left[1]}:{bottom_right[1]}) extends past valid "
                f"SLM indices (0:{slm_dim[0] - 1}, 0:{slm_dim[1] - 1})"
            )
        mask = np.zeros((3,) + slm_dim)
        mask[:, top_left[0] : bottom_right[0], top_left[1] : bottom_right[1]] = 1

        # call parent constructor
        super().__init__(mask=mask, pixel_shape=pixel_shape)


class LineAperture(RectAperture):
    def __init__(self, n_pixels, slm_dim, pixel_shape, vertical=True, center=None):
        """
        Object to create line aperture.

        Parameters
        ----------
        n_pixels : int
            Number of pixels for aperture.
        slm_dim : tuple(int)
            Dimensions (height, width) of the spatial light modulator (SLM).
        pixel_shape : tuple(float)
            Pixel dimensions (height, width) in meters.
        vertical : bool
            Whether apertude should be vertical line (True), or horizontal line (False).
        center : tuple(int)
            [Optional] center of aperture along (SLM) coordinates, indexing starts in top-left
            corner. Default is to place center of aperture at center of SLM.
        """
        if vertical:
            apert_dim = (n_pixels, 1)
        else:
            apert_dim = (1, n_pixels)
        super().__init__(
            apert_dim=apert_dim, slm_dim=slm_dim, pixel_shape=pixel_shape, center=center
        )


class SquareAperture(RectAperture):
    def __init__(self, side, slm_dim, pixel_shape, center=None):
        """
        Object to create line aperture.

        Parameters
        ----------
        side : int
            Number of pixels for each side length.
        slm_dim : tuple(int)
            Dimensions (height, width) of the spatial light modulator (SLM).
        pixel_shape : tuple(float)
            Pixel dimensions (height, width) in meters.
        center : tuple(int)
            [Optional] center of aperture along (SLM) coordinates, indexing starts in top-left
            corner. Default is to place center of aperture at center of SLM.
        """
        super().__init__(
            apert_dim=(side, side), slm_dim=slm_dim, pixel_shape=pixel_shape, center=center
        )


class CircAperture(DigitalAperture):
    def __init__(self, radius, slm_dim, pixel_shape, center=None):
        """
        Object to create line aperture.

        Parameters
        ----------
        radius : int
            Radius in number of pixels.
        slm_dim : tuple(int)
            Dimensions (height, width) of the spatial light modulator (SLM).
        pixel_shape : tuple(float)
            Pixel dimensions (height, width) in meters.
        center : tuple(int)
            [Optional] center of aperture along (SLM) coordinates, indexing starts in top-left
            corner. Default is to place center of aperture at center of SLM.
        """
        # check input values
        assert radius > 0
        assert slm_dim[0] > 0
        assert slm_dim[1] > 0

        # check / compute center
        if center is None:
            center = (slm_dim[0] // 2, slm_dim[1] // 2)
        else:
            assert (
                0 <= center[0] < slm_dim[0]
            ), f"Center {center} must lie within SLM dimensions {slm_dim}."
            assert (
                0 <= center[1] < slm_dim[1]
            ), f"Center {center} must lie within SLM dimensions {slm_dim}."
        self._center = center

        # compute mask
        self._radius = radius
        mask = np.zeros((3,) + slm_dim)
        top_left = (self._center[0] - self._radius, self._center[1] - self._radius)
        bottom_right = (top_left[0] + 2 * self._radius, top_left[1] + 2 * self._radius)
        r2 = self._radius ** 2
        i, j = np.meshgrid(
            np.arange(top_left[0], bottom_right[0] + 1),
            np.arange(top_left[1], bottom_right[1] + 1),
            sparse=True,
            indexing="ij",
        )
        x2 = (i - self._center[0]) ** 2
        y2 = (j - self._center[1]) ** 2
        mask[:, i, j] = np.floor(x2 + y2) < r2
        super().__init__(mask=mask, pixel_shape=pixel_shape)
