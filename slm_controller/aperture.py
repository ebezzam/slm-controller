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
    def __init__(self, slm):
        """
        Digital aperture with a spatial light modulator.

        Parameters
        ----------
        slm : :py:class:`~slm_controller.slm.SLM`
            SLM object on which to program aperture.
        """
        self._slm = slm

    @property
    def area(self):
        """ Area of active cells. """
        return np.sum(self.mask) * np.prod(self._slm.cell_dim)

    @property
    def mask(self):
        """
        Return mask as an :py:class:`~numpy.ndarray` object with shape (3, height, width) for RGB
        or (3, height, width) for grayscale.
        """
        return self._slm.values

    def plot(self, show_tick_labels=False):
        """
        Plot aperture.

        Parameters
        ----------
        show_tick_labels : bool
            Whether to show cell number along x- and y-axis.
        """

        import matplotlib.pyplot as plt

        # prepare mask data for `imshow`, expects the input data array size to be (width, height, 3)
        Z = self.mask.transpose(1, 2, 0)

        # plot
        fig, ax = plt.subplots()
        extent = [
            -0.5 * self._slm.cell_dim[1],
            (self._slm.shape[1] - 0.5) * self._slm.cell_dim[1],
            (self._slm.shape[0] - 0.5) * self._slm.cell_dim[0],
            -0.5 * self._slm.cell_dim[0],
        ]
        ax.imshow(Z, extent=extent)
        ax.grid(which="major", axis="both", linestyle="-", color="0.5", linewidth=0.25)

        x_ticks = np.arange(-0.5, self._slm.shape[1], 1) * self._slm.cell_dim[1]
        ax.set_xticks(x_ticks)
        if show_tick_labels:
            x_tick_labels = (np.arange(-0.5, self._slm.shape[1], 1) + 0.5).astype(int)
        else:
            x_tick_labels = [None] * len(x_ticks)
        ax.set_xticklabels(x_tick_labels)

        y_ticks = np.arange(-0.5, self._slm.shape[0], 1) * self._slm.cell_dim[0]
        ax.set_yticks(y_ticks)
        if show_tick_labels:
            y_tick_labels = (np.arange(-0.5, self._slm.shape[0], 1) + 0.5).astype(int)
        else:
            y_tick_labels = [None] * len(y_ticks)
        ax.set_yticklabels(y_tick_labels)


class RectAperture(DigitalAperture):
    def __init__(self, apert_dim, slm, center=None):
        """
        Object to create rectangular aperture.

        Parameters
        ----------
        apert_dim : tuple(float)
            Dimensions (height, width) in meters of aperture.
        slm : :py:class:`~slm_controller.slm.SLM`
            SLM object on which to program aperture.
        center : tuple(int)
            [Optional] center of aperture along (SLM) coordinates, indexing starts in top-left
            corner. Default is to place center of aperture at center of SLM.
        """

        # check input values
        assert apert_dim[0] > 0
        assert apert_dim[1] > 0

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
        self._center = center

        # compute mask
        self._apert_dim = np.array(apert_dim)
        top_left = self._center - self._apert_dim / 2
        bottom_right = top_left + self._apert_dim
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
        super().__init__(slm=slm)


class LineAperture(RectAperture):
    def __init__(self, length, slm, vertical=True, center=None):
        """
        Object to create line aperture.

        Parameters
        ----------
        length : float
            Length of aperture in meters.
        slm : :py:class:`~slm_controller.slm.SLM`
            SLM object on which to program aperture.
        vertical : bool
            Whether apertude should be vertical line (True), or horizontal line (False).
        center : tuple(int)
            [Optional] center of aperture along (SLM) coordinates, indexing starts in top-left
            corner. Default is to place center of aperture at center of SLM.
        """
        if vertical:
            apert_dim = (length, slm.cell_dim[1])
        else:
            apert_dim = (slm.cell_dim[0], length)
        super().__init__(apert_dim=apert_dim, slm=slm, center=center)


class SquareAperture(RectAperture):
    def __init__(self, side, slm, center=None):
        """
        Object to create line aperture.

        Parameters
        ----------
        side : float
            Side length of square in meters.
        slm : :py:class:`~slm_controller.slm.SLM`
            SLM object on which to program aperture.
        center : tuple(int)
            [Optional] center of aperture along (SLM) coordinates, indexing starts in top-left
            corner. Default is to place center of aperture at center of SLM.
        """
        super().__init__(apert_dim=(side, side), slm=slm, center=center)


class CircAperture(DigitalAperture):
    def __init__(self, radius, slm, center=None):
        """
        Object to create circle aperture.

        Parameters
        ----------
        radius : float
            Radius in meters.
        slm : :py:class:`~slm_controller.slm.SLM`
            SLM object on which to program aperture.
        center : tuple(float)
            [Optional] center of aperture along (SLM) coordinates, indexing starts in top-left
            corner. Default is to place center of aperture at center of SLM.
        """
        # check input values
        assert radius > 0

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
        self._center = center

        # compute mask
        self._radius = radius
        top_left = self._center - radius
        bottom_right = top_left + 2 * self._radius + slm.cell_dim
        r2 = self._radius ** 2
        i, j = np.meshgrid(
            np.arange(top_left[0], bottom_right[0], slm.cell_dim[0]),
            np.arange(top_left[1], bottom_right[1], slm.cell_dim[1]),
            sparse=True,
            indexing="ij",
        )
        x2 = (i - self._center[0]) ** 2
        y2 = (j - self._center[1]) ** 2

        slm[top_left[0] : bottom_right[0], top_left[1] : bottom_right[1]] = x2 + y2 < r2
        super().__init__(slm=slm)
