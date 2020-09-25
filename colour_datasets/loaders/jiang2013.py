# -*- coding: utf-8 -*-
"""
Camera Spectral Sensitivity Database - Jiang et al. (2013)
==========================================================

Defines the objects implementing support for *Jiang, Liu, Gu and Süsstrunk
(2013)* *Camera Spectral Sensitivity Database* dataset loading:

-   :class:`colour_datasets.loaders.DatasetLoader_Jiang2013`
-   :func:`colour_datasets.loaders.build_Jiang2013`

References
----------
-   :cite:`Jiang2013` : Jiang, J., Liu, D., Gu, J., & Susstrunk, S. (2013).
    What is the space of spectral sensitivity functions for digital color
    cameras? 2013 IEEE Workshop on Applications of Computer Vision (WACV),
    168-179. doi:10.1109/WACV.2013.6475015
"""

from __future__ import division, unicode_literals

import codecs
import numpy as np
import os
import re
from collections import OrderedDict

from colour import SpectralShape
from colour.characterisation import RGB_CameraSensitivities
from colour.utilities import as_float_array

from colour_datasets.records import datasets
from colour_datasets.loaders import AbstractDatasetLoader

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019-2020 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = ['DatasetLoader_Jiang2013', 'build_Jiang2013']


class DatasetLoader_Jiang2013(AbstractDatasetLoader):
    """
    Defines the *Jiang et al. (2013)* *Camera Spectral Sensitivity Database*
    dataset loader.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.DatasetLoader_Jiang2013.ID`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.DatasetLoader_Jiang2013.__init__`
    -   :meth:`colour_datasets.loaders.DatasetLoader_Jiang2013.load`

    References
    ----------
    :cite:`Jiang2013`
    """

    ID = '3245883'
    """
    Dataset record id, i.e. the *Zenodo* record number.

    ID : unicode
    """

    def __init__(self):
        super(DatasetLoader_Jiang2013,
              self).__init__(datasets()[DatasetLoader_Jiang2013.ID])

    def load(self):
        """
        Syncs, parses, converts and returns the *Jiang et al. (2013)*
        *Camera Spectral Sensitivity Database* dataset content.

        Returns
        -------
        OrderedDict
            *Jiang et al. (2013)* *Camera Spectral Sensitivity Database*
            dataset content.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = DatasetLoader_Jiang2013()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.content.keys())
        28
        """

        super(DatasetLoader_Jiang2013, self).sync()

        shape = SpectralShape(400, 720, 10)

        self._content = OrderedDict()
        database_path = os.path.join(self.record.repository, 'dataset',
                                     'camspec_database.txt')
        with codecs.open(database_path, encoding='utf-8') as database_file:
            lines = filter(
                None, (line.strip() for line in database_file.readlines()))
            camera = None
            for line in lines:
                if re.match('[a-zA-Z]+', line):
                    camera = line
                    self._content[camera] = []
                    continue

                self._content[camera].extend(
                    [float(value) for value in line.split('\t')])

        for camera, values in self._content.items():
            self._content[camera] = RGB_CameraSensitivities(
                np.transpose(as_float_array(values).reshape([3, 33])),
                shape.range(),
                name=camera)

        return self._content


_DATASET_LOADER_JIANG2013 = None
"""
Singleton instance of the *Jiang et al. (2013)*
*Camera Spectral Sensitivity Database* dataset loader.

_DATASET_LOADER_JIANG2013 : DatasetLoader_Jiang2013
"""


def build_Jiang2013(load=True):
    """
    Singleton factory that builds the *Jiang et al. (2013)*
    *Camera Spectral Sensitivity Database* dataset loader.

    Parameters
    ----------
    load : bool, optional
        Whether to load the dataset upon instantiation.

    Returns
    -------
    DatasetLoader_Jiang2013
        Singleton instance of the *Jiang et al. (2013)*
        *Camera Spectral Sensitivity Database* dataset loader.

    References
    ----------
    :cite:`Jiang2013`
    """

    global _DATASET_LOADER_JIANG2013

    if _DATASET_LOADER_JIANG2013 is None:
        _DATASET_LOADER_JIANG2013 = DatasetLoader_Jiang2013()
        if load:
            _DATASET_LOADER_JIANG2013.load()

    return _DATASET_LOADER_JIANG2013
