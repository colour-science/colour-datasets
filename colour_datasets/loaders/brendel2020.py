# -*- coding: utf-8 -*-
"""
Measured Commercial LED Spectra - Brendel (2020)
================================================

Defines the objects implementing support for *Brendel (2020)*
*Measured Commercial LED Spectra* dataset loading:

-   :class:`colour_datasets.loaders.DatasetLoader_Brendel2020`
-   :func:`colour_datasets.loaders.build_Brendel2020`

References
----------
-   :cite:`Brendel2020` : Brendel, H. (2020). Measured Commercial LED Spectra.
    Retrieved September 26, 2020, from
    https://haraldbrendel.com/files/led_spd_350_700.csv
"""

from __future__ import division, unicode_literals

import numpy as np
import os
from collections import OrderedDict

from colour import LinearInterpolator, SpectralShape, SpectralDistribution
from colour.utilities import as_int

from colour_datasets.records import datasets
from colour_datasets.loaders import AbstractDatasetLoader

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019-2020 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = ['DatasetLoader_Brendel2020', 'build_Brendel2020']


class DatasetLoader_Brendel2020(AbstractDatasetLoader):
    """
    Defines the *Brendel (2020)* *Measured Commercial LED Spectra* dataset
    loader.

    Attributes
    ----------
    ID

    Methods
    -------
    load

    References
    ----------
    :cite:`Brendel2020`
    """

    ID = '4051012'
    """
    Dataset record id, i.e. the *Zenodo* record number.

    ID : unicode
    """

    def __init__(self):
        super(DatasetLoader_Brendel2020,
              self).__init__(datasets()[DatasetLoader_Brendel2020.ID])

    def load(self):
        """
        Syncs, parses, converts and returns the *Brendel (2020)*
        *Measured Commercial LED Spectra* dataset content.

        Returns
        -------
        OrderedDict
            *Brendel (2020)* *Measured Commercial LED Spectra* dataset content.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = DatasetLoader_Brendel2020()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.content.keys())
        29
        """

        super(DatasetLoader_Brendel2020, self).sync()

        self._content = OrderedDict()

        wavelengths = SpectralShape(350, 700, 2).range()

        csv_path = os.path.join(self.record.repository, 'dataset',
                                'led_spd_350_700.csv')

        for i, values in enumerate(
                np.loadtxt(csv_path, delimiter=',', skiprows=1)):
            peak = as_int(wavelengths[np.argmax(values)])
            name = '{0}nm - LED {1} - Brendel (2020)'.format(peak, i)

            self._content[name] = SpectralDistribution(
                values,
                wavelengths,
                name=name,
                interpolator=LinearInterpolator)

        return self._content


_DATASET_LOADER_BRENDEL2020 = None
"""
Singleton instance of the *Brendel (2020)* *Measured Commercial LED Spectra*
dataset loader.

_DATASET_LOADER_BRENDEL2020 : DatasetLoader_Brendel2020
"""


def build_Brendel2020(load=True):
    """
    Singleton factory that builds the *Brendel (2020)*
    *Measured Commercial LED Spectra* dataset loader.

    Parameters
    ----------
    load : bool, optional
        Whether to load the dataset upon instantiation.

    Returns
    -------
    DatasetLoader_Brendel2020
        Singleton instance of the *Brendel (2020)*
        *Measured Commercial LED Spectra* dataset loader.

    References
    ----------
    :cite:`Brendel2020`
    """

    global _DATASET_LOADER_BRENDEL2020

    if _DATASET_LOADER_BRENDEL2020 is None:
        _DATASET_LOADER_BRENDEL2020 = DatasetLoader_Brendel2020()
        if load:
            _DATASET_LOADER_BRENDEL2020.load()

    return _DATASET_LOADER_BRENDEL2020
