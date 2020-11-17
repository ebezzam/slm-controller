import numpy as np
from slm_controller.util import _prepare_index_vals


class SLM:
    def __init__(self, shape, cell_dim, grayscale=False):
        """
        Class for defining SLM.

        Parameters
        ----------
        shape : tuple(int)
            (height, width) in number of cell.
        cell_dim : tuple(float)
            Cell dimensions (height, width) in meters.
        """
        assert np.all(shape) > 0
        assert np.all(cell_dim) > 0
        self._shape = shape
        self._cell_dim = cell_dim
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
    def cell_dim(self):
        return self._cell_dim

    @property
    def dim(self):
        return np.array(self._shape) * np.array(self._cell_dim)

    @property
    def height(self):
        return self._shape[0] * self._cell_dim[0]

    @property
    def width(self):
        return self._shape[1] * self._cell_dim[1]

    @property
    def center(self):
        return np.array([self.height / 2, self.width / 2])

    @property
    def center_cell(self):
        return np.array([self._shape[0] // 2, self._shape[1] // 2])

    @property
    def values(self):
        return self._values

    def __getitem__(self, key):
        idx = _prepare_index_vals(key, self._cell_dim)
        return self._values[idx]

    def __setitem__(self, key, value):
        idx = _prepare_index_vals(key, self._cell_dim)
        self._values[idx] = value
