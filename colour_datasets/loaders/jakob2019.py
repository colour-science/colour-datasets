# -*- coding: utf-8 -*-
"""
Spectral Upsampling Coefficient Tables - Jakob and Hanika (2019)
================================================================

Defines the objects implementing support for *Jakob and Hanika (2019)*
*Spectral Upsampling Coefficient Tables* dataset loading:

-   :class:`colour_datasets.loaders.DatasetLoader_Jakob2019`
-   :func:`colour_datasets.loaders.build_Jakob2019`

References
----------
-   :cite:`Jakob2019` : Jakob, W., & Hanika, J. (2019). A Low‐Dimensional
    Function Space for Efficient Spectral Upsampling. Computer Graphics Forum,
    38(2), 147-155. doi:10.1111/cgf.13626
"""

from __future__ import division, unicode_literals

import glob
import os
from collections import OrderedDict

from colour.recovery import LUT3D_Jakob2019

from colour_datasets.records import datasets
from colour_datasets.loaders import AbstractDatasetLoader

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019-2020 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = ['DatasetLoader_Jakob2019', 'build_Jakob2019']


class DatasetLoader_Jakob2019(AbstractDatasetLoader):
    """
    Defines the *Jakob and Hanika (2019)*
    *Spectral Upsampling Coefficient Tables* dataset loader.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.DatasetLoader_Jakob2019.ID`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.DatasetLoader_Jakob2019.__init__`
    -   :meth:`colour_datasets.loaders.DatasetLoader_Jakob2019.load`

    References
    ----------
    :cite:`Jakob2019`
    """

    ID = '4050598'
    """
    Dataset record id, i.e. the *Zenodo* record number.

    ID : unicode
    """

    def __init__(self):
        super(DatasetLoader_Jakob2019,
              self).__init__(datasets()[DatasetLoader_Jakob2019.ID])

    def load(self):
        """
        Syncs, parses, converts and returns the *Jakob and Hanika (2019)*
        *Spectral Upsampling Coefficient Tables* dataset content.

        Returns
        -------
        OrderedDict
            *Jakob and Hanika (2019)* *Spectral Upsampling Coefficient Tables*
            dataset content.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = DatasetLoader_Jakob2019()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.content.keys())
        4
        """

        super(DatasetLoader_Jakob2019, self).sync()

        self._content = OrderedDict()

        tables_path = os.path.join(self.record.repository, 'dataset',
                                   'Jakob2019Spectral', 'supplement', 'tables')

        coeff_file_to_RGB_colourspace = {
            'rec2020': 'ITU-R BT.2020',
            'srgb': 'sRGB',
            'aces2065_1': 'ACES2065-1',
            'prophotorgb': 'ProPhoto RGB',
        }

        for coeff_file in glob.glob('{0}/*.coeff'.format(tables_path)):
            key = os.path.splitext(os.path.basename(coeff_file))[0]
            key = coeff_file_to_RGB_colourspace.get(key, key)

            LUT = LUT3D_Jakob2019()
            LUT.read(coeff_file)

            self._content[key] = LUT

        return self._content


_DATASET_LOADER_JAKOB2019 = None
"""
Singleton instance of the *Jakob and Hanika (2019)*
*Spectral Upsampling Coefficient Tables* dataset loader.

_DATASET_LOADER_JAKOB2019 : DatasetLoader_Jakob2019
"""


def build_Jakob2019(load=True):
    """
    Singleton factory that builds the *Jakob and Hanika (2019)*
    *Spectral Upsampling Coefficient Tables* dataset loader.

    Parameters
    ----------
    load : bool, optional
        Whether to load the dataset upon instantiation.

    Returns
    -------
    DatasetLoader_Jakob2019
        Singleton instance of the *Jakob and Hanika (2019)*
        *Spectral Upsampling Coefficient Tables* dataset loader.

    References
    ----------
    :cite:`Jakob2019`
    """

    global _DATASET_LOADER_JAKOB2019

    if _DATASET_LOADER_JAKOB2019 is None:
        _DATASET_LOADER_JAKOB2019 = DatasetLoader_Jakob2019()
        if load:
            _DATASET_LOADER_JAKOB2019.load()

    return _DATASET_LOADER_JAKOB2019
