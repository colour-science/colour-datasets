# -*- coding: utf-8 -*-
"""
New Color Specifications for ColorChecker SG and Classic Charts - X-Rite (2016)
===============================================================================

Defines the objects implementing support for *X-Rite (2016)*
*New Color Specifications for ColorChecker SG and Classic Charts* dataset
loading:

-   :class:`colour_datasets.loaders.XRite2016DatasetLoader`
-   :func:`colour_datasets.loaders.build_XRite2016`

References
----------
-   :cite:`X-Rite2016` : X-Rite. (2016). New Color Specifications for
    ColorChecker SG and Classic Charts. Retrieved June 14, 2019, from
    https://xritephoto.com/ph_product_overview.aspx?\
ID=938&Action=Support&SupportID=5884
"""

from __future__ import division, unicode_literals

import codecs
import numpy as np
import os
from collections import OrderedDict

from colour import ILLUMINANTS, Lab_to_XYZ, XYZ_to_xyY
from colour.characterisation import ColourChecker

from colour_datasets.records import datasets
from colour_datasets.loaders import AbstractDatasetLoader

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['XRite2016DatasetLoader', 'build_XRite2016']


class XRite2016DatasetLoader(AbstractDatasetLoader):
    """
    Defines the *X-Rite (2016)*
    *New Color Specifications for ColorChecker SG and Classic Charts* dataset
    loader.

    Attributes
    ----------
    ID

    Methods
    -------
    load

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
        super(XRite2016DatasetLoader,
              self).__init__(datasets()[XRite2016DatasetLoader.ID])

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
        >>> dataset = XRite2016DatasetLoader()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.content.keys())
        4
        """

        super(XRite2016DatasetLoader, self).sync()

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
            ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['ICC D50'])

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


_XRITE2016_DATASET_LOADER = None
"""
Singleton instance of the *X-Rite (2016)*
*New Color Specifications for ColorChecker SG and Classic Charts* dataset
loader.

_XRITE2016_DATASET_LOADER : XRite2016DatasetLoader
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
    XRite2016DatasetLoader
        Singleton instance of the *X-Rite (2016)*
        *New Color Specifications for ColorChecker SG and Classic Charts*
        dataset loader.

    References
    ----------
    :cite:`X-Rite2016`
    """

    global _XRITE2016_DATASET_LOADER

    if _XRITE2016_DATASET_LOADER is None:
        _XRITE2016_DATASET_LOADER = XRite2016DatasetLoader()
        if load:
            _XRITE2016_DATASET_LOADER.load()

    return _XRITE2016_DATASET_LOADER
