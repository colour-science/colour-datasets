# -*- coding: utf-8 -*-
"""
Constant Perceived-Hue Data - Ebner and Fairchild (1998)
========================================================

Defines the objects implementing support for *Ebner and Fairchild (1998)*
*Constant Perceived-Hue Data* dataset loading:

-   :class:`colour_datasets.loaders.DatasetLoader_Ebner1998`
-   :func:`colour_datasets.loaders.build_Ebner1998`

References
----------
-   :cite:`Ebner1998` : Ebner, F., & Fairchild, M. D. (1998). Finding constant
    hue surfaces in color space. In G. B. Beretta & R. Eschbach (Eds.), Proc.
    SPIE 3300, Color Imaging: Device-Independent Color, Color Hardcopy, and
    Graphic Arts III, (2 January 1998) (pp. 107-117). doi:10.1117/12.298269
"""

import codecs
import numpy as np
import os
from collections import namedtuple

from colour.utilities import as_float_array

from colour_datasets.loaders import AbstractDatasetLoader
from colour_datasets.records import datasets

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019-2021 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = [
    'ConstantPerceivedHueColourMatches_Ebner1998', 'DatasetLoader_Ebner1998',
    'build_Ebner1998'
]


class ConstantPerceivedHueColourMatches_Ebner1998(
        namedtuple('ConstantPerceivedHueColourMatches_Ebner1998',
                   ('name', 'XYZ_r', 'XYZ_cr', 'XYZ_ct', 'metadata'))):
    """
    Defines *Ebner and Fairchild (1998)* *Constant Perceived-Hue Data*
    colour matches data for a given hue angle.

    Parameters
    ----------
    name : unicode
        *Ebner and Fairchild (1998)* *Constant Perceived-Hue Data* hue angle or
        name.
    XYZ_r : array_like
        *CIE XYZ* tristimulus values of the reference illuminant.
    XYZ_cr : array_like
        *CIE XYZ* tristimulus values of the reference colour under the
        reference illuminant.
    XYZ_ct : array_like
        *CIE XYZ* tristimulus values of the colour matches under the reference
        illuminant.
    metadata : dict
        Dataset metadata.
    """


class DatasetLoader_Ebner1998(AbstractDatasetLoader):
    """
    Defines the *Ebner and Fairchild (1998)* *Constant Perceived-Hue Data*
    dataset loader.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.DatasetLoader_Ebner1998.ID`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.DatasetLoader_Ebner1998.__init__`
    -   :meth:`colour_datasets.loaders.DatasetLoader_Ebner1998.load`

    References
    ----------
    :cite:`Ebner1998`
    """

    ID = '3362536'
    """
    Dataset record id, i.e. the *Zenodo* record number.

    ID : unicode
    """

    def __init__(self):
        super(DatasetLoader_Ebner1998,
              self).__init__(datasets()[DatasetLoader_Ebner1998.ID])

    def load(self):
        """
        Syncs, parses, converts and returns the *Ebner and Fairchild (1998)*
        *Constant Perceived-Hue Data* dataset content.

        Returns
        -------
        dict
            *Ebner and Fairchild (1998)* Constant Perceived-Hue Data* dataset
            content.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = DatasetLoader_Ebner1998()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.content.keys())
        1
        """

        super(DatasetLoader_Ebner1998, self).sync()

        self._content = dict([('Constant Perceived-Hue Data', dict())])

        datafile_path = os.path.join(self.record.repository, 'dataset',
                                     'Ebner_Constant_Hue_Data.txt')

        def _parse_float_values(data):
            """
            Parses float values from given data.
            """

            data = [float(x) / 100 for x in data.split('\t') if x]

            values = as_float_array(data).reshape(-1, 3)

            return np.squeeze(values)

        with codecs.open(datafile_path, encoding='utf-8') as database_file:
            lines = filter(
                None, (line.strip() for line in database_file.readlines()))

            for line in lines:
                if line.startswith('White Point'):
                    XYZ_r = _parse_float_values(line.split(':')[-1])
                elif line.startswith('reference hue'):
                    line = line.replace('reference hue ', '')
                    hue, data = line.split('\t', 1)
                    hue, data = int(hue), _parse_float_values(data)

                    self._content['Constant Perceived-Hue Data'][hue] = (
                        ConstantPerceivedHueColourMatches_Ebner1998(
                            'Reference Hue Angle - {0}'.format(hue), XYZ_r,
                            data[0], data[1:], {'h': hue}))

        return self._content


_DATASET_LOADER_EBNER1998 = None
"""
Singleton instance of the *Ebner and Fairchild (1998)*
*Constant Perceived-Hue Data* dataset loader.

_DATASET_LOADER_EBNER1998 : DatasetLoader_Ebner1998
"""


def build_Ebner1998(load=True):
    """
    Singleton factory that builds the *Ebner and Fairchild (1998)*
    *Constant Perceived-Hue Data* dataset loader.

    Parameters
    ----------
    load : bool, optional
        Whether to load the dataset upon instantiation.

    Returns
    -------
    DatasetLoader_Ebner1998
        Singleton instance of the *Ebner and Fairchild (1998)*
        *Constant Perceived-Hue Data* dataset loader.

    References
    ----------
    :cite:`Ebner1998`
    """

    global _DATASET_LOADER_EBNER1998

    if _DATASET_LOADER_EBNER1998 is None:
        _DATASET_LOADER_EBNER1998 = DatasetLoader_Ebner1998()
        if load:
            _DATASET_LOADER_EBNER1998.load()

    return _DATASET_LOADER_EBNER1998
