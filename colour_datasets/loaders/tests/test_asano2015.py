# -*- coding: utf-8 -*-
"""
Defines unit tests for :mod:`colour_datasets.loaders.asano2015` module.
"""

from __future__ import division, unicode_literals

import numpy as np
import unittest

from colour import SpectralShape

from colour_datasets.loaders import Asano2015DatasetLoader, build_Asano2015

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['TestAsano2015DatasetLoader', 'TestBuildAsano2015']


class TestAsano2015DatasetLoader(unittest.TestCase):
    """
    Defines :class:`colour_datasets.loaders.asano2015.Asano2015DatasetLoader`
    class unit tests methods.
    """

    def test_required_attributes(self):
        """
        Tests presence of required attributes.
        """

        required_attributes = ('ID', )

        for attribute in required_attributes:
            self.assertIn(attribute, dir(Asano2015DatasetLoader))

    def test_required_methods(self):
        """
        Tests presence of required methods.
        """

        required_methods = ('load', 'parse_workbook_Asano2015')

        for method in required_methods:
            self.assertIn(method, dir(Asano2015DatasetLoader))

    def test_load(self):
        """
        Tests :func:`colour_datasets.loaders.asano2015.Asano2015DatasetLoader.\
load` method.
        """

        dataset = Asano2015DatasetLoader()
        self.assertEqual(
            sorted(dataset.load().keys()),
            ['Categorical Observers', 'Colour Normal Observers'])

        self.assertEqual(
            dataset.content['Categorical Observers'][1].XYZ_2.shape,
            SpectralShape(390, 780, 5))

        np.testing.assert_almost_equal(
            dataset.content['Categorical Observers'][1].XYZ_2[390],
            np.array([
                0.003774670254076,
                0.000033807427536,
                0.017705556255144,
            ]),
            decimal=7)

        np.testing.assert_almost_equal(
            dataset.content['Categorical Observers'][10].LMS_10[780],
            np.array([
                0.000101460310461,
                9.67131698024335e-06,
                0.000000000000000,
            ]),
            decimal=7)

        self.assertAlmostEqual(
            dataset.content['Categorical Observers']
            [5].parameters['Shift in S [nm]'],
            0.233255808,
            places=7)

        self.assertEqual(
            dataset.content['Colour Normal Observers'][1].XYZ_2.shape,
            SpectralShape(390, 780, 5))

        np.testing.assert_almost_equal(
            dataset.content['Colour Normal Observers'][1].XYZ_2[390],
            np.array([
                0.001627436785620,
                0.000021871064674,
                0.007492391403616,
            ]),
            decimal=7)

        np.testing.assert_almost_equal(
            dataset.content['Colour Normal Observers'][10].LMS_10[780],
            np.array([
                0.000092440377130,
                6.93870146211108e-06,
                0.000000000000000,
            ]),
            decimal=7)

        self.assertAlmostEqual(
            dataset.content['Colour Normal Observers']
            [5].parameters['Shift in S [nm]'],
            0.000649602695013,
            places=7)

        self.assertEqual(
            dataset.content['Colour Normal Observers'][151].others['Location'],
            'Darmstadt')


class TestBuildAsano2015(unittest.TestCase):
    """
    Defines :func:`colour_datasets.loaders.asano2015.build_Asano2015`
    definition unit tests methods.
    """

    def test_build_Asano2015(self):
        """
        Tests :func:`colour_datasets.loaders.asano2015.build_Asano2015`
        definition.
        """

        self.assertIs(build_Asano2015(), build_Asano2015())


if __name__ == '__main__':
    unittest.main()
