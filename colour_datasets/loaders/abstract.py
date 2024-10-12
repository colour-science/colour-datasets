"""
Abstract Dataset Loader
=======================

Define the abstract class implementing support for dataset loading:

-   :class:`colour_datasets.loaders.AbstractDatasetLoader`
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from colour.hints import Any

from colour_datasets.records import Record

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "AbstractDatasetLoader",
]


class AbstractDatasetLoader(ABC):
    """
    Define the base class for a dataset loader.

    This is an :class:`ABCMeta` abstract class that must be inherited by
    sub-classes.

    The sub-classes are expected to implement the
    :meth:`colour_datasets.loaders.AbstractDatasetLoader.load` method that
    handles the syncing, parsing, conversion and return of the dataset content
    as a *Python* object.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.AbstractDatasetLoader.ID`
    -   :attr:`colour_datasets.loaders.AbstractDatasetLoader.record`
    -   :attr:`colour_datasets.loaders.AbstractDatasetLoader.id`
    -   :attr:`colour_datasets.loaders.AbstractDatasetLoader.content`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.AbstractDatasetLoader.__init__`
    -   :meth:`colour_datasets.loaders.AbstractDatasetLoader.load`
    -   :meth:`colour_datasets.loaders.AbstractDatasetLoader.sync`

    Parameters
    ----------
    record
        Dataset record.
    """

    ID: str = "Undefined"
    """Dataset record id, i.e., the *Zenodo* record number."""

    def __init__(self, record: Record) -> None:
        self._record: Record = record
        self._content: Any | None = None

    @property
    def record(self) -> Record:
        """
        Getter property for the dataset record.

        Returns
        -------
        :class:`colour_datasets.Record`
            Dataset record.
        """

        return self._record

    @property
    def id(self) -> str:
        """
        Getter property for the dataset id.

        Returns
        -------
        :class:`str`
            Dataset id.
        """

        return self.__class__.ID

    @property
    def content(self) -> Any:
        """
        Getter property for the dataset content.

        Returns
        -------
        :class:`object`
           Dataset content.
        """

        return self._content

    @abstractmethod
    def load(self) -> Any:
        """
        Sync, parse, convert and return the dataset content as a *Python*
        object.

        Returns
        -------
        :class:`object`
            Dataset content as a *Python* object.

        Notes
        -----
        -   Sub-classes are required to call
            :meth:`colour_datasets.loaders.AbstractDatasetLoader.sync` method
            when they implement it, e.g., ``super().sync()``.
        """

    def sync(self):
        """
        Sync the dataset content, i.e., checks whether it is synced and pulls
        it if required.
        """

        if not self.record.synced():
            self.record.pull()
