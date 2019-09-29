# -*- coding: utf-8 -*-
"""
Zenodo
======

Defines the objects implementing support for a *Zenodo* community and its
records:

-   :class:`colour_datasets.Record`
-   :class:`colour_datasets.Community`
"""

from __future__ import division, unicode_literals
import json
import os
import six
import shutil
import setuptools.archive_util
import stat
import tempfile
import textwrap
from collections import Mapping
from six.moves import html_parser
from six.moves import urllib
from pprint import pformat

from colour.utilities import warning

from colour_datasets.utilities import url_download, json_open
from colour_datasets.records import Configuration

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['Record', 'Community']


class Record(object):
    """
    Defines an object storing a *Zenodo* record data and providing methods to
    sync it in a local repository.

    Attributes
    ----------
    data
    configuration
    repository
    id
    title

    Methods
    -------
    __init__
    __str__
    __repr__
    from_id
    synced
    pull
    remove

    Parameters
    ----------
    data : unicode
        *Zenodo* record data.
    configuration : Configuration
        *Colour - Datasets* configuration.

    Examples
    --------
    >>> record = Record(json_open('https://zenodo.org/api/records/3245883'))

    # Doctests skip for Python 2.x compatibility.
    >>> record.id  # doctest: +SKIP
    '3245883'
    >>> record.title  # doctest: +SKIP
    'Camera Spectral Sensitivity Database'
    """

    def __init__(self, data, configuration=None):

        self._data = data
        self._configuration = (Configuration()
                               if configuration is None else configuration)

    @property
    def data(self):
        """
        Getter and setter property for the *Zenodo* record data.

        Parameters
        ----------
        value : dict
            Value to set the *Zenodo* record data with.

        Returns
        -------
        dict
            *Zenodo* record data.
        """

        return self._data

    @property
    def configuration(self):
        """
        Getter and setter property for the *Colour - Datasets* configuration.

        Parameters
        ----------
        value : Configuration
            Value to set the *Colour - Datasets* configuration with.

        Returns
        -------
        unicode
           *Colour - Datasets* configuration.
        """

        return self._configuration

    @property
    def repository(self):
        """
        Getter and setter property for the *Zenodo* record local repository.

        Parameters
        ----------
        value : unicode
            Value to set the the *Zenodo* record local repository with.

        Returns
        -------
        unicode
            *Zenodo* record local repository.
        """

        return os.path.join(self._configuration.repository, self.id)

    @property
    def id(self):
        """
        Getter and setter property for the *Zenodo* record id.

        Parameters
        ----------
        value : unicode
            Value to set the *Zenodo* record id with.

        Returns
        -------
        unicode
            *Zenodo* record id.
        """

        return six.text_type(self._data['id'])

    @property
    def title(self):
        """
        Getter and setter property for the *Zenodo* record title.

        Parameters
        ----------
        value : unicode
            Value to set the *Zenodo* record title with.

        Returns
        -------
        unicode
            *Zenodo* record title.
        """

        return self._data['metadata']['title']

    def __str__(self):
        """
        Returns a formatted string representation of the *Zenodo* record.

        Returns
        -------
        unicode
            Formatted string representation.

        Examples
        --------
        >>> data = json_open('https://zenodo.org/api/records/3245883')
        >>> print('\\n'.join(str(Record(data)).splitlines()[:4]))
        Camera Spectral Sensitivity Database - 1.0.0
        ============================================
        <BLANKLINE>
        Record ID        : 3245883
        """

        def strip_html(text):
            """
            Strips *HTML* tags from given text.

            Parameters
            ----------
            text : unicode
                Text to strips the *HTML* tags from.

            Returns
            -------
            unicode
                Text with *HTML* tags stripped of.
            """

            text = text.replace('&nbsp;', ' ').replace('\n\n', ' ')

            parts = []
            parser = html_parser.HTMLParser()
            parser.handle_data = parts.append
            parser.feed(text)

            return ''.join(parts)

        metadata = self._data['metadata']
        authors = '; '.join(
            [creator['name'] for creator in metadata['creators']])
        files = self._data['files']

        representation = (
            '{0} - {1}\n'
            '{2}\n\n'
            'Record ID        : {3}\n'
            'Authors          : {4}\n'
            'License          : {5}\n'
            'DOI              : {6}\n'
            'Publication Date : {7}\n'
            'URL              : {8}\n\n'
            'Description\n-----------\n\n{9}\n\n'
            'Files\n-----\n\n{10}'.format(
                metadata['title'],
                metadata['version'],
                '=' * (len(self.title) + 3 + len(metadata['version'])),
                self.id,
                authors,
                metadata['license']['id'],
                metadata['doi'],
                metadata['publication_date'],
                self._data['links']['html'],
                '\n'.join(
                    textwrap.wrap(strip_html(metadata['description']), 79)),
                '\n'.join([
                    '- {0} : {1}'.format(file_data['key'],
                                         file_data['links']['self'])
                    for file_data in sorted(files, key=lambda x: x['key'])
                ]),
            ))

        if six.PY2:
            representation = representation.encode('utf-8')

        return representation

    def __repr__(self):
        """
        Returns an evaluable string representation of the *Zenodo* record.

        Returns
        -------
        unicode
            Evaluable string representation.

        Examples
        --------
        >>> data = json_open('https://zenodo.org/api/records/3245883')

        # Doctests skip for Python 2.x compatibility.
        >>> print('\\n'.join(repr(Record(data)).splitlines()[:4]))
        ... # doctest: +SKIP
        Record(
            {'conceptdoi': '10.5281/zenodo.3245882',
             'conceptrecid': '3245882',
             'created': '2019-06-14T09:34:15.765924+00:00',
        """

        return '{0}(\n{1},\n{2}\n)'.format(
            self.__class__.__name__, '\n'.join([
                '    {0}'.format(line)
                for line in pformat(self._data).splitlines()
            ]), '    Configuration(\n{0}\n    )'.format('\n'.join([
                '        {0}'.format(line)
                for line in pformat(self._configuration).splitlines()
            ])))

    @staticmethod
    def from_id(id_, configuration=None, retries=3):
        """
        :class:`colour_datasets.Record` class factory that builds an instance
        using given *Zenodo* record id.

        Parameters
        ----------
        id_ : unicode
            *Zenodo* record id.
        configuration : Configuration, optional
            configuration : Configuration
                *Colour - Datasets* configuration.
        retries : int, optional
            Number of retries in case where a networking error occurs.

        Returns
        -------
        Record
            *Zenodo* record data.

        Examples
        --------
        # Doctests skip for Python 2.x compatibility.
        >>> Record.from_id('3245883').title
        ... # doctest: +SKIP
        'Camera Spectral Sensitivity Database'
        """

        configuration = (Configuration()
                         if configuration is None else configuration)

        if not os.path.exists(configuration.repository):
            os.makedirs(configuration.repository)

        record_url = '{0}/records/{1}'.format(configuration.api_url, id_)

        return Record(json_open(record_url, retries), configuration)

    def synced(self):
        """
        Returns whether the *Zenodo* record data is synced to the local
        repository.

        Returns
        -------
        bool
            Whether the *Zenodo* record data is synced to the local repository.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> record = Record.from_id('3245883')
        >>> with suppress_stdout():
        ...     record.pull()
        >>> record.synced()
        True
        >>> record.remove()
        >>> record.synced()
        False
        """

        downloads_directory = os.path.join(
            self.repository, self._configuration.downloads_directory)
        deflate_directory = os.path.join(self.repository,
                                         self._configuration.deflate_directory)
        return all([
            os.path.exists(downloads_directory),
            os.path.exists(deflate_directory),
        ])

    def pull(self, use_urls_txt_file=True, retries=3):
        """
        Pulls the *Zenodo* record data to the local repository.

        Parameters
        ----------
        use_urls_txt_file : bool, optional
            Whether to use the *urls.txt* file: if such a file is present in
            the *Zenodo* record data, the urls it defines take precedence over
            the record data files. The later will be used in the eventuality
            where the urls are not available.
        retries : int, optional
            Number of retries in case where a networking error occurs or the
            *MD5* hash is not matching.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> record = Record.from_id('3245883')
        >>> record.remove()
        >>> with suppress_stdout():
        ...     record.pull()
        >>> record.synced()
        True
        """

        print('Pulling "{0}" record content...'.format(self.title))

        if not os.path.exists(self._configuration.repository):
            os.makedirs(self._configuration.repository)

        downloads_directory = os.path.join(
            self.repository, self._configuration.downloads_directory)
        if not os.path.exists(downloads_directory):
            os.makedirs(downloads_directory)

        # As much as possible, the original file urls are used, those are
        # given by the content of :attr:`URLS_TXT_FILE` attribute file.
        urls_txt = None
        for file_data in self.data['files']:
            if file_data['key'] == self._configuration.urls_txt_file:
                urls_txt = file_data
                break

        def _urls_download(urls):
            """
            Downloads given urls.
            """

            for url, md5 in urls.items():
                filename = os.path.join(
                    downloads_directory,
                    urllib.parse.unquote(url.split('/')[-1]))
                url_download(url, filename, md5.split(':')[-1], retries)

        try:
            if use_urls_txt_file and urls_txt:
                urls = {}
                urls_txt_file = tempfile.mktemp()
                url_download(urls_txt['links']['self'], urls_txt_file,
                             urls_txt['checksum'].split(':')[-1], retries)

                with open(urls_txt_file, 'r') as json_file:
                    urls_txt_json = json.load(json_file)
                    for url, md5 in urls_txt_json['urls'].items():
                        urls[url] = md5.split(':')[-1]

                shutil.copyfile(
                    urls_txt_file,
                    os.path.join(downloads_directory,
                                 self._configuration.urls_txt_file))

                _urls_download(urls)
            else:
                raise ValueError(
                    '"{0}" file was not found in record data!'.format(
                        self._configuration.urls_txt_file))
        except (urllib.error.URLError, ValueError) as error:
            warning('An error occurred using urls from "{0}" file: {1}\n'
                    'Switching to record urls...'.format(
                        self._configuration.urls_txt_file, error))

            urls = {}
            for file_data in self.data['files']:
                if file_data['key'] == self._configuration.urls_txt_file:
                    continue

                urls[file_data['links']['self']] = (
                    file_data['checksum'].split(':')[-1])

            _urls_download(urls)

        deflate_directory = os.path.join(self.repository,
                                         self._configuration.deflate_directory)
        if os.path.exists(deflate_directory):
            shutil.rmtree(deflate_directory, onerror=_remove_readonly)

        shutil.copytree(downloads_directory, deflate_directory)

        for filename in os.listdir(deflate_directory):
            filename = os.path.join(deflate_directory, filename)
            if not os.path.isfile(filename):
                continue

            basename, extension = os.path.splitext(filename)
            basename = os.path.basename(basename)
            if extension.lower() in ('.zip', '.tar', '.gz', '.bz2'):
                if basename.lower().endswith('.tar'):
                    basename = basename.rsplit('.', 1)[0]

                basename = basename.replace('.', '_')
                unpacking_directory = os.path.join(deflate_directory, basename)

                print('Unpacking "{0}" archive...'.format(filename))
                setuptools.archive_util.unpack_archive(filename,
                                                       unpacking_directory)
                os.remove(filename)

        with open(os.path.join(self.repository, 'record.json'),
                  'w') as record_json:
            json.dump(self.data, record_json, indent=4, sort_keys=True)

    def remove(self):
        """
        Removes the *Zenodo* record data local repository.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> record = Record.from_id('3245883')
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
    Defines an object storing a *Zenodo* community data.

    Attributes
    ----------
    data
    configuration
    repository
    records

    Methods
    -------
    __init__
    __str__
    __repr__
    __getitem__
    __iter__
    __len__
    from_id
    synced
    pull
    remove

    Parameters
    ----------
    data : unicode
        *Zenodo* community data.
    configuration : Configuration
        *Colour - Datasets* configuration.

    Examples
    --------
    >>> community_data = json_open(
    ...     'https://zenodo.org/api/communities/colour-science-datasets')
    >>> records_data = json_open(
    ...     'https://zenodo.org/api/records/?q=communities:'
    ...     'colour-science-datasets')
    >>> community = Community({
    ...     'community': community_data,
    ...     'records': records_data,
    ... })

    # Doctests skip for Python 2.x compatibility.
    >>> community['3245883'].title  # doctest: +SKIP
    'Camera Spectral Sensitivity Database'
    """

    def __init__(self, data, configuration=None):
        self._data = data
        self._configuration = (Configuration()
                               if configuration is None else configuration)

        hits = self._data['records']['hits']['hits']
        self._records = {
            six.text_type(hit['id']): Record(hit, self._configuration)
            for hit in hits
        }

    @property
    def data(self):
        """
        Getter and setter property for the *Zenodo* community data.

        Parameters
        ----------
        value : dict
            Value to set the *Zenodo* community data.with.

        Returns
        -------
        dict
            *Zenodo* community data.
        """

        return self._data

    @property
    def configuration(self):
        """
        Getter and setter property for the *Colour - Datasets* configuration.

        Parameters
        ----------
        value : Configuration
            Value to set the *Colour - Datasets* configuration with.

        Returns
        -------
        unicode
           *Colour - Datasets* configuration.
        """

        return self._configuration

    @property
    def repository(self):
        """
        Getter and setter property for the *Zenodo* community local repository.

        Parameters
        ----------
        value : unicode
            Value to set the the *Zenodo* community local repository with.

        Returns
        -------
        unicode
            *Zenodo* community local repository.
        """

        return self._configuration.repository

    @property
    def records(self):
        """
        Getter and setter property for the *Zenodo* community records.

        Parameters
        ----------
        value : dict
            Value to set the *Zenodo* community records with.

        Returns
        -------
        dict
             *Zenodo* community records.
        """

        return self._records

    def __str__(self):
        """
        Returns a formatted string representation of the *Zenodo* community.

        Returns
        -------
        unicode
            Formatted string representation.

        Examples
        --------
        >>> community = Community.from_id('colour-science-datasets-tests')
        >>> print('\\n'.join(str(community).splitlines()[:6]))
        ... # doctest: +ELLIPSIS
        colour-science-datasets-tests
        =============================
        <BLANKLINE>
        Datasets : ...
        Synced   : ...
        URL      : https://zenodo.org/communities/\
colour-science-datasets-tests/
        """

        datasets = '\n'.join([
            '[{0}] {1} : {2}'.format('x' if dataset.synced() else ' ',
                                     dataset.id, dataset.title)
            for dataset in sorted(self.values(), key=lambda x: x.title)
        ])
        representation = ('{0}\n'
                          '{1}\n\n'
                          'Datasets : {2}\n'
                          'Synced   : {3}\n'
                          'URL      : {4}\n\n'
                          'Datasets\n--------\n\n'
                          '{5}'.format(
                              self._configuration.community,
                              '=' * len(self._configuration.community),
                              len(self),
                              len([
                                  dataset for dataset in self.values()
                                  if dataset.synced()
                              ]),
                              self._data['community']['links']['html'],
                              datasets,
                          ))

        if six.PY2:
            representation = representation.encode('utf-8')

        return representation

    def __repr__(self):
        """
        Returns an evaluable string representation of the *Zenodo* community.

        Returns
        -------
        unicode
            Evaluable string representation.

        Examples
        --------
        >>> community = Community.from_id('colour-science-datasets-tests')

        # Doctests skip for Python 2.x compatibility.
        >>> print('\\n'.join(repr(community).splitlines()[:4]))
        ... # doctest: +SKIP
        Community(
            {'community': {'created': '2019-06-09T10:45:47.999975+00:00',
                           'curation_policy': '',
                           'description': '',
        """

        return '{0}(\n{1},\n{2}\n)'.format(
            self.__class__.__name__, '\n'.join([
                '    {0}'.format(line)
                for line in pformat(self._data).splitlines()
            ]), '    Configuration(\n{0}\n    )'.format('\n'.join([
                '        {0}'.format(line)
                for line in pformat(self._configuration).splitlines()
            ])))

    def __getitem__(self, id_):
        """
        Returns the *Zenodo* record at given id.

        Parameters
        ----------
        id_ : unicode
            *Zenodo* recordid.

        Returns
        -------
        Record
            *Zenodo* record at given id.

        Examples
        --------
        >>> community = Community.from_id('colour-science-datasets-tests')

        # Doctests skip for Python 2.x compatibility.
        >>> community['3245883'].title  # doctest: +SKIP
        'Camera Spectral Sensitivity Database'
        """

        return self._records[id_]

    def __iter__(self):
        """
        Iterates through the *Zenodo* community records.

        Returns
        -------
        iterator
            *Zenodo* community records iterator.

        Examples
        --------
        # Doctests skip for Python 2.x compatibility.
        >>> for record in Community.from_id('colour-science-datasets-tests'):
        ...     print(record) # doctest: +SKIP
        """

        return iter(self._records)

    def __len__(self):
        """
        Returns *Zenodo* community records count.

        Returns
        -------
        int
            *Zenodo* community records count.

        Examples
        --------
        # Doctests skip for Python 2.x compatibility.
        >>> len(Community.from_id('colour-science-datasets-tests'))
        ... # doctest: +SKIP
        3
        """

        return len(self._records)

    @staticmethod
    def from_id(id_, configuration=None, retries=3):
        """
        :class:`colour_datasets.Community` class factory that builds an
        instance using given *Zenodo* community id.

        Parameters
        ----------
        id_ : unicode
            *Zenodo* community id.
        configuration : Configuration, optional
            configuration : Configuration
                *Colour - Datasets* configuration.
        retries : int, optional
            Number of retries in case where a networking error occurs.

        Returns
        -------
        Community
            *Zenodo* community data.

        Examples
        --------
        >>> community = Community.from_id('colour-science-datasets-tests')

        # Doctests skip for Python 2.x compatibility.
        >>> community['3245883'].title  # doctest: +SKIP
        'Camera Spectral Sensitivity Database'
        """

        configuration = (Configuration()
                         if configuration is None else configuration)
        configuration.community = id_

        if not os.path.exists(configuration.repository):
            os.makedirs(configuration.repository)

        community_url = '{0}/communities/{1}'.format(configuration.api_url,
                                                     configuration.community)
        # NOTE: Retrieving 512 datasets at most. This should cover needs for
        # the foreseeable future. There is likely an undocumented hard limit on
        # "Zenodo" server side.
        records_url = '{0}/records/?q=communities:{1}&size=512'.format(
            configuration.api_url, configuration.community)

        community_json_filename = os.path.join(
            configuration.repository,
            '{0}-community.json'.format(configuration.community))
        records_json_filename = os.path.join(
            configuration.repository,
            '{0}-records.json'.format(configuration.community))

        try:
            community_data = json_open(community_url, retries)
            records_data = json_open(records_url, retries)

            for key, value in {
                    community_json_filename: community_data,
                    records_json_filename: records_data,
            }.items():
                with open(key, 'w') as json_file:
                    json.dump(value, json_file, indent=4, sort_keys=True)
        except (urllib.error.URLError, ValueError):
            warning('Retrieving the "{0}" community data failed '
                    'after {1} attempts, '
                    'attempting to use cached local data!')
            if not all([
                    os.path.exists(community_json_filename),
                    os.path.exists(records_json_filename),
            ]):
                raise RuntimeError('Local files were not found, aborting!')

            with open(community_json_filename) as json_file:
                community_data = json.loads(json_file.read())

            with open(records_json_filename) as json_file:
                records_data = json.loads(json_file.read())

        data = {
            'community': community_data,
            'records': records_data,
        }

        return Community(data, configuration)

    def synced(self):
        """
        Returns whether the *Zenodo* community data is synced to the local
        repository.

        Returns
        -------
        bool
            Whether the *Zenodo* community data is synced to the local
            repository.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> community = Community.from_id('colour-science-datasets-tests')
        >>> with suppress_stdout():
        ...     community.pull()  # doctest: +SKIP
        >>> community.synced()  # doctest: +SKIP
        True
        >>> community.remove()
        >>> community.synced()
        False
        """

        return all([record.synced() for record in self._records.values()])

    def pull(self, use_urls_txt_file=True, retries=3):
        """
        Pulls the *Zenodo* community data to the local repository.

        Parameters
        ----------
        use_urls_txt_file : bool, optional
            Whether to use the *urls.txt* file: if such a file is present in
            a *Zenodo* record data, the urls it defines take precedence over
            the record data files. The later will be used in the eventuality
            where the urls are not available.
        retries : int, optional
            Number of retries in case where a networking error occurs or the
            *MD5* hash is not matching.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> community = Community.from_id('colour-science-datasets-tests')
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
        Removes the *Zenodo* community data local repository.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> community = Community.from_id('colour-science-datasets-tests')
        >>> with suppress_stdout():
        ...     community.pull()  # doctest: +SKIP
        >>> community.remove()
        >>> community.synced()
        False
        """

        if os.path.exists(self.repository):
            shutil.rmtree(self.repository, onerror=_remove_readonly)


def _remove_readonly(function, path, excinfo):
    """
    Error handler for :func:`shutil.rmtree` definition that removes read-only
    files.
    """

    os.chmod(path, stat.S_IWRITE)

    function(path)
