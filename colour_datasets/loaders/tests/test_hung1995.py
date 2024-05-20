"""Define the unit tests for the :mod:`colour_datasets.loaders.hung1995` module."""


import numpy as np
from colour.constants import TOLERANCE_ABSOLUTE_TESTS

from colour_datasets.loaders import DatasetLoader_Hung1995, build_Hung1995

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestDatasetLoader_Hung1995",
    "TestBuildHung1995",
]


class TestDatasetLoader_Hung1995:
    """
    Define :class:`colour_datasets.loaders.hung1995.DatasetLoader_Hung1995`
    class unit tests methods.
    """

    def test_required_attributes(self):
        """Test the presence of required attributes."""

        required_attributes = ("ID",)

        for attribute in required_attributes:
            assert attribute in dir(DatasetLoader_Hung1995)

    def test_required_methods(self):
        """Test the presence of required methods."""

        required_methods = ("__init__", "load")

        for method in required_methods:
            assert method in dir(DatasetLoader_Hung1995)

    def test_load(self):
        """
        Test :func:`colour_datasets.loaders.hung1995.DatasetLoader_Hung1995.\
load` method.
        """

        dataset = DatasetLoader_Hung1995()
        assert list(dataset.load().keys()) == [
            "Table I",
            "Table II",
            "Table III",
            "Table IV",
            "Constant Hue Loci Data - CL",
            "Constant Hue Loci Data - VL",
        ]
        assert list(dataset.load()["Constant Hue Loci Data - CL"].keys()) == [
            "Red",
            "Red-yellow",
            "Yellow",
            "Yellow-green",
            "Green",
            "Green-cyan",
            "Cyan",
            "Cyan-blue",
            "Blue",
            "Blue-magenta",
            "Magenta",
            "Magenta-red",
        ]

        np.testing.assert_allclose(
            dataset.load()["Constant Hue Loci Data - CL"]["Cyan"].XYZ_r,
            np.array(
                [
                    0.980705971659919,
                    1.000000000000000,
                    1.182249493927126,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )
        np.testing.assert_allclose(
            dataset.load()["Constant Hue Loci Data - CL"]["Cyan"].XYZ_cr,
            np.array(
                [
                    0.495450736980020,
                    0.722700000000000,
                    1.149029086144775,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )
        np.testing.assert_allclose(
            dataset.load()["Constant Hue Loci Data - CL"]["Cyan"].XYZ_ct,
            np.array(
                [
                    [0.655100000000000, 0.722700000000000, 0.916200000000000],
                    [0.603500000000000, 0.722700000000000, 0.995100000000000],
                    [0.553100000000000, 0.722700000000000, 1.084400000000000],
                    [0.495500000000000, 0.722700000000000, 1.149100000000000],
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )


class TestBuildHung1995:
    """
    Define :func:`colour_datasets.loaders.hung1995.build_Hung1995`
    definition unit tests methods.
    """

    def test_build_Hung1995(self):
        """
        Test :func:`colour_datasets.loaders.hung1995.build_Hung1995`
        definition.
        """

        assert build_Hung1995() is build_Hung1995()
