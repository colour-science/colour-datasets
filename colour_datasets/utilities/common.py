"""
Common Utilities
================

Defines the common utilities objects that don't fall in any specific category.
"""

from __future__ import annotations

import functools
import gzip
import hashlib
import json
import os
import setuptools.archive_util
import shutil
import sys
import urllib.error
import urllib.request
from tqdm import tqdm
from cachetools import cached, TTLCache

from colour.hints import Any, Boolean, Callable, Dict, Integer, Optional

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "New BSD License - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "suppress_stdout",
    "TqdmUpTo",
    "hash_md5",
    "url_download",
    "json_open",
    "unpack_gzipfile",
]


class suppress_stdout:
    """A context manager and decorator temporarily suppressing standard output."""

    def __enter__(self) -> suppress_stdout:
        """Redirect the standard output upon entering the context manager."""

        self._stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

        return self

    def __exit__(self, *args: Any):
        """Restore the standard output upon exiting the context manager."""

        sys.stdout.close()
        sys.stdout = self._stdout

    def __call__(self, function: Callable) -> Callable:
        """Call the wrapped definition."""

        @functools.wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Callable:
            with self:
                return function(*args, **kwargs)

        return wrapper


class TqdmUpTo(tqdm):
    """:class:`tqdm` sub-class used to report the progress of an action."""

    def update_to(
        self,
        chunks_count: Integer = 1,
        chunk_size: Integer = 1,
        total_size: Optional[Integer] = None,
    ):
        """
        Report the progress of an action.

        Parameters
        ----------
        chunks_count
            Number of blocks transferred.
        chunk_size
            Size of each block (in tqdm units).
        total_size
            Total size (in tqdm units).
        """

        if total_size is not None:
            self.total = total_size

        self.update(chunks_count * chunk_size - self.n)


def hash_md5(filename: str, chunk_size: Integer = 2**16) -> str:
    """
    Compute the *Message Digest 5 (MD5)* hash of given file.

    Parameters
    ----------
    filename
        File to compute the *MD5* hash of.
    chunk_size
        Chunk size to read from the file.

    Returns
    -------
    :class:`str`
        *MD5* hash of given file.
    """

    md5 = hashlib.md5()

    with open(filename, "rb") as file_object:
        while True:
            chunk = file_object.read(chunk_size)
            if not chunk:
                break

            md5.update(chunk)

    return md5.hexdigest()


def url_download(
    url: str, filename: str, md5: Optional[str] = None, retries: Integer = 3
):
    """
    Download given url and saves its content at given file.

    Parameters
    ----------
    url
        Url to download.
    filename
        File to save the url content at.
    md5
        *Message Digest 5 (MD5)* hash of the content at given url. If provided
        the saved content at given file will be hashed and compared to ``md5``.
    retries
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
                unit="B",
                unit_scale=True,
                miniters=1,
                desc=f"Downloading \"{url.split('/')[-1]}\" file",
            ) as progress:
                urllib.request.urlretrieve(
                    url,
                    filename=filename,
                    reporthook=progress.update_to,
                    data=None,
                )

            if md5 is not None:
                if md5.lower() != hash_md5(filename):
                    raise ValueError(
                        f'"MD5" hash of "{filename}" file does not match the '
                        f"expected hash!"
                    )

            attempt = retries
        except (urllib.error.URLError, OSError, ValueError) as error:
            attempt += 1
            print(
                f'An error occurred while downloading "{filename}" file '
                f"during attempt {attempt}, retrying..."
            )
            if attempt == retries:
                raise error


@cached(cache=TTLCache(maxsize=256, ttl=300))
def json_open(url: str, retries: Integer = 3) -> Dict:
    """
    Open given url and return its content as *JSON*.

    Parameters
    ----------
    url
        Url to open.
    retries
        Number of retries in case where a networking error occurs.

    Returns
    -------
    :class:`dict`
        *JSON* data.

    Raises
    ------
    urllib.error.URLError, ValueError
        If the url cannot be opened or parsed as *JSON*.

    Notes
    -----
    -   The definition caches the request *JSON* output for 5 minutes.

    Examples
    --------
    # Doctests skip for Python 2.x compatibility.
    >>> json_open('https://zenodo.org/api/records/3245883')
    ... # doctest: +SKIP
    '{"conceptdoi":"10.5281/zenodo.3245882"'
    """

    data = {}

    attempt = 0
    while attempt != retries:
        try:
            return json.loads(urllib.request.urlopen(url).read())
        except (urllib.error.URLError, ValueError) as error:
            attempt += 1
            print(
                f'An error occurred while opening "{url}" url during attempt '
                f"{attempt}, retrying..."
            )
            if attempt == retries:
                raise error

    return data


def unpack_gzipfile(
    filename: str, extraction_directory: str, *args: Any
) -> Boolean:
    """
    Unpack given *GZIP* file to given extraction directory.

    Parameters
    ----------
    filename
        *GZIP* file to extract.
    extraction_directory
        Directory where to extract the *GZIP* file.

    Other Parameters
    ----------------
    args
        Arguments.

    Returns
    -------
    :class:`bool`
        Definition success.

    Notes
    -----
    -   This definition is used as an extra driver for
        :func:`setuptools.archive_util.unpack archive` definition.
    """

    extraction_path = os.path.join(
        extraction_directory, os.path.splitext(os.path.basename(filename))[0]
    )

    if not os.path.exists(extraction_directory):
        os.makedirs(extraction_directory)

    try:
        with gzip.open(filename) as gzip_file, open(
            extraction_path, "wb"
        ) as output_file:
            shutil.copyfileobj(gzip_file, output_file)
    except Exception as e:
        print(e)
        raise setuptools.archive_util.UnrecognizedFormat(
            f'{filename} is not a "GZIP" file!'
        )

    return True


setuptools.archive_util.extraction_drivers = (
    setuptools.archive_util.unpack_directory,
    setuptools.archive_util.unpack_zipfile,
    setuptools.archive_util.unpack_tarfile,
    unpack_gzipfile,
)
