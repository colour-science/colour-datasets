# -*- coding: utf-8 -*-
"""
Defines unit tests for :mod:`colour_datasets.loaders.jakob2019` module.
"""

from __future__ import division, unicode_literals

import unittest

from colour_datasets.loaders import DatasetLoader_Jakob2019, build_Jakob2019

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019-2020 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = ['TestDatasetLoader_Jakob2019', 'TestBuildJakob2019']


class TestDatasetLoader_Jakob2019(unittest.TestCase):
    """
    Defines :class:`colour_datasets.loaders.jakob2019.DatasetLoader_Jakob2019`
    class unit tests methods.
    """

    def test_required_attributes(self):
        """
        Tests presence of required attributes.
        """

        required_attributes = ('ID', )

        for attribute in required_attributes:
            self.assertIn(attribute, dir(DatasetLoader_Jakob2019))

    def test_required_methods(self):
        """
        Tests presence of required methods.
        """

        required_methods = ('__init__', 'load')

        for method in required_methods:
            self.assertIn(method, dir(DatasetLoader_Jakob2019))

    def test_load(self):
        """
        Tests :func:`colour_datasets.loaders.jakob2019.\
DatasetLoader_Jakob2019.load` method.
        """

        dataset = DatasetLoader_Jakob2019()
        self.assertEqual(
            sorted(dataset.load().keys()),
            ['ACES2065-1', 'ITU-R BT.2020', 'ProPhoto RGB', 'sRGB'])


class TestBuildJakob2019(unittest.TestCase):
    """
    Defines :func:`colour_datasets.loaders.jakob2019.build_Jakob2019`
    definition unit tests methods.
    """

    def test_build_Jakob2019(self):
        """
        Tests :func:`colour_datasets.loaders.jakob2019.build_Jakob2019`
        definition.
        """

        self.assertIs(build_Jakob2019(), build_Jakob2019())


if __name__ == '__main__':
    unittest.main()
