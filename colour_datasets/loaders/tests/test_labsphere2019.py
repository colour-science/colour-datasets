# -*- coding: utf-8 -*-
"""
Defines unit tests for :mod:`colour_datasets.loaders.labsphere2019` module.
"""

from __future__ import division, unicode_literals

import unittest

from colour import SpectralShape

from colour_datasets.loaders import (Labsphere2019DatasetLoader,
                                     build_Labsphere2019)

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['TestLabsphere2019DatasetLoader', 'TestBuildLabsphere2019']


class TestLabsphere2019DatasetLoader(unittest.TestCase):
    """
    Defines :class:`colour_datasets.loaders.labsphere2019.\
Labsphere2019DatasetLoader` class unit tests methods.
    """

    def test_required_attributes(self):
        """
        Tests presence of required attributes.
        """

        required_attributes = ('ID', )

        for attribute in required_attributes:
            self.assertIn(attribute, dir(Labsphere2019DatasetLoader))

    def test_required_methods(self):
        """
        Tests presence of required methods.
        """

        required_methods = ('load', )

        for method in required_methods:
            self.assertIn(method, dir(Labsphere2019DatasetLoader))

    def test_load(self):
        """
        Tests :func:`colour_datasets.loaders.labsphere2019.\
Labsphere2019DatasetLoader.load` method.
        """

        dataset = Labsphere2019DatasetLoader()
        self.assertEqual(
            sorted(dataset.load().keys()), ['Labsphere SRS-99-020'])
        self.assertEqual(dataset.content['Labsphere SRS-99-020'].shape,
                         SpectralShape(250, 2500, 1))


class TestBuildLabsphere2019(unittest.TestCase):
    """
    Defines :func:`colour_datasets.loaders.labsphere2019.build_Labsphere2019`
    definition unit tests methods.
    """

    def test_build_Labsphere2019(self):
        """
        Tests :func:`colour_datasets.loaders.labsphere2019.build_Labsphere2019`
        definition.
        """

        self.assertIs(build_Labsphere2019(), build_Labsphere2019())


if __name__ == '__main__':
    unittest.main()
