# !/usr/bin/env python
"""Define the unit tests for the :mod:`colour_datasets.loaders.xrite2016` module."""

import unittest

from colour.characterisation import ColourChecker

from colour_datasets.loaders import DatasetLoader_XRite2016, build_XRite2016

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestDatasetLoader_XRite2016",
    "TestBuildXRite2016",
]


class TestDatasetLoader_XRite2016(unittest.TestCase):
    """
    Define :class:`colour_datasets.loaders.xrite2016.DatasetLoader_XRite2016`
    class unit tests methods.
    """

    def test_required_attributes(self):
        """Test the presence of required attributes."""

        required_attributes = ("ID",)

        for attribute in required_attributes:
            self.assertIn(attribute, dir(DatasetLoader_XRite2016))

    def test_required_methods(self):
        """Test the presence of required methods."""

        required_methods = ("__init__", "load")

        for method in required_methods:
            self.assertIn(method, dir(DatasetLoader_XRite2016))

    def test_load(self):
        """
        Test :func:`colour_datasets.loaders.xrite2016.\
DatasetLoader_XRite2016.load` method.
        """

        dataset = DatasetLoader_XRite2016()
        self.assertEqual(
            sorted(dataset.load().keys()),
            [
                "ColorChecker24 - After November 2014",
                "ColorChecker24 - Before November 2014",
                "ColorCheckerSG - After November 2014",
                "ColorCheckerSG - Before November 2014",
            ],
        )
        self.assertIsInstance(
            dataset.content["ColorChecker24 - After November 2014"],
            ColourChecker,
        )


class TestBuildXRite2016(unittest.TestCase):
    """
    Define :func:`colour_datasets.loaders.xrite2016.build_XRite2016`
    definition unit tests methods.
    """

    def test_build_XRite2016(self):
        """
        Test :func:`colour_datasets.loaders.xrite2016.build_XRite2016`
        definition.
        """

        self.assertIs(build_XRite2016(), build_XRite2016())


if __name__ == "__main__":
    unittest.main()
