# -*- coding: utf-8 -*-
"""
Labsphere SRS-99-020 - Labsphere (2019)
=======================================

Defines the objects implementing support for *Labsphere (2019)*
*Labsphere SRS-99-020* dataset loading:

-   :class:`colour_datasets.loaders.Labsphere2019DatasetLoader`
-   :func:`colour_datasets.loaders.build_Labsphere2019`

References
----------
-   :cite:`Labsphere2019` : Labsphere. (2019). Labsphere SRS-99-020.
    doi:10.5281/zenodo.3245875
"""

from __future__ import division, unicode_literals

import numpy as np
import os
from collections import OrderedDict

from colour import SpectralDistribution
from colour.utilities import tsplit

from colour_datasets.records import datasets
from colour_datasets.loaders import AbstractDatasetLoader

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['Labsphere2019DatasetLoader', 'build_Labsphere2019']


class Labsphere2019DatasetLoader(AbstractDatasetLoader):
    """
    Defines the *Labsphere (2019)* *Labsphere SRS-99-020* dataset loader.

    Attributes
    ----------
    ID

    Methods
    -------
    load

    References
    ----------
    :cite:`Labsphere2019`
    """

    ID = '3245875'
    """
    Dataset record id, i.e. the *Zenodo* record number.

    ID : unicode
    """

    def __init__(self):
        super(Labsphere2019DatasetLoader,
              self).__init__(datasets()[Labsphere2019DatasetLoader.ID])

    def load(self):
        """
        Syncs, parses, converts and returns the *Labsphere (2019)*
        *Labsphere SRS-99-020* dataset content.

        Returns
        -------
        OrderedDict
            *Labsphere (2019)* *Labsphere SRS-99-020* dataset content.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = Labsphere2019DatasetLoader()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.content.keys())
        1
        """

        super(Labsphere2019DatasetLoader, self).sync()

        sd_path = os.path.join(self.record.repository, 'dataset',
                               'SRS-99-020.txt')

        values = tsplit(np.loadtxt(sd_path, delimiter='\t', skiprows=2))
        self._content = OrderedDict([
            ('Labsphere SRS-99-020',
             SpectralDistribution(
                 values[1], values[0], name='Labsphere SRS-99-020')),
        ])

        return self._content


_LABSPHERE2019_DATASET_LOADER = None
"""
Singleton instance of the *Labsphere (2019)* *Labsphere SRS-99-020* dataset
loader.

_LABSPHERE2019_DATASET_LOADER : Labsphere2019DatasetLoader
"""


def build_Labsphere2019(load=True):
    """
    Singleton factory that builds the *Labsphere (2019)* *Labsphere SRS-99-020*
    dataset loader.

    Parameters
    ----------
    load : bool, optional
        Whether to load the dataset upon instantiation.

    Returns
    -------
    Labsphere2019DatasetLoader
        Singleton instance of the *Labsphere (2019)* *Labsphere SRS-99-020*
        dataset loader.

    References
    ----------
    :cite:`Labsphere2019`
    """

    global _LABSPHERE2019_DATASET_LOADER

    if _LABSPHERE2019_DATASET_LOADER is None:
        _LABSPHERE2019_DATASET_LOADER = Labsphere2019DatasetLoader()
        if load:
            _LABSPHERE2019_DATASET_LOADER.load()

    return _LABSPHERE2019_DATASET_LOADER
