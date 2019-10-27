# -*- coding: utf-8 -*-
"""
Defines unit tests for :mod:`colour_datasets.loaders.xrite2016` module.
"""

from __future__ import division, unicode_literals

import unittest

from colour.characterisation import ColourChecker

from colour_datasets.loaders import XRite2016DatasetLoader, build_XRite2016

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['TestXRite2016DatasetLoader', 'TestBuildXRite2016']


class TestXRite2016DatasetLoader(unittest.TestCase):
    """
    Defines :class:`colour_datasets.loaders.xrite2016.XRite2016DatasetLoader`
    class unit tests methods.
    """

    def test_required_attributes(self):
        """
        Tests presence of required attributes.
        """

        required_attributes = ('ID', )

        for attribute in required_attributes:
            self.assertIn(attribute, dir(XRite2016DatasetLoader))

    def test_required_methods(self):
        """
        Tests presence of required methods.
        """

        required_methods = ('load', )

        for method in required_methods:
            self.assertIn(method, dir(XRite2016DatasetLoader))

    def test_load(self):
        """
        Tests :func:`colour_datasets.loaders.xrite2016.XRite2016DatasetLoader.\
load` method.
        """

        dataset = XRite2016DatasetLoader()
        self.assertEqual(
            sorted(dataset.load().keys()), [
                'ColorChecker24 - After November 2014',
                'ColorChecker24 - Before November 2014',
                'ColorCheckerSG - After November 2014',
                'ColorCheckerSG - Before November 2014',
            ])
        self.assertIsInstance(
            dataset.content['ColorChecker24 - After November 2014'],
            ColourChecker)


class TestBuildXRite2016(unittest.TestCase):
    """
    Defines :func:`colour_datasets.loaders.xrite2016.build_XRite2016`
    definition unit tests methods.
    """

    def test_build_XRite2016(self):
        """
        Tests :func:`colour_datasets.loaders.xrite2016.build_XRite2016`
        definition.
        """

        self.assertIs(build_XRite2016(), build_XRite2016())


if __name__ == '__main__':
    unittest.main()
