# -*- coding: utf-8 -*-
"""
Defines unit tests for :mod:`colour_datasets.records.configuration` module.
"""

from __future__ import division, unicode_literals

import unittest

from colour_datasets.records import Configuration, use_sandbox, sandbox

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['TestUseSandbox', 'TestSandbox']


class TestUseSandbox(unittest.TestCase):
    """
    Defines :func:`colour_datasets.records.configuration.use_sandbox`
    definition unit tests methods.
    """

    def tearDown(self):
        """
        After tests actions.
        """

        use_sandbox(False)

    def test_use_sandbox(self):
        """
        Tests :func:`colour_datasets.records.configuration.use_sandbox`
        definition.
        """

        self.assertEqual(Configuration().api_url, 'https://zenodo.org/api')
        use_sandbox()
        self.assertEqual(Configuration().api_url,
                         'https://sandbox.zenodo.org/api')
        use_sandbox(False)


class TestSandbox(unittest.TestCase):
    """
    Defines :func:`colour_datasets.records.configuration.sandbox`
    definition unit tests methods.
    """

    def test_sandbox(self):
        """
        Tests :func:`colour_datasets.records.configuration.sandbox`
        definition.
        """

        self.assertEqual(Configuration().api_url, 'https://zenodo.org/api')

        with sandbox():
            self.assertEqual(Configuration().api_url,
                             'https://sandbox.zenodo.org/api')

        with sandbox('https://www.colour-science.org', 'colour-science'):
            self.assertEqual(Configuration().api_url,
                             'https://www.colour-science.org')
            self.assertEqual(Configuration().community, 'colour-science')


if __name__ == '__main__':
    unittest.main()
