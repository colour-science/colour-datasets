# !/usr/bin/env python
"""Define the unit tests for the :mod:`colour_datasets.loaders.ebner1998` module."""

import unittest

import numpy as np

from colour_datasets.loaders import DatasetLoader_Ebner1998, build_Ebner1998

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestDatasetLoader_Ebner1998",
    "TestBuildEbner1998",
]


class TestDatasetLoader_Ebner1998(unittest.TestCase):
    """
    Define :class:`colour_datasets.loaders.ebner1998.DatasetLoader_Ebner1998`
    class unit tests methods.
    """

    def test_required_attributes(self):
        """Test the presence of required attributes."""

        required_attributes = ("ID",)

        for attribute in required_attributes:
            self.assertIn(attribute, dir(DatasetLoader_Ebner1998))

    def test_required_methods(self):
        """Test the presence of required methods."""

        required_methods = ("__init__", "load")

        for method in required_methods:
            self.assertIn(method, dir(DatasetLoader_Ebner1998))

    def test_load(self):
        """
        Test :func:`colour_datasets.loaders.ebner1998.\
DatasetLoader_Ebner1998.load` method.
        """

        dataset = DatasetLoader_Ebner1998()
        self.assertListEqual(
            sorted(dataset.load().keys()), ["Constant Perceived-Hue Data"]
        )

        self.assertListEqual(
            sorted(dataset.load()["Constant Perceived-Hue Data"].keys()),
            [
                0,
                24,
                48,
                72,
                96,
                120,
                144,
                168,
                192,
                216,
                240,
                264,
                288,
                312,
                336,
            ],
        )

        np.testing.assert_array_almost_equal(
            dataset.load()["Constant Perceived-Hue Data"][96].XYZ_r,
            np.array(
                [
                    0.950100000000000,
                    1.000000000000000,
                    1.088100000000000,
                ]
            ),
            decimal=7,
        )
        np.testing.assert_array_almost_equal(
            dataset.load()["Constant Perceived-Hue Data"][96].XYZ_cr,
            np.array(
                [
                    0.518400000000000,
                    0.566800000000000,
                    0.211200000000000,
                ]
            ),
            decimal=7,
        )
        np.testing.assert_array_almost_equal(
            dataset.load()["Constant Perceived-Hue Data"][96].XYZ_ct,
            np.array(
                [
                    [0.028909000000000, 0.029891000000000, 0.010142000000000],
                    [0.059861000000000, 0.062359000000000, 0.028395000000000],
                    [0.061870000000000, 0.062359000000000, 0.010384000000000],
                    [0.108221000000000, 0.112510000000000, 0.017582000000000],
                    [0.138453000000000, 0.145417000000000, 0.084043000000000],
                    [0.140725000000000, 0.145417000000000, 0.037708000000000],
                    [0.174718000000000, 0.184187000000000, 0.027642000000000],
                    [0.266956000000000, 0.281233000000000, 0.186195000000000],
                    [0.267106000000000, 0.281233000000000, 0.102615000000000],
                    [0.265222000000000, 0.281233000000000, 0.048764000000000],
                    [0.378172000000000, 0.407494000000000, 0.060499000000000],
                    [0.452991000000000, 0.482781000000000, 0.349471000000000],
                    [0.448363000000000, 0.482781000000000, 0.217887000000000],
                    [0.444752000000000, 0.482781000000000, 0.124260000000000],
                    [0.512315000000000, 0.566813000000000, 0.085942000000000],
                    [0.709748000000000, 0.763034000000000, 0.589282000000000],
                    [0.701174000000000, 0.763034000000000, 0.398412000000000],
                    [0.698154000000000, 0.763034000000000, 0.253302000000000],
                    [0.705383000000000, 0.763034000000000, 0.148054000000000],
                    [0.704427000000000, 0.763034000000000, 0.112490000000000],
                ]
            ),
            decimal=7,
        )


class TestBuildEbner1998(unittest.TestCase):
    """
    Define :func:`colour_datasets.loaders.ebner1998.build_Ebner1998`
    definition unit tests methods.
    """

    def test_build_Ebner1998(self):
        """
        Test :func:`colour_datasets.loaders.ebner1998.build_Ebner1998`
        definition.
        """

        self.assertIs(build_Ebner1998(), build_Ebner1998())


if __name__ == "__main__":
    unittest.main()
