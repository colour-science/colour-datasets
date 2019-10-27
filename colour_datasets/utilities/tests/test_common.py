# -*- coding: utf-8 -*-
"""
Defines unit tests for :mod:`colour_datasets.utilities.common` module.
"""

from __future__ import division, unicode_literals

import os
import unittest
import tempfile
import shutil

from colour_datasets.loaders import build_Labsphere2019
from colour_datasets.utilities import (hash_md5, url_download, json_open,
                                       unpack_gzipfile)

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = [
    'TestHashMd5', 'TestUrlDownload', 'TestJsonOpen', 'TestUnpackGzipfile'
]


class TestHashMd5(unittest.TestCase):
    """
    Defines :func:`colour_datasets.utilities.common.hash_md5` definition unit
    tests methods.
    """

    def test_hash_md5(self):
        """
        Tests :func:`colour_datasets.utilities.common.hash_md5` definition.
        """

        dataset = build_Labsphere2019()
        dataset.load()

        self.assertEqual(
            hash_md5(
                os.path.join(dataset.record.repository, 'dataset',
                             'SRS-99-020.txt')),
            '7c7a7b76c399e5c4e3afbd32e22b2b2e')

        self.assertEqual(
            hash_md5(
                os.path.join(dataset.record.repository, 'dataset',
                             'SRS-99-020.txt'),
                chunk_size=8), '7c7a7b76c399e5c4e3afbd32e22b2b2e')


class TestUrlDownload(unittest.TestCase):
    """
    Defines :func:`colour_datasets.utilities.common.url_download` definition
    unit tests methods.
    """

    def setUp(self):
        """
        Initialises common tests attributes.
        """

        self._temporary_file = tempfile.mktemp()

    def tearDown(self):
        """
        After tests actions.
        """

        os.remove(self._temporary_file)

    def test_url_download(self):
        """
        Tests :func:`colour_datasets.utilities.common.url_download` definition.
        """

        dataset = build_Labsphere2019()
        dataset.load()

        md5 = hash_md5(
            os.path.join(dataset.record.repository, 'dataset',
                         'SRS-99-020.txt'))
        url_download(
            'https://zenodo.org/api/files/a1f87\
ae9-bf9b-4451-becd-b4b3d7e35cc5/SRS-99-020.txt', self._temporary_file)

        self.assertEqual(md5, hash_md5(self._temporary_file))

        url_download(
            'https://zenodo.org/api/files/a1f87\
ae9-bf9b-4451-becd-b4b3d7e35cc5/SRS-99-020.txt', self._temporary_file, md5)

        self.assertRaises(
            IOError, lambda: url_download('https://nemo.io', self.
                                          _temporary_file))
        self.assertRaises(
            ValueError, lambda: url_download(
                'https://zenodo.org/api/files/a1f87\
ae9-bf9b-4451-becd-b4b3d7e35cc5/SRS-99-020.txt', self._temporary_file,
                '7c7a7b76c399e5c4e3afbd32e22b2b2f'))


class TestJsonOpen(unittest.TestCase):
    """
    Defines :func:`colour_datasets.utilities.common.json_open` definition
    unit tests methods.
    """

    def test_json_open(self):
        """
        Tests :func:`colour_datasets.utilities.common.json_open` definition.
        """

        data = json_open('https://zenodo.org/api/records/3245883')

        self.assertEqual(data['id'], 3245883)

        self.assertRaises(IOError, lambda: json_open('https://nemo.io'))


class TestUnpackGzipfile(unittest.TestCase):
    """
    Defines :func:`colour_datasets.utilities.common.unpack_gzipfile` definition
    unit tests methods.
    """

    def setUp(self):
        """
        Initialises common tests attributes.
        """

        self._temporary_directory = tempfile.mkdtemp()

    def tearDown(self):
        """
        After tests actions.
        """

        shutil.rmtree(self._temporary_directory)

    def test_unpack_gzipfile(self):
        """
        Tests :func:`colour_datasets.utilities.common.unpack_gzipfile`
        definition.
        """

        unpack_gzipfile(
            os.path.join(
                os.path.dirname(__file__), 'resources', 'example.txt.gz'),
            self._temporary_directory)

        with open(os.path.join(self._temporary_directory,
                               'example.txt')) as file_handle:
            self.assertEqual(
                file_handle.read(),
                'This is the content of a text file stored '
                'inside a "GZIP" file.')


if __name__ == '__main__':
    unittest.main()
