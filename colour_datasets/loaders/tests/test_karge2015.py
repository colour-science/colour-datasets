# !/usr/bin/env python
"""Define the unit tests for the :mod:`colour_datasets.loaders.karge2015` module."""

import unittest

from colour import SpectralShape

from colour_datasets.loaders import DatasetLoader_Karge2015, build_Karge2015

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestDatasetLoader_Karge2015",
    "TestBuildKarge2015",
]


class TestDatasetLoader_Karge2015(unittest.TestCase):
    """
    Define :class:`colour_datasets.loaders.karge2015.DatasetLoader_Karge2015`
    class unit tests methods.
    """

    def test_required_attributes(self):
        """Test the presence of required attributes."""

        required_attributes = ("ID",)

        for attribute in required_attributes:
            self.assertIn(attribute, dir(DatasetLoader_Karge2015))

    def test_required_methods(self):
        """Test the presence of required methods."""

        required_methods = ("__init__", "load")

        for method in required_methods:
            self.assertIn(method, dir(DatasetLoader_Karge2015))

    def test_load(self):
        """
        Test :func:`colour_datasets.loaders.karge2015.\
DatasetLoader_Karge2015.load` method.
        """

        dataset = DatasetLoader_Karge2015()
        self.assertEqual(
            sorted(dataset.load().keys()),
            [
                "Arri HMI",
                "Arri LED",
                "Arri TU",
                "Bron Kobold FL",
                "Bron Kobold HMI",
                "CMT Kinoflo FL",
                "Dedolight TU",
            ],
        )
        self.assertEqual(
            dataset.content["Arri HMI"]["Raw"][
                "Arri_Compact125W_HMI_Spot"
            ].shape,
            SpectralShape(380, 780, 4),
        )


class TestBuildKarge2015(unittest.TestCase):
    """
    Define :func:`colour_datasets.loaders.karge2015.build_Karge2015`
    definition unit tests methods.
    """

    def test_build_Karge2015(self):
        """
        Test :func:`colour_datasets.loaders.karge2015.build_Karge2015`
        definition.
        """

        self.assertIs(build_Karge2015(), build_Karge2015())


if __name__ == "__main__":
    unittest.main()
