# -*- coding: utf-8 -*-
"""
Spectral Database of Commonly Used Cine Lighting - Karge et al. (2015)
======================================================================

Defines the objects implementing support for *Karge, Froehlich and Eberhardt
(2015)* *Spectral Database of Commonly Used Cine Lighting* dataset loading:

-   :class:`colour_datasets.loaders.DatasetLoader_Karge2015`
-   :func:`colour_datasets.loaders.build_Karge2015`

References
----------
-   :cite:`Karge2015` : Karge, A., Froehlich, J., & Eberhardt, B. (2015). A
    Spectral Database of Commonly Used Cine Lighting. Color and Imaging
    Conference, 2015. https://www.researchgate.net/publication/\
282908037_A_Spectral_Database_of_Commonly_Used_Cine_Lighting
"""

import os
import re
from collections import defaultdict

from colour.algebra import LinearInterpolator
from colour.io import read_sds_from_csv_file

from colour_datasets.loaders import AbstractDatasetLoader
from colour_datasets.records import datasets

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019-2021 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = [
    'DatasetLoader_Karge2015',
    'build_Karge2015',
]


class DatasetLoader_Karge2015(AbstractDatasetLoader):
    """
    Defines the *Karge et al. (2015)*
    *Spectral Database of Commonly Used Cine Lighting* dataset loader.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.DatasetLoader_Karge2015.ID`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.DatasetLoader_Karge2015.__init__`
    -   :meth:`colour_datasets.loaders.DatasetLoader_Karge2015.load`

    References
    ----------
    :cite:`Karge2015`
    """

    ID = '4642271'
    """
    Dataset record id, i.e. the *Zenodo* record number.

    ID : str
    """

    def __init__(self):
        super(DatasetLoader_Karge2015,
              self).__init__(datasets()[DatasetLoader_Karge2015.ID])

    def load(self):
        """
        Syncs, parses, converts and returns the *Karge et al. (2015)*
        *Spectral Database of Commonly Used Cine Lighting* dataset content.

        Returns
        -------
        dict
            *Karge et al. (2015)*
            *Spectral Database of Commonly Used Cine Lighting* dataset content.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = DatasetLoader_Karge2015()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.content.keys())
        7
        """

        super(DatasetLoader_Karge2015, self).sync()

        self._content = defaultdict(lambda: defaultdict(dict))

        database_root = os.path.join(self.record.repository, 'dataset',
                                     'OFTP_full-sample-package_v2')
        for path in sorted(os.listdir(database_root)):
            if path.split('_')[0] not in ('Arri', 'Bron', 'CMT', 'Dedolight'):
                continue

            type_ = os.path.splitext(path)[0].replace('_v2', '').replace(
                '_normalized', '').replace('_', ' ')
            category = 'Normalised' if 'normalized' in path else 'Raw'
            path = os.path.join(database_root, path)

            sds = dict()
            for name, sd in read_sds_from_csv_file(
                    path, transpose=True, delimiter=';').items():
                if re.match('f\\d', name):
                    continue

                sd.interpolator = LinearInterpolator
                sds[name] = sd

            self._content[type_][category] = sds

        return dict(self._content)


_DATASET_LOADER_KARGE2015 = None
"""
Singleton instance of the *Karge et al. (2015)*
*Spectral Database of Commonly Used Cine Lighting* dataset loader.

_DATASET_LOADER_KARGE2015 : DatasetLoader_Karge2015
"""


def build_Karge2015(load=True):
    """
    Singleton factory that builds the *Karge et al. (2015)*
    *Spectral Database of Commonly Used Cine Lighting* dataset loader.

    Parameters
    ----------
    load : bool, optional
        Whether to load the dataset upon instantiation.

    Returns
    -------
    DatasetLoader_Karge2015
        Singleton instance of the *Karge et al. (2015)*
        *Spectral Database of Commonly Used Cine Lighting* dataset loader.

    References
    ----------
    :cite:`Karge2015`
    """

    global _DATASET_LOADER_KARGE2015

    if _DATASET_LOADER_KARGE2015 is None:
        _DATASET_LOADER_KARGE2015 = DatasetLoader_Karge2015()
        if load:
            _DATASET_LOADER_KARGE2015.load()

    return _DATASET_LOADER_KARGE2015
