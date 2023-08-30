# !/usr/bin/env python
"""Define the unit tests for the :mod:`colour_datasets.loaders.abstract` module."""

import unittest

from colour_datasets.loaders import AbstractDatasetLoader

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestAbstractDatasetLoader",
]


class TestAbstractDatasetLoader(unittest.TestCase):
    """
    Define :class:`colour_datasets.loaders.abstract.AbstractDatasetLoader`
    class unit tests methods.
    """

    def test_required_attributes(self):
        """Test the presence of required attributes."""

        required_attributes = ("ID", "record", "id", "content")

        for attribute in required_attributes:
            self.assertIn(attribute, dir(AbstractDatasetLoader))

    def test_required_methods(self):
        """Test the presence of required methods."""

        required_methods = ("__init__", "load", "sync")

        for method in required_methods:
            self.assertIn(method, dir(AbstractDatasetLoader))


if __name__ == "__main__":
    unittest.main()
