import abc
import numpy as np


class DigitalAperture:
    def __init__(self, slm_dim):
        """
        Abstract class for digital apertures with a spatial light modulator.

        Parameters
        ----------
        slm_dim : tuple(int)
            Dimensions (height, width) of the spatial light modulator.
        """
        assert slm_dim[0] > 0
        assert slm_dim[1] > 1
        self._slm_dim = slm_dim
        self._mask = None

    @property
    def n_slm_pixels(self):
        return self._slm_dim[0] * self._slm_dim[1]

    @property
    def mask(self):
        """
        Return mask as an :py:class:`~numpy.ndarray` object with shape (3, height, width).
        """
        return self._mask

    @abc.abstractmethod
    def _compute_mask(self):
        pass

    def plot(self):

        import matplotlib.pyplot as plt

        # prepare mask data for `imshow`, expects the input data array size to be (width, height, 3)
        Z = self.mask.transpose(1, 2, 0)

        # plot
        fig, ax = plt.subplots()
        ax.imshow(Z)
        ax.grid(which="major", axis="both", linestyle="-", color="0.5", linewidth=0.25)

        x_ticks = np.arange(-0.5, self._slm_dim[1], 1)
        labels_x = [None] * len(x_ticks)
        plt.xticks(x_ticks, labels=labels_x)
        y_ticks = np.arange(-0.5, self._slm_dim[0], 1)
        labels_y = [None] * len(y_ticks)
        plt.yticks(y_ticks, labels=labels_y)


class RectAperture(DigitalAperture):
    def __init__(self, apert_dim, slm_dim, center=None):
        """
        Object to create rectangular aperture.

        Parameters
        ----------
        apert_dim : tuple(int)
            Dimensions (height, width) of aperture.
        slm_dim : tuple(int)
            Dimensions (height, width) of the spatial light modulator (SLM).
        center : tuple(int)
            [Optional] center of aperture along (SLM) coordinates, indexing starts in top-left
            corner. Default is to place center of aperture at center of SLM.
        """

        super().__init__(slm_dim=slm_dim)
        assert apert_dim[0] > 0
        assert apert_dim[1] > 1
        self._apert_dim = apert_dim
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
        self._compute_mask()

    def _compute_mask(self):

        # determine position of aperture
        top_left = (
            self._center[0] - self._apert_dim[0] // 2,
            self._center[1] - self._apert_dim[1] // 2,
        )
        bottom_right = (top_left[0] + self._apert_dim[0], top_left[1] + self._apert_dim[1])
        if (
            top_left[0] < 0
            or top_left[1] < 0
            or bottom_right[0] >= self._slm_dim[0]
            or bottom_right[1] >= self._slm_dim[1]
        ):
            raise ValueError(
                f"Aperture ({top_left[0]}:{bottom_right[0]}, "
                f"{top_left[1]}:{bottom_right[1]}) extends past valid "
                f"SLM indices (0:{self._slm_dim[0] - 1}, 0:{self._slm_dim[1] - 1})"
            )

        # create mask
        self._mask = np.zeros((3,) + self._slm_dim)
        self._mask[:, top_left[0] : bottom_right[0], top_left[1] : bottom_right[1]] = 1
