import pytest
from slm_controller.slm import SLM
from slm_controller.aperture import RectAperture


class TestAperture:
    """
    Test :py:module:`~slm_controller.aperture`.
    """

    def test_rect_aperture(self):
        slm_dim = (10, 10)
        pixel_shape = (0.18e-3, 0.18e-3)
        apert_dim = (2 * pixel_shape[0], 2 * pixel_shape[1])

        # create SLM
        slm = SLM(shape=slm_dim, pixel_shape=pixel_shape)

        # valid
        RectAperture(apert_dim=apert_dim, slm=slm)

        # invalid, outside SLM
        with pytest.raises(AssertionError, match="must lie within SLM dimensions"):
            RectAperture(apert_dim=apert_dim, slm=slm, center=(slm.height, slm.width))

        # aperture extends beyond
        with pytest.raises(ValueError, match="extends past valid SLM dimensions"):
            RectAperture(
                apert_dim=apert_dim,
                slm=slm,
                center=(slm.height - pixel_shape[0], slm.width - pixel_shape[1]),
            )
