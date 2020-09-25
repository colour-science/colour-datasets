# -*- coding: utf-8 -*-
"""
New Color Specifications for ColorChecker SG and Classic Charts - X-Rite (2016)
===============================================================================

Defines the objects implementing support for *X-Rite (2016)* *New Color
Specifications for ColorChecker SG and Classic Charts* dataset loading:

-   :class:`colour_datasets.loaders.DatasetLoader_XRite2016`
-   :func:`colour_datasets.loaders.build_XRite2016`

References
----------
-   :cite:`X-Rite2016` : X-Rite. (2016). New color specifications for
    ColorChecker SG and Classic Charts. Retrieved October 29, 2018, from
    http://xritephoto.com/ph_product_overview.aspx?ID=938&Action=Support&\
SupportID=5884#
"""

from __future__ import division, unicode_literals

import codecs
import numpy as np
import os
from collections import OrderedDict

from colour import CCS_ILLUMINANTS, Lab_to_XYZ, XYZ_to_xyY
from colour.characterisation import ColourChecker

from colour_datasets.records import datasets
from colour_datasets.loaders import AbstractDatasetLoader

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019-2020 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = ['DatasetLoader_XRite2016', 'build_XRite2016']


class DatasetLoader_XRite2016(AbstractDatasetLoader):
    """
    Defines the *X-Rite (2016)*
    *New Color Specifications for ColorChecker SG and Classic Charts* dataset
    loader.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.DatasetLoader_XRite2016.ID`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.DatasetLoader_XRite2016.__init__`
    -   :meth:`colour_datasets.loaders.DatasetLoader_XRite2016.load`

    References
    ----------
    :cite:`X-Rite2016`
    """

    ID = '3245895'
    """
    Dataset record id, i.e. the *Zenodo* record number.

    ID : unicode
    """

    def __init__(self):
        super(DatasetLoader_XRite2016,
              self).__init__(datasets()[DatasetLoader_XRite2016.ID])

    def load(self):
        """
        Syncs, parses, converts and returns the *X-Rite (2016)*
        *New Color Specifications for ColorChecker SG and Classic Charts*
        dataset content.

        Returns
        -------
        OrderedDict
            *X-Rite (2016)* *New Color Specifications for ColorChecker SG and
            Classic Charts* dataset content.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = DatasetLoader_XRite2016()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.content.keys())
        4
        """

        super(DatasetLoader_XRite2016, self).sync()

        keys = (
            'ColorChecker24 - After November 2014',
            'ColorChecker24 - Before November 2014',
            'ColorCheckerSG - After November 2014',
            'ColorCheckerSG - Before November 2014',
        )
        filenames = (
            'ColorChecker24_After_Nov2014.txt',
            'ColorChecker24_Before_Nov2014.txt',
            'ColorCheckerSG_After_Nov2014.txt',
            'ColorCheckerSG_Before_Nov2014.txt',
        )

        # TODO: Implement support for "CGATS" file format in "Colour":
        # https://github.com/colour-science/colour/issues/354
        illuminant = (
            CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['ICC D50'])

        self._content = OrderedDict()
        for key, filename in zip(keys, filenames):
            directory = os.path.splitext(filename)[0]
            path = os.path.join(self.record.repository, 'dataset', directory,
                                filename)

            with codecs.open(path, encoding='utf-8') as xrite_file:
                samples = []
                is_data = False
                lines = filter(
                    None, (line.strip() for line in xrite_file.readlines()))
                for line in lines:
                    if line == 'END_DATA':
                        is_data = False

                    if is_data:
                        tokens = line.split()
                        samples.append([
                            tokens[0],
                            [
                                float(value.replace(',', '.'))
                                for value in tokens[1:]
                            ],
                        ])

                    if line == 'BEGIN_DATA':
                        is_data = True

            i, j = (6, 4) if len(samples) == 24 else (14, 10)
            samples = np.array(samples)
            samples = np.transpose(samples.reshape([i, j, 2]), [1, 0, 2])
            keys, values = zip(*samples.reshape([-1, 2]))
            values = XYZ_to_xyY(Lab_to_XYZ(values, illuminant))
            self._content[key] = ColourChecker(key,
                                               OrderedDict(zip(keys, values)),
                                               illuminant)

        return self._content


_DATASET_LOADER_XRITE2016 = None
"""
Singleton instance of the *X-Rite (2016)*
*New Color Specifications for ColorChecker SG and Classic Charts* dataset
loader.

_DATASET_LOADER_XRITE2016 : DatasetLoader_XRite2016
"""


def build_XRite2016(load=True):
    """
    Singleton factory that the builds *X-Rite (2016)*
    *New Color Specifications for ColorChecker SG and Classic Charts* dataset
    loader.

    Parameters
    ----------
    load : bool, optional
        Whether to load the dataset upon instantiation.

    Returns
    -------
    DatasetLoader_XRite2016
        Singleton instance of the *X-Rite (2016)*
        *New Color Specifications for ColorChecker SG and Classic Charts*
        dataset loader.

    References
    ----------
    :cite:`X-Rite2016`
    """

    global _DATASET_LOADER_XRITE2016

    if _DATASET_LOADER_XRITE2016 is None:
        _DATASET_LOADER_XRITE2016 = DatasetLoader_XRite2016()
        if load:
            _DATASET_LOADER_XRITE2016.load()

    return _DATASET_LOADER_XRITE2016
