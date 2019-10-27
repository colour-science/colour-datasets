# -*- coding: utf-8 -*-
"""
Defines unit tests for :mod:`colour_datasets.loaders.jiang2013` module.
"""

from __future__ import division, unicode_literals

import unittest

from colour import SpectralShape

from colour_datasets.loaders import Jiang2013DatasetLoader, build_Jiang2013

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['TestJiang2013DatasetLoader', 'TestBuildJiang2013']


class TestJiang2013DatasetLoader(unittest.TestCase):
    """
    Defines :class:`colour_datasets.loaders.jiang2013.Jiang2013DatasetLoader`
    class unit tests methods.
    """

    def test_required_attributes(self):
        """
        Tests presence of required attributes.
        """

        required_attributes = ('ID', )

        for attribute in required_attributes:
            self.assertIn(attribute, dir(Jiang2013DatasetLoader))

    def test_required_methods(self):
        """
        Tests presence of required methods.
        """

        required_methods = ('load', )

        for method in required_methods:
            self.assertIn(method, dir(Jiang2013DatasetLoader))

    def test_load(self):
        """
        Tests :func:`colour_datasets.loaders.jiang2013.Jiang2013DatasetLoader.\
load` method.
        """

        dataset = Jiang2013DatasetLoader()
        self.assertEqual(
            sorted(dataset.load().keys()), [
                'Canon 1DMarkIII', 'Canon 20D', 'Canon 300D', 'Canon 40D',
                'Canon 500D', 'Canon 50D', 'Canon 5DMarkII', 'Canon 600D',
                'Canon 60D', 'Hasselblad H2', 'Nikon D200', 'Nikon D3',
                'Nikon D300s', 'Nikon D3X', 'Nikon D40', 'Nikon D50',
                'Nikon D5100', 'Nikon D700', 'Nikon D80', 'Nikon D90',
                'Nokia N900', 'Olympus E-PL2', 'Pentax K-5', 'Pentax Q',
                'Phase One', 'Point Grey Grasshopper 50S5C',
                'Point Grey Grasshopper2 14S5C', 'SONY NEX-5N'
            ])
        self.assertEqual(dataset.content['Canon 1DMarkIII'].shape,
                         SpectralShape(400, 720, 10))


class TestBuildJiang2013(unittest.TestCase):
    """
    Defines :func:`colour_datasets.loaders.jiang2013.build_Jiang2013`
    definition unit tests methods.
    """

    def test_build_Jiang2013(self):
        """
        Tests :func:`colour_datasets.loaders.jiang2013.build_Jiang2013`
        definition.
        """

        self.assertIs(build_Jiang2013(), build_Jiang2013())


if __name__ == '__main__':
    unittest.main()
