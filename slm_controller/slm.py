import numpy as np

from slm_controller.util import _prepare_index_vals


class SLM:
    def __init__(self, shape, pixel_shape, grayscale=False):
        """
        Class for defining SLM.

        Parameters
        ----------
        shape : tuple(int)
            (height, width) in number of pixels.
        pixel_shape : tuple(float)
            Pixel dimensions (height, width) in meters.
        """
        assert shape[0] > 0
        assert shape[1] > 0
        assert pixel_shape[0] > 0
        assert pixel_shape[1] > 0
        self._shape = shape
        self._pixel_shape = pixel_shape
        self._shape_m = (shape[0] * pixel_shape[0], shape[1] * pixel_shape[1])
        if grayscale:
            self._values = np.zeros((1,) + shape)
        else:
            self._values = np.zeros((3,) + shape)

    @property
    def size(self):
        return np.prod(self._shape)

    @property
    def shape(self):
        return self._shape

    @property
    def pixel_shape(self):
        return self._pixel_shape

    @property
    def pixel_area(self):
        return np.prod(self._pixel_shape)

    @property
    def dim(self):
        return self._shape_m

    @property
    def area(self):
        return np.prod(self._shape_m)

    @property
    def height(self):
        return self._shape_m[0]

    @property
    def width(self):
        return self._shape_m[1]

    @property
    def center(self):
        return np.array([self._shape_m[0] / 2, self._shape_m[1] / 2])

    @property
    def center_pixel(self):
        return np.array([self._shape[0] // 2, self._shape[1] // 2])

    @property
    def values(self):
        return self._values

    def __getitem__(self, key):
        idx = _prepare_index_vals(key, self._pixel_shape)
        return self._values[idx]

    def __setitem__(self, key, value):
        idx = _prepare_index_vals(key, self._pixel_shape)
        self._values[idx] = value
