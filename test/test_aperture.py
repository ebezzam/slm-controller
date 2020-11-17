import pytest
from slm_controller.slm import SLM
from slm_controller.aperture import create_rect_aperture


class TestAperture:
    """
    Test :py:module:`~slm_controller.aperture`.
    """

    def test_rect_aperture(self):
        slm_shape = (10, 10)
        cell_dim = (0.18e-3, 0.18e-3)
        apert_dim = (2 * cell_dim[0], 2 * cell_dim[1])

        # valid
        create_rect_aperture(slm_shape=slm_shape, cell_dim=cell_dim, apert_dim=apert_dim)

        # invalid, outside SLM
        slm = SLM(shape=slm_shape, cell_dim=cell_dim)
        with pytest.raises(AssertionError, match="must lie within SLM dimensions"):
            create_rect_aperture(
                slm_shape=slm_shape,
                cell_dim=cell_dim,
                apert_dim=apert_dim,
                center=(slm.height, slm.width),
            )

        # aperture extends beyond
        with pytest.raises(ValueError, match="extends past valid SLM dimensions"):
            create_rect_aperture(
                slm_shape=slm_shape,
                cell_dim=cell_dim,
                apert_dim=apert_dim,
                center=(slm.height - cell_dim[0], slm.width - cell_dim[1]),
            )
