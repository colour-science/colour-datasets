# !/usr/bin/env python
"""
Define the unit tests for the :mod:`colour_datasets.loaders.winquist2022`
module.
"""

import unittest

import numpy as np

from colour_datasets.loaders import (
    DatasetLoader_Winquist2022,
    build_Winquist2022,
)

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestDatasetLoader_Winquist2022",
    "TestBuildWinquist2022",
]


class TestDatasetLoader_Winquist2022(unittest.TestCase):
    """
    Define
    :class:`colour_datasets.loaders.winquist2022.DatasetLoader_Winquist2022`
    class unit tests methods.
    """

    def test_required_attributes(self):
        """Test the presence of required attributes."""

        required_attributes = ("ID",)

        for attribute in required_attributes:
            self.assertIn(attribute, dir(DatasetLoader_Winquist2022))

    def test_required_methods(self):
        """Test the presence of required methods."""

        required_methods = ("__init__", "load")

        for method in required_methods:
            self.assertIn(method, dir(DatasetLoader_Winquist2022))

    def test_load(self):
        """
        Test
        :func:`colour_datasets.loaders.winquist2022.DatasetLoader_Winquist2022.\
load` method.
        """

        dataset = DatasetLoader_Winquist2022()
        self.assertEqual(len(dataset.load().keys()), 17)

        np.testing.assert_array_almost_equal(
            dataset.load()["Canon EOS_1DX_Mark_II"][555],
            np.array([0.27472975, 0.88354587, 0.08992765]),
            decimal=7,
        )


class TestBuildWinquist2022(unittest.TestCase):
    """
    Define :func:`colour_datasets.loaders.winquist2022.build_Winquist2022`
    definition unit tests methods.
    """

    def test_build_Winquist2022(self):
        """
        Test :func:`colour_datasets.loaders.winquist2022.build_Winquist2022`
        definition.
        """

        self.assertIs(build_Winquist2022(), build_Winquist2022())


if __name__ == "__main__":
    unittest.main()
