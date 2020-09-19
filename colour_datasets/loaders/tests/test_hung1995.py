# -*- coding: utf-8 -*-
"""
Defines unit tests for :mod:`colour_datasets.loaders.hung1995` module.
"""

from __future__ import division, unicode_literals

import numpy as np
import unittest

from colour_datasets.loaders import DatasetLoader_Hung1995, build_Hung1995

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019-2020 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = ['TestDatasetLoader_Hung1995', 'TestBuildHung1995']


class TestDatasetLoader_Hung1995(unittest.TestCase):
    """
    Defines :class:`colour_datasets.loaders.hung1995.DatasetLoader_Hung1995`
    class unit tests methods.
    """

    def test_required_attributes(self):
        """
        Tests presence of required attributes.
        """

        required_attributes = ('ID', )

        for attribute in required_attributes:
            self.assertIn(attribute, dir(DatasetLoader_Hung1995))

    def test_required_methods(self):
        """
        Tests presence of required methods.
        """

        required_methods = ('__init__', 'load')

        for method in required_methods:
            self.assertIn(method, dir(DatasetLoader_Hung1995))

    def test_load(self):
        """
        Tests :func:`colour_datasets.loaders.hung1995.DatasetLoader_Hung1995.\
load` method.
        """

        dataset = DatasetLoader_Hung1995()
        self.assertListEqual(
            list(dataset.load().keys()), [
                'Table I', 'Table II', 'Table III', 'Table IV',
                'Constant Hue Loci Data - CL', 'Constant Hue Loci Data - VL'
            ])
        self.assertListEqual(
            list(dataset.load()['Constant Hue Loci Data - CL'].keys()), [
                'Red', 'Red-yellow', 'Yellow', 'Yellow-green', 'Green',
                'Green-cyan', 'Cyan', 'Cyan-blue', 'Blue', 'Blue-magenta',
                'Magenta', 'Magenta-red'
            ])

        np.testing.assert_almost_equal(
            dataset.load()['Constant Hue Loci Data - CL']['Cyan'].XYZ_r,
            np.array([
                0.980705971659919,
                1.000000000000000,
                1.182249493927126,
            ]),
            decimal=7)
        np.testing.assert_almost_equal(
            dataset.load()['Constant Hue Loci Data - CL']['Cyan'].XYZ_cr,
            np.array([
                0.495450736980020,
                0.722700000000000,
                1.149029086144775,
            ]),
            decimal=7)
        np.testing.assert_almost_equal(
            dataset.load()['Constant Hue Loci Data - CL']['Cyan'].XYZ_ct,
            np.array(
                [[0.655100000000000, 0.722700000000000, 0.916200000000000], [
                    0.603500000000000, 0.722700000000000, 0.995100000000000
                ], [0.553100000000000, 0.722700000000000, 1.084400000000000],
                 [0.495500000000000, 0.722700000000000, 1.149100000000000]]),
            decimal=7)


class TestBuildHung1995(unittest.TestCase):
    """
    Defines :func:`colour_datasets.loaders.hung1995.build_Hung1995`
    definition unit tests methods.
    """

    def test_build_Hung1995(self):
        """
        Tests :func:`colour_datasets.loaders.hung1995.build_Hung1995`
        definition.
        """

        self.assertIs(build_Hung1995(), build_Hung1995())


if __name__ == '__main__':
    unittest.main()
