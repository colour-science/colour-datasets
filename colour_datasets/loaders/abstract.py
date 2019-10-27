# -*- coding: utf-8 -*-
"""
Abstract Dataset Loader
=======================

Defines the abstract class implementing support for dataset loading:

-   :class:`colour_datasets.loaders.AbstractDatasetLoader`
"""

from __future__ import division, unicode_literals

from abc import ABCMeta, abstractmethod
from six import add_metaclass

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['AbstractDatasetLoader']


@add_metaclass(ABCMeta)
class AbstractDatasetLoader:
    """
    Defines the base class for a dataset loader.

    This is an :class:`ABCMeta` abstract class that must be inherited by
    sub-classes.

    The sub-classes are expected to implement the
    :meth:`colour_datasets.loaders.AbstractDatasetLoader.load` method that
    handles the syncing, parsing, conversion and return of the dataset content
    as a *Python* object.

    Attributes
    ----------
    ID
    record
    id
    content

    Methods
    -------
    load
    sync

    Parameters
    ----------
    record : Record
        Dataset record.
    """

    ID = None
    """
    Dataset record id, i.e. the *Zenodo* record number.

    ID : unicode
    """

    def __init__(self, record):
        self._record = record
        self._content = None

    @property
    def record(self):
        """
        Getter and setter property for the dataset record.

        Parameters
        ----------
        value : Record
            Value to set the dataset record with.

        Returns
        -------
        unicode
            Dataset record.
        """

        return self._record

    @property
    def id(self):
        """
        Getter and setter property for the dataset id.

        Parameters
        ----------
        value : unicode
            Value to set the dataset id with.

        Returns
        -------
        unicode
            Dataset id.
        """

        return self.__class__.ID

    @property
    def content(self):
        """
        Getter and setter property for the dataset content.

        Parameters
        ----------
        value : object
            Value to set the dataset content with.

        Returns
        -------
        unicode
           Dataset content.
        """

        return self._content

    @abstractmethod
    def load(self):
        """
        Syncs, parses, converts and returns the dataset content as a *Python*
        object.

        Returns
        -------
        object
            Dataset content as a *Python* object.

        Notes
        -----
        -   Sub-classes are required to call
            :meth:`colour_datasets.loaders.AbstractDatasetLoader.sync` method
            when they implement it, e.g.
            ``super(MyDatasetLoader, self).sync()``.
        """

        pass

    def sync(self):
        """
        Syncs the dataset content, i.e. checks whether it is synced and pulls
        it if required.
        """

        if not self.record.synced():
            self.record.pull()
