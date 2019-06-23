# -*- coding: utf-8 -*-
"""
Common Utilities
================

Defines common utilities objects that don't fall in any specific category.
"""

from __future__ import division, unicode_literals

import functools
import hashlib
import json
import os
import sys
from six.moves import urllib
from tqdm import tqdm

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = [
    'suppress_stdout', 'TqdmUpTo', 'hash_md5', 'url_download', 'json_open'
]


class suppress_stdout(object):
    """
    A context manager and decorator temporarily suppressing standard output.
    """

    def __enter__(self):
        """
        Called upon entering the context manager and decorator.
        """

        self._stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

        return self

    def __exit__(self, *args):
        """
        Called upon exiting the context manager and decorator.
        """

        sys.stdout.close()
        sys.stdout = self._stdout

    def __call__(self, function):
        """
        Calls the wrapped definition.
        """

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            with self:
                return function(*args, **kwargs)

        return wrapper


class TqdmUpTo(tqdm):
    """
    :class:`tqdm` sub-class used to report the progress of an action.
    """

    def update_to(self, chunks_count=1, chunk_size=1, total_size=None):
        """
        Reports the progress of an action.

        Parameters
        ----------
        chunks_count : int, optional
            Number of blocks transferred.
        chunk_size : int, optional
            Size of each block (in tqdm units).
        total_size : int, optional
            Total size (in tqdm units).
        """

        if total_size is not None:
            self.total = total_size

        self.update(chunks_count * chunk_size - self.n)


def hash_md5(filename, chunk_size=2 ** 16):
    """
    Computes the *Message Digest 5 (MD5)* hash of given file.

    Parameters
    ----------
    filename : unicode
        File to compute the *MD5* hash of.
    chunk_size : int, optional
        Chunk size to read from the file.

    Returns
    -------
    unicode
        *MD5* hash of given file.
    """

    md5 = hashlib.md5()

    with open(filename, 'rb') as file_object:
        while True:
            chunk = file_object.read(chunk_size)
            if not chunk:
                break

            md5.update(chunk)

    return md5.hexdigest()


def url_download(url, filename, md5=None, retries=3):
    """
    Downloads given url and saves its content at given file.

    Parameters
    ----------
    url : unicode
        Url to download.
    filename : unicode
        File to save the url content at.
    md5 : unicode, optional
        *Message Digest 5 (MD5)* hash of the content at given url. If provided
        the saved content at given file will be hashed and compared to ``md5``.
    retries : int, optional
        Number of retries in case where a networking error occurs or the *MD5*
        hash is not matching.

    Examples
    --------
    >>> import os
    >>> url_download(
    ...     'https://github.com/colour-science/colour-datasets', os.devnull)
    """

    attempt = 0
    while attempt != retries:
        try:
            with TqdmUpTo(
                    unit='B',
                    unit_scale=True,
                    miniters=1,
                    desc='Downloading "{0}" file'.format(
                        url.split('/')[-1])) as progress:
                urllib.request.urlretrieve(
                    url,
                    filename=filename,
                    reporthook=progress.update_to,
                    data=None)

            if md5 is not None:
                if md5.lower() != hash_md5(filename):
                    raise ValueError(
                        '"MD5" hash of "{0}" file '
                        'does not match the expected hash!'.format(filename))

            attempt = retries
        except (urllib.error.URLError, IOError, ValueError) as error:
            attempt += 1
            print('An error occurred while downloading "{0}" file '
                  'during attempt {1}, retrying...'.format(filename, attempt))
            if attempt == retries:
                raise error


def json_open(url, retries=3):
    """
    Opens given url and return its content as "JSON".

    Parameters
    ----------
    url : unicode
        Url to open.
    retries : int, optional
        Number of retries in case where a networking error occurs.

    Examples
    --------
    # Doctests skip for Python 2.x compatibility.
    >>> json_open('https://zenodo.org/api/records/3245883')[:38]
    ... # doctest: +SKIP
    '{"conceptdoi":"10.5281/zenodo.3245882"'
    """

    attempt = 0
    while attempt != retries:
        try:
            return json.loads(urllib.request.urlopen(url).read())

            attempt = retries
        except (urllib.error.URLError, IOError, ValueError) as error:
            attempt += 1
            print('An error occurred while opening "{0}" url '
                  'during attempt {1}, retrying...'.format(url, attempt))
            if attempt == retries:
                raise error