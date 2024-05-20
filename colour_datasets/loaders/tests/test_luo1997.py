"""Define the unit tests for the :mod:`colour_datasets.loaders.luo1997` module."""


import numpy as np
from colour.constants import TOLERANCE_ABSOLUTE_TESTS

from colour_datasets.loaders import DatasetLoader_Luo1997, build_Luo1997

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestDatasetLoader_Luo1997",
    "TestBuildLuo1997",
]


class TestDatasetLoader_Luo1997:
    """
    Define :class:`colour_datasets.loaders.luo1997.DatasetLoader_Luo1997`
    class unit tests methods.
    """

    def test_required_attributes(self):
        """Test the presence of required attributes."""

        required_attributes = ("ID",)

        for attribute in required_attributes:
            assert attribute in dir(DatasetLoader_Luo1997)

    def test_required_methods(self):
        """Test the presence of required methods."""

        required_methods = ("__init__", "load")

        for method in required_methods:
            assert method in dir(DatasetLoader_Luo1997)

    def test_load(self):
        """
        Test :func:`colour_datasets.loaders.luo1997.DatasetLoader_Luo1997.\
load` method.
        """

        dataset = DatasetLoader_Luo1997()
        assert len(dataset.load().keys()) == 8

        np.testing.assert_allclose(
            dataset.content["R-HL"].phases["1"].JQCH_v,
            np.array(
                [
                    [56.16667000, 57.86961000, 196.66670000],
                    [54.50000000, 47.84477000, 222.66670000],
                    [44.66667000, 59.75408000, 209.16670000],
                    [39.33333000, 60.04782000, 217.50000000],
                    [51.16667000, 70.94367000, 190.00000000],
                    [57.66667000, 57.94122000, 193.33330000],
                    [47.00000000, 52.76572000, 219.16670000],
                    [48.16667000, 46.68655000, 271.66670000],
                    [40.83333000, 49.02215000, 270.83330000],
                    [41.33333000, 56.26083000, 295.00000000],
                    [69.50000000, 47.90268000, 172.50000000],
                    [57.83333000, 58.76534000, 184.16670000],
                    [66.83334000, 33.28886000, 190.00000000],
                    [52.66667000, 38.72170000, 186.66670000],
                    [47.33333000, 50.98633000, 189.16670000],
                    [69.16666000, 31.70590000, 214.16670000],
                    [59.66667000, 29.39379000, 219.16670000],
                    [43.16667000, 40.31440000, 218.33330000],
                    [22.83333000, 32.29254000, 242.50000000],
                    [22.83333000, 44.26646000, 285.00000000],
                    [54.83333000, 45.02808000, 300.83330000],
                    [46.83333000, 56.90472000, 302.16670000],
                    [20.83333000, 40.13494000, 302.16670000],
                    [13.83333000, 24.78231000, 201.66670000],
                    [76.50000000, 19.74625000, 257.50000000],
                    [50.00000000, 32.07797000, 240.00000000],
                    [37.16667000, 36.46753000, 217.50000000],
                    [71.66666000, 24.01473000, 296.66670000],
                    [46.33333000, 34.97781000, 287.50000000],
                    [37.66667000, 34.27040000, 277.50000000],
                    [53.33333000, 39.96097000, 301.66670000],
                    [40.50000000, 45.44844000, 303.33330000],
                    [69.50000000, 27.82081000, 162.50000000],
                    [53.66667000, 42.07102000, 170.00000000],
                    [44.16667000, 46.79108000, 180.83330000],
                    [73.83334000, 19.88776000, 173.33330000],
                    [55.50000000, 30.71196000, 186.66670000],
                    [45.50000000, 36.97079000, 177.33330000],
                    [70.66666000, 59.04763000, 125.00000000],
                    [23.16667000, 42.69704000, 306.33330000],
                    [84.33334000, 2.30505800, 279.16670000],
                    [62.66667000, 2.41827100, 278.33330000],
                    [49.33333000, 1.41421400, 253.33330000],
                    [36.33333000, 1.84931100, 176.66670000],
                    [45.66667000, 2.66716800, 125.00000000],
                    [10.00000000, 1.76273400, 225.00000000],
                    [79.33334000, 12.37990000, 320.33330000],
                    [52.83333000, 23.06538000, 321.16670000],
                    [41.16667000, 21.36245000, 321.66670000],
                    [11.16667000, 12.03591000, 324.16670000],
                    [53.16667000, 40.98200000, 318.33330000],
                    [40.00000000, 42.85206000, 318.83330000],
                    [69.50000000, 69.00055000, 94.33334000],
                    [49.83333000, 44.36057000, 121.66670000],
                    [69.33334000, 26.66056000, 112.50000000],
                    [52.00000000, 35.99024000, 132.50000000],
                    [45.83333000, 43.28527000, 116.66670000],
                    [58.50000000, 22.26538000, 91.66666000],
                    [58.33333000, 29.67985000, 111.66670000],
                    [46.00000000, 38.75251000, 123.33330000],
                    [75.00000000, 13.83745000, 76.66666000],
                    [52.66667000, 16.61791000, 76.66666000],
                    [44.16667000, 24.49417000, 84.16666000],
                    [51.16667000, 38.33792000, 346.66670000],
                    [42.50000000, 43.69113000, 340.00000000],
                    [17.00000000, 19.72399000, 349.16670000],
                    [49.66667000, 43.38010000, 335.00000000],
                    [20.83333000, 31.47086000, 327.50000000],
                    [69.16666000, 66.55367000, 91.66666000],
                    [53.66667000, 55.06004000, 75.83334000],
                    [54.66667000, 29.65701000, 52.16667000],
                    [47.33333000, 36.25274000, 61.66667000],
                    [75.00000000, 25.63061000, 393.66670000],
                    [44.00000000, 29.60447000, 381.66670000],
                    [21.33333000, 29.10929000, 16.66667000],
                    [75.66666000, 18.72404000, 391.66670000],
                    [51.50000000, 39.52409000, 379.16670000],
                    [40.00000000, 42.19035000, 377.00000000],
                    [13.66667000, 27.50569000, 379.16670000],
                    [51.33333000, 52.31194000, 363.33330000],
                    [43.83333000, 51.12469000, 360.83330000],
                    [19.66667000, 27.04408000, 359.16670000],
                    [70.00000000, 66.52412000, 86.66666000],
                    [69.33334000, 47.00951000, 58.33333000],
                    [56.50000000, 54.37062000, 55.00000000],
                    [41.16667000, 51.48495000, 63.33333000],
                    [73.50000000, 26.70713000, 3.83333300],
                    [58.50000000, 35.39288000, 1.66666700],
                    [47.66667000, 44.30476000, 28.33333000],
                    [41.66667000, 49.40073000, 32.50000000],
                    [22.16667000, 43.22822000, 11.66667000],
                    [44.50000000, 57.09751000, 373.83330000],
                    [51.83333000, 49.52876000, 388.33330000],
                    [29.83333000, 50.95493000, 380.83330000],
                    [46.83333000, 56.68077000, 381.66670000],
                    [51.66667000, 66.77108000, 50.00000000],
                    [53.83333000, 69.32430000, 43.33333000],
                    [43.66667000, 62.93172000, 33.66667000],
                    [54.50000000, 49.32152000, 26.66667000],
                    [46.16667000, 67.57368000, 17.00000000],
                    [35.33333000, 59.85252000, 403.00000000],
                    [45.66667000, 75.18921000, 20.00000000],
                    [43.83333000, 70.55120000, 399.16670000],
                    [45.50000000, 71.89995000, 395.33330000],
                    [45.66667000, 61.23224000, 387.50000000],
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        assert (
            dataset.content["R-HL"].metadata["Description of each data group"]
            == "Reflective media with luminances ranging 364-232 cd/m2"
        )


class TestBuildLuo1997:
    """
    Define :func:`colour_datasets.loaders.luo1997.build_Luo1997`
    definition unit tests methods.
    """

    def test_build_Luo1997(self):
        """
        Test :func:`colour_datasets.loaders.luo1997.build_Luo1997`
        definition.
        """

        assert build_Luo1997() is build_Luo1997()
