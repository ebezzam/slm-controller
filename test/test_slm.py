from slm_controller.slm import SLM


dim = 10
s = SLM(shape=(dim, dim), cell_dim=(1, 1))


class TestSLMIndexing:
    """
    Test :py:module:`~slm_controller.slm.SLM`.
    """

    def test_row_indexing(self):
        # single row
        val = s[3.5]
        assert val.shape == (3, dim)
        val = s[3.5, :]
        assert val.shape == (3, dim)

        # get a few rows
        val = s[1.5:4]
        assert val.shape == (3, 3, dim)
        val = s[:4.5]
        assert val.shape == (3, 4, dim)
        val = s[4.5:]
        assert val.shape == (3, 6, dim)

    def test_col_indexing(self):
        # single column
        val = s[:, 3.5]
        assert val.shape == (3, dim)

        # get a few columns
        val = s[:, 1.5:4]
        assert val.shape == (3, dim, 3)
        val = s[:, :4.5]
        assert val.shape == (3, dim, 4)
        val = s[:, 4.5:]
        assert val.shape == (3, dim, 6)
