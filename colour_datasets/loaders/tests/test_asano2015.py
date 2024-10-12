"""Define the unit tests for the :mod:`colour_datasets.loaders.asano2015` module."""


import numpy as np
from colour import SpectralShape
from colour.constants import TOLERANCE_ABSOLUTE_TESTS

from colour_datasets.loaders import DatasetLoader_Asano2015, build_Asano2015

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestDatasetLoader_Asano2015",
    "TestBuildAsano2015",
]


class TestDatasetLoader_Asano2015:
    """
    Define :class:`colour_datasets.loaders.asano2015.DatasetLoader_Asano2015`
    class unit tests methods.
    """

    def test_required_attributes(self):
        """Test the presence of required attributes."""

        required_attributes = ("ID",)

        for attribute in required_attributes:
            assert attribute in dir(DatasetLoader_Asano2015)

    def test_required_methods(self):
        """Test the presence of required methods."""

        required_methods = ("__init__", "load", "parse_workbook_Asano2015")

        for method in required_methods:
            assert method in dir(DatasetLoader_Asano2015)

    def test_load(self):
        """
        Test :func:`colour_datasets.loaders.asano2015.\
DatasetLoader_Asano2015.load` method.
        """

        dataset = DatasetLoader_Asano2015()
        assert sorted(dataset.load().keys()) == [
            "Categorical Observers",
            "Colour Normal Observers",
        ]

        assert dataset.content["Categorical Observers"][1].XYZ_2.shape == SpectralShape(
            390, 780, 5
        )

        np.testing.assert_allclose(
            dataset.content["Categorical Observers"][1].XYZ_2[390],
            np.array(
                [
                    0.003774670254076,
                    0.000033807427536,
                    0.017705556255144,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            dataset.content["Categorical Observers"][10].LMS_10[780],
            np.array(
                [
                    0.000101460310461,
                    9.67131698024335e-06,
                    0.000000000000000,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            dataset.content["Categorical Observers"][5].parameters["Shift in S [nm]"],
            0.233255808,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        assert dataset.content["Colour Normal Observers"][
            1
        ].XYZ_2.shape == SpectralShape(390, 780, 5)

        np.testing.assert_allclose(
            dataset.content["Colour Normal Observers"][1].XYZ_2[390],
            np.array(
                [
                    0.001627436785620,
                    0.000021871064674,
                    0.007492391403616,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            dataset.content["Colour Normal Observers"][10].LMS_10[780],
            np.array(
                [
                    0.000092440377130,
                    6.93870146211108e-06,
                    0.000000000000000,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            dataset.content["Colour Normal Observers"][5].parameters["Shift in S [nm]"],
            0.000649602695013,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        assert (
            dataset.content["Colour Normal Observers"][151].others["Location"]
            == "Darmstadt"
        )


class TestBuildAsano2015:
    """
    Define :func:`colour_datasets.loaders.asano2015.build_Asano2015`
    definition unit tests methods.
    """

    def test_build_Asano2015(self):
        """
        Test :func:`colour_datasets.loaders.asano2015.build_Asano2015`
        definition.
        """

        assert build_Asano2015() is build_Asano2015()
