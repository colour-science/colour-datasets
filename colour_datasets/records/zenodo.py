"""
Zenodo
======

Define the objects implementing support for a *Zenodo* community and its
records:

-   :class:`colour_datasets.Record`
-   :class:`colour_datasets.Community`
"""

from __future__ import annotations

import json
import os
import re
import shutil
import stat
import tempfile
import textwrap
import urllib
import urllib.error
from collections.abc import Mapping
from html.parser import HTMLParser
from pprint import pformat

import setuptools.archive_util
from colour.hints import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
)
from colour.utilities import optional, warning

from colour_datasets.records import Configuration
from colour_datasets.utilities import json_open, url_download

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "Record",
    "Community",
]


class Record:
    """
    Define an object storing a *Zenodo* record data and providing methods to
    sync it in a local repository.

    Parameters
    ----------
    data
        *Zenodo* record data.
    configuration
        *Colour - Datasets* configuration.

    Attributes
    ----------
    -   :attr:`colour_datasets.Record.data`
    -   :attr:`colour_datasets.Record.configuration`
    -   :attr:`colour_datasets.Record.repository`
    -   :attr:`colour_datasets.Record.id`
    -   :attr:`colour_datasets.Record.title`

    Methods
    -------
    -   :meth:`colour_datasets.Record.__init__`
    -   :meth:`colour_datasets.Record.__str__`
    -   :meth:`colour_datasets.Record.__repr__`
    -   :meth:`colour_datasets.Record.from_id`
    -   :meth:`colour_datasets.Record.synced`
    -   :meth:`colour_datasets.Record.pull`
    -   :meth:`colour_datasets.Record.remove`

    Examples
    --------
    >>> record = Record(json_open("https://zenodo.org/api/records/3245883"))
    >>> record.id
    '3245883'
    >>> record.title
    'Camera Spectral Sensitivity Database - Jiang et al. (2013)'
    """

    def __init__(self, data: dict, configuration: Configuration | None = None) -> None:
        self._data: dict = data
        self._configuration: Configuration = optional(configuration, Configuration())

    @property
    def data(self) -> dict:
        """
        Getter property for the *Zenodo* record data.

        Returns
        -------
        :class:`dict`
            *Zenodo* record data.
        """

        return self._data

    @property
    def configuration(self) -> Configuration:
        """
        Getter property for the *Colour - Datasets* configuration.

        Returns
        -------
        :class:`colour_datasets.Configuration`
           *Colour - Datasets* configuration.
        """

        return self._configuration

    @property
    def repository(self) -> str:
        """
        Getter property for the *Zenodo* record local repository.

        Returns
        -------
        :class:`str`
            *Zenodo* record local repository.
        """

        return os.path.join(self._configuration.repository, self.id)

    @property
    def id(self) -> str:
        """
        Getter property for the *Zenodo* record id.

        Returns
        -------
        :class:`str`
            *Zenodo* record id.
        """

        return str(self._data["id"])

    @property
    def title(self) -> str:
        """
        Getter property for the *Zenodo* record title.

        Returns
        -------
        :class:`str`
            *Zenodo* record title.
        """

        return self._data["metadata"]["title"]

    def __str__(self) -> str:
        """
        Return a formatted string representation of the *Zenodo* record.

        Returns
        -------
        :class:`str`
            Formatted string representation.

        Examples
        --------
        >>> data = json_open("https://zenodo.org/api/records/3245883")
        >>> print("\\n".join(str(Record(data)).splitlines()[:4]))
        Camera Spectral Sensitivity Database - Jiang et al. (2013) - 1.0.0
        ==================================================================
        <BLANKLINE>
        Record ID        : 3245883
        """

        def strip_html(text: str) -> str:
            """Strip *HTML* tags from given text."""

            text = text.replace("&nbsp;", " ").replace("\n\n", " ")

            parts: List[str] = []
            parser = HTMLParser()
            parser.handle_data = parts.append  # pyright: ignore
            parser.feed(text)

            return "".join(parts)

        metadata = self._data["metadata"]
        authors = "; ".join([creator["name"] for creator in metadata["creators"]])
        files = self._data["files"]

        description = "\n".join(textwrap.wrap(strip_html(metadata["description"]), 79))

        files = "\n".join(
            [
                f'- {file_data["key"]} : {file_data["links"]["self"]}'
                for file_data in sorted(files, key=lambda x: x["key"])
            ]
        )

        representation = "\n".join(
            [
                f'{metadata["title"]} - {metadata["version"]}',
                f'{"=" * (len(self.title) + 3 + len(metadata["version"]))}',
                "",
                f"Record ID        : {self.id}",
                f"Authors          : {authors}",
                f'License          : {metadata["license"]["id"]}',
                f'DOI              : {metadata["doi"]}',
                f'Publication Date : {metadata["publication_date"]}',
                f'URL              : {self._data["links"]["self_html"]}\n',
                "Description",
                "-----------",
                "",
                f"{description}",
                "",
                "Files",
                "-----",
                "",
                f"{files}",
            ]
        )

        return representation

    def __repr__(self) -> str:
        """
        Return an evaluable string representation of the *Zenodo* record.

        Returns
        -------
        :class:`str`
            Evaluable string representation.

        Examples
        --------
        >>> data = json_open("https://zenodo.org/api/records/3245883")
        >>> print("\\n".join(repr(Record(data)).splitlines()[:4]))
        Record(
            {'conceptdoi': '10.5281/zenodo.3245882',
             'conceptrecid': '3245882',
             'created': '2019-06-14T09:34:15.765924+00:00',
        """

        data = "\n".join([f"    {line}" for line in pformat(self._data).splitlines()])

        configuration = "\n".join(
            [f"        {line}" for line in pformat(self._configuration).splitlines()]
        )
        configuration = f"    Configuration(\n{configuration}\n    )"

        return f"{self.__class__.__name__}(\n{data},\n{configuration}\n)"

    @staticmethod
    def from_id(
        id_: str,
        configuration: Configuration | None = None,
        retries: int = 3,
    ) -> Record:
        """
        :class:`colour_datasets.Record` class factory that builds an instance
        using given *Zenodo* record id.

        Parameters
        ----------
        id_
            *Zenodo* record id.
        configuration
            configuration
                *Colour - Datasets* configuration.
        retries
            Number of retries in case where a networking error occurs.

        Returns
        -------
        :class:`colour_datasets.Record`
            *Zenodo* record data.

        Examples
        --------
        >>> Record.from_id("3245883").title
        'Camera Spectral Sensitivity Database - Jiang et al. (2013)'
        """

        configuration = Configuration() if configuration is None else configuration

        if not os.path.exists(configuration.repository):
            os.makedirs(configuration.repository)

        record_url = f"{configuration.api_url}/records/{id_}"

        return Record(json_open(record_url, retries), configuration)

    def synced(self) -> bool:
        """
        Return whether the *Zenodo* record data is synced to the local
        repository.

        Returns
        -------
        :class:`bool`
            Whether the *Zenodo* record data is synced to the local repository.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> record = Record.from_id("3245883")
        >>> with suppress_stdout():
        ...     record.pull()
        >>> record.synced()
        True
        >>> record.remove()
        >>> record.synced()
        False
        """

        downloads_directory = os.path.join(
            self.repository, self._configuration.downloads_directory
        )
        deflate_directory = os.path.join(
            self.repository, self._configuration.deflate_directory
        )
        return all(
            [
                os.path.exists(downloads_directory),
                os.path.exists(deflate_directory),
            ]
        )

    def pull(self, use_urls_txt_file: bool = True, retries: int = 3):
        """
        Pull the *Zenodo* record data to the local repository.

        Parameters
        ----------
        use_urls_txt_file
            Whether to use the *urls.txt* file: if such a file is present in
            the *Zenodo* record data, the urls it defines take precedence over
            the record data files. The later will be used in the eventuality
            where the urls are not available.
        retries
            Number of retries in case where a networking error occurs or the
            *MD5* hash is not matching.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> record = Record.from_id("3245883")
        >>> record.remove()
        >>> with suppress_stdout():
        ...     record.pull()
        >>> record.synced()
        True
        """

        print(f'Pulling "{self.title}" record content...')  # noqa: T201

        if not os.path.exists(self._configuration.repository):
            os.makedirs(self._configuration.repository)

        downloads_directory = os.path.join(
            self.repository, self._configuration.downloads_directory
        )
        if not os.path.exists(downloads_directory):
            os.makedirs(downloads_directory)

        # As much as possible, the original file urls are used, those are
        # given by the content of :attr:`URLS_TXT_FILE` attribute file.
        urls_txt = None
        for file_data in self.data["files"]:
            if file_data["key"] == self._configuration.urls_txt_file:
                urls_txt = file_data
                break

        def urls_download(urls: Dict) -> None:
            """Download given urls."""

            for url, md5 in urls.items():
                filename = re.sub("/content$", "", url)
                filename = os.path.join(
                    downloads_directory,
                    urllib.parse.unquote(  # pyright: ignore
                        filename.split("/")[-1]
                    ),
                )
                url_download(url, filename, md5.split(":")[-1], retries)

        try:
            if use_urls_txt_file and urls_txt:
                urls = {}
                urls_txt_file = tempfile.NamedTemporaryFile(delete=False).name
                url_download(
                    urls_txt["links"]["self"],
                    urls_txt_file,
                    urls_txt["checksum"].split(":")[-1],
                    retries,
                )

                with open(urls_txt_file) as json_file:
                    urls_txt_json = json.load(json_file)
                    for url, md5 in urls_txt_json["urls"].items():
                        urls[url] = md5.split(":")[-1]

                shutil.copyfile(
                    urls_txt_file,
                    os.path.join(
                        downloads_directory, self._configuration.urls_txt_file
                    ),
                )

                urls_download(urls)
            else:
                raise ValueError(  # noqa: TRY301
                    f'"{self._configuration.urls_txt_file}" file was not '
                    f"found in record data!"
                )
        except (urllib.error.URLError, ValueError) as error:
            warning(
                f"An error occurred using urls from "
                f'"{self._configuration.urls_txt_file}" file: {error}\n'
                f"Switching to record urls..."
            )

            urls = {}
            for file_data in self.data["files"]:
                if file_data["key"] == self._configuration.urls_txt_file:
                    continue

                # TODO: Remove the following space escaping: The new Zenodo API
                # is not quoting filenames properly thus we are temporarily
                # escaping spaces for now.
                # https://github.com/colour-science/colour-datasets/issues/
                # 36#issuecomment-1773464695
                url = file_data["links"]["self"].replace(" ", "%20")

                urls[url] = file_data["checksum"].split(":")[-1]

            urls_download(urls)

        deflate_directory = os.path.join(
            self.repository, self._configuration.deflate_directory
        )
        if os.path.exists(deflate_directory):
            shutil.rmtree(deflate_directory, onerror=_remove_readonly)

        shutil.copytree(downloads_directory, deflate_directory)

        for filename in os.listdir(deflate_directory):
            filename = os.path.join(  # noqa: PLW2901
                deflate_directory, filename
            )
            if not os.path.isfile(filename):
                continue

            basename, extension = os.path.splitext(filename)
            basename = os.path.basename(basename)
            if extension.lower() in (".zip", ".tar", ".gz", ".bz2"):
                if basename.lower().endswith(".tar"):
                    basename = basename.rsplit(".", 1)[0]

                basename = basename.replace(".", "_")
                unpacking_directory = os.path.join(deflate_directory, basename)

                print(f'Unpacking "{filename}" archive...')  # noqa: T201
                setuptools.archive_util.unpack_archive(filename, unpacking_directory)
                os.remove(filename)

        with open(os.path.join(self.repository, "record.json"), "w") as record_json:
            json.dump(self.data, record_json, indent=4, sort_keys=True)

    def remove(self):
        """
        Remove the *Zenodo* record data local repository.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> record = Record.from_id("3245883")
        >>> with suppress_stdout():
        ...     record.pull()
        >>> record.remove()
        >>> record.synced()
        False
        """

        if os.path.exists(self.repository):
            shutil.rmtree(self.repository, onerror=_remove_readonly)


class Community(Mapping):
    """
    Define an object storing a *Zenodo* community data.

    Parameters
    ----------
    data
        *Zenodo* community data.
    configuration
        *Colour - Datasets* configuration.

    Attributes
    ----------
    -   :attr:`colour_datasets.Community.data`
    -   :attr:`colour_datasets.Community.configuration`
    -   :attr:`colour_datasets.Community.repository`
    -   :attr:`colour_datasets.Community.records`

    Methods
    -------
    -   :meth:`colour_datasets.Community.__init__`
    -   :meth:`colour_datasets.Community.__str__`
    -   :meth:`colour_datasets.Community.__repr__`
    -   :meth:`colour_datasets.Community.__getitem__`
    -   :meth:`colour_datasets.Community.__iter__`
    -   :meth:`colour_datasets.Community.__len__`
    -   :meth:`colour_datasets.Community.from_id`
    -   :meth:`colour_datasets.Community.synced`
    -   :meth:`colour_datasets.Community.pull`
    -   :meth:`colour_datasets.Community.remove`

    Examples
    --------
    >>> community_data = json_open(
    ...     "https://zenodo.org/api/communities/colour-science-datasets"
    ... )
    >>> records_data = json_open(community_data["links"]["records"])
    >>> community = Community(
    ...     {
    ...         "community": community_data,
    ...         "records": records_data,
    ...     }
    ... )
    >>> community["3245883"].title
    'Camera Spectral Sensitivity Database - Jiang et al. (2013)'
    """

    def __init__(self, data: Dict, configuration: Configuration | None = None) -> None:
        self._data: Dict = data
        self._configuration: Configuration = optional(configuration, Configuration())

        hits = self._data["records"]["hits"]["hits"]
        self._records: Dict = {
            str(hit["id"]): Record(hit, self._configuration) for hit in hits
        }

    @property
    def data(self) -> Dict:
        """
        Getter property for the *Zenodo* community data.

        Returns
        -------
        :class:`dict`
            *Zenodo* community data.
        """

        return self._data

    @property
    def configuration(self) -> Configuration:
        """
        Getter property for the *Colour - Datasets* configuration.

        Returns
        -------
        :class:`colour_datasets.Configuration`
           *Colour - Datasets* configuration.
        """

        return self._configuration

    @property
    def repository(self) -> str:
        """
        Getter property for the *Zenodo* community local repository.

        Returns
        -------
        :class:`str`
            *Zenodo* community local repository.
        """

        return self._configuration.repository

    @property
    def records(self) -> Dict:
        """
        Getter property for the *Zenodo* community records.

        Returns
        -------
        :class:`dict`
             *Zenodo* community records.
        """

        return self._records

    def __str__(self) -> str:
        """
        Return a formatted string representation of the *Zenodo* community.

        Returns
        -------
        :class:`str`
            Formatted string representation.

        Examples
        --------
        >>> community = Community.from_id("colour-science-datasets-tests")
        >>> print("\\n".join(str(community).splitlines()[:6]))
        ... # doctest: +ELLIPSIS
        colour-science-datasets-tests
        =============================
        <BLANKLINE>
        Datasets : ...
        Synced   : ...
        URL      : https://zenodo.org/communities/\
colour-science-datasets-tests
        """

        datasets = "\n".join(
            [
                (
                    f"[{'x' if dataset.synced() else ' '}] "
                    f"{dataset.id} : {dataset.title}"
                )
                for dataset in sorted(self.values(), key=lambda x: x.title)
            ]
        )

        synced = len([dataset for dataset in self.values() if dataset.synced()])

        representation = "\n".join(
            [
                f"{self._configuration.community}",
                f'{"=" * len(self._configuration.community)}',
                "",
                f"Datasets : {len(self)}",
                f"Synced   : {synced}",
                f'URL      : {self._data["community"]["links"]["self_html"]}',
                "",
                "Datasets",
                "--------",
                "",
                f"{datasets}",
            ]
        )

        return representation

    def __repr__(self) -> str:
        """
        Return an evaluable string representation of the *Zenodo* community.

        Returns
        -------
        :class:`str`
            Evaluable string representation.

        Examples
        --------
        >>> community = Community.from_id("colour-science-datasets-tests")
        >>> print("\\n".join(repr(community).splitlines()[:4]))
        Community(
            {'community': {'access': {'member_policy': 'open',
                                      'members_visibility': 'public',
                                      'record_submission_policy': 'open',
        """

        data = "\n".join([f"    {line}" for line in pformat(self._data).splitlines()])

        configuration = "\n".join(
            [f"        {line}" for line in pformat(self._configuration).splitlines()]
        )
        configuration = f"    Configuration(\n{configuration}\n    )"

        return f"{self.__class__.__name__}(\n{data},\n{configuration}\n)"

    def __getitem__(self, item: str | Any) -> Any:
        """
        Return the *Zenodo* record at given id.

        Parameters
        ----------
        item
            *Zenodo* recordid.

        Returns
        -------
        :class:`colour_datasets.Record`
            *Zenodo* record at given id.

        Examples
        --------
        >>> community = Community.from_id("colour-science-datasets-tests")
        >>> community["3245883"].title
        'Camera Spectral Sensitivity Database - Jiang et al. (2013)'
        """

        return self._records[item]

    def __iter__(self) -> Generator:
        """
        Iterate through the *Zenodo* community records.

        Yields
        ------
        Generator
            *Zenodo* community records iterator.

        Examples
        --------
        >>> for record in Community.from_id("colour-science-datasets-tests"):
        ...     print(record)  # doctest: +SKIP
        """

        yield from self._records

    def __len__(self) -> int:
        """
        Return *Zenodo* community records count.

        Returns
        -------
        :class:`int`
            *Zenodo* community records count.

        Examples
        --------
        # Doctests skip for Python 2.x compatibility.
        >>> len(Community.from_id("colour-science-datasets-tests"))
        ... # doctest: +SKIP
        3
        """

        return len(self._records)

    @staticmethod
    def from_id(
        id_: str,
        configuration: Configuration | None = None,
        retries: int = 3,
    ) -> Community:
        """
        :class:`colour_datasets.Community` class factory that builds an
        instance using given *Zenodo* community id.

        Parameters
        ----------
        id_ :
            *Zenodo* community id.
        configuration :
            configuration :
                *Colour - Datasets* configuration.
        retries :
            Number of retries in case where a networking error occurs.

        Returns
        -------
        :class:`colour_datasets.Community`
            *Zenodo* community data.

        Examples
        --------
        >>> community = Community.from_id("colour-science-datasets-tests")
        >>> community["3245883"].title
        'Camera Spectral Sensitivity Database - Jiang et al. (2013)'
        """

        configuration = Configuration() if configuration is None else configuration
        configuration.community = id_

        if not os.path.exists(configuration.repository):
            os.makedirs(configuration.repository)

        community_url = f"{configuration.api_url}/communities/{configuration.community}"

        community_json_filename = os.path.join(
            configuration.repository,
            f"{configuration.community}-community.json",
        )
        records_json_filename = os.path.join(
            configuration.repository, f"{configuration.community}-records.json"
        )

        try:
            community_data = json_open(community_url, retries)
            records_data = json_open(community_data["links"]["records"], retries)

            for key, value in {
                community_json_filename: community_data,
                records_json_filename: records_data,
            }.items():
                with open(key, "w") as json_file:
                    json.dump(value, json_file, indent=4, sort_keys=True)
        except (urllib.error.URLError, ValueError) as error:
            warning(
                'Retrieving the "{0}" community data failed '
                "after {1} attempts, "
                "attempting to use cached local data!"
            )
            if not all(
                [
                    os.path.exists(community_json_filename),
                    os.path.exists(records_json_filename),
                ]
            ):
                raise RuntimeError("Local files were not found, aborting!") from error

            with open(community_json_filename) as json_file:
                community_data = json.loads(json_file.read())

            with open(records_json_filename) as json_file:
                records_data = json.loads(json_file.read())

        data = {
            "community": community_data,
            "records": records_data,
        }

        return Community(data, configuration)

    def synced(self) -> bool:
        """
        Return whether the *Zenodo* community data is synced to the local
        repository.

        Returns
        -------
        :class:`bool`
            Whether the *Zenodo* community data is synced to the local
            repository.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> community = Community.from_id("colour-science-datasets-tests")
        >>> with suppress_stdout():
        ...     community.pull()  # doctest: +SKIP
        >>> community.synced()  # doctest: +SKIP
        True
        >>> community.remove()
        >>> community.synced()
        False
        """

        return all(record.synced() for record in self._records.values())

    def pull(self, use_urls_txt_file: bool = True, retries: int = 3):
        """
        Pull the *Zenodo* community data to the local repository.

        Parameters
        ----------
        use_urls_txt_file
            Whether to use the *urls.txt* file: if such a file is present in
            a *Zenodo* record data, the urls it defines take precedence over
            the record data files. The later will be used in the eventuality
            where the urls are not available.
        retries
            Number of retries in case where a networking error occurs or the
            *MD5* hash is not matching.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> community = Community.from_id("colour-science-datasets-tests")
        >>> community.remove()
        >>> with suppress_stdout():
        ...     community.pull()  # doctest: +SKIP
        >>> community.synced()  # doctest: +SKIP
        True
        """

        if not os.path.exists(self._configuration.repository):
            os.makedirs(self._configuration.repository)

        for record in self._records.values():
            record.pull(use_urls_txt_file, retries)

    def remove(self):
        """
        Remove the *Zenodo* community data local repository.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> community = Community.from_id("colour-science-datasets-tests")
        >>> with suppress_stdout():
        ...     community.pull()  # doctest: +SKIP
        >>> community.remove()
        >>> community.synced()
        False
        """

        if os.path.exists(self.repository):
            shutil.rmtree(self.repository, onerror=_remove_readonly)


def _remove_readonly(
    function: Callable,
    path: str,
    excinfo: Any,  # noqa: ARG001
):
    """
    Error handler for :func:`shutil.rmtree` definition that removes read-only
    files.
    """

    os.chmod(path, stat.S_IWRITE)

    function(path)
