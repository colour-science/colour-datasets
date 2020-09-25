# -*- coding: utf-8 -*-
"""
Constant Hue Loci Data - Hung and Berns (1995)
==============================================

Defines the objects implementing support for *Hung and Berns (1995)* *Constant
Hue Loci Data* dataset loading:

-   :class:`colour_datasets.loaders.DatasetLoader_Hung1995`
-   :func:`colour_datasets.loaders.build_Hung1995`

References
----------
-   :cite:`Hung1995` : Hung, P.-C., & Berns, R. S. (1995). Determination of
    constant Hue Loci for a CRT gamut and their predictions using color
    appearance spaces. Color Research & Application, 20(5), 285-295.
    doi:10.1002/col.5080200506
"""

from __future__ import division, unicode_literals

import numpy as np
import os
from collections import OrderedDict, namedtuple

from colour import CCS_ILLUMINANTS, xy_to_XYZ, xyY_to_XYZ

from colour_datasets.records import datasets
from colour_datasets.loaders import AbstractDatasetLoader

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019-2020 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = [
    'ConstantPerceivedHueColourMatches_Hung1995', 'DatasetLoader_Hung1995',
    'build_Hung1995'
]


class ConstantPerceivedHueColourMatches_Hung1995(
        namedtuple('ConstantPerceivedHueColourMatches_Hung1995',
                   ('name', 'XYZ_r', 'XYZ_cr', 'XYZ_ct', 'metadata'))):
    """
    Defines *Hung and Berns (1995)* *Constant Hue Loci Data*
    colour matches data for a given hue angle.

    Parameters
    ----------
    name : unicode
        *Hung and Berns (1995)* *Constant Hue Loci Data* hue angle or
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


class DatasetLoader_Hung1995(AbstractDatasetLoader):
    """
    Defines the *Hung and Berns (1995)* *Constant Hue Loci Data*
    dataset loader.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.DatasetLoader_Hung1995.ID`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.DatasetLoader_Hung1995.__init__`
    -   :meth:`colour_datasets.loaders.DatasetLoader_Hung1995.load`

    References
    ----------
    :cite:`Hung1995`
    """

    ID = '3367463'
    """
    Dataset record id, i.e. the *Zenodo* record number.

    ID : unicode
    """

    def __init__(self):
        super(DatasetLoader_Hung1995,
              self).__init__(datasets()[DatasetLoader_Hung1995.ID])

    def load(self):
        """
        Syncs, parses, converts and returns the *Hung and Berns (1995)*
        *Constant Hue Loci Data* dataset content.

        Returns
        -------
        OrderedDict
            *Hung and Berns (1995)* *Constant Hue Loci Data* dataset content.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = DatasetLoader_Hung1995()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.content.keys())
        6
        """

        super(DatasetLoader_Hung1995, self).sync()

        self._content = OrderedDict()

        filenames = OrderedDict([
            ('Table I.csv', 'Reference colors.'),
            ('Table II.csv', 'Intra- and interobserver variances for each '
             'reference hue expressed in circumferential '
             'hue-angle difference.'),
            ('Table III.csv', 'Weight-averaged constant hue loci for the CL '
             'experiment.'),
            ('Table IV.csv', 'Weight-averaged constant hue loci for the VL '
             'experiment.'),
        ])

        for filename in filenames:
            datafile_path = os.path.join(self.record.repository, 'dataset',
                                         filename)

            self._content[filename.split('.')[0]] = np.genfromtxt(
                datafile_path,
                delimiter=',',
                names=True,
                dtype=None,
                encoding='utf-8')

        hues = [
            'Red', 'Red-yellow', 'Yellow', 'Yellow-green', 'Green',
            'Green-cyan', 'Cyan', 'Cyan-blue', 'Blue', 'Blue-magenta',
            'Magenta', 'Magenta-red'
        ]

        XYZ_r = xy_to_XYZ(
            CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C'])

        for table, experiment in [('Table III', 'CL'), ('Table IV', 'VL')]:
            key = 'Constant Hue Loci Data - {0}'.format(experiment)
            self._content[key] = OrderedDict()
            for hue in hues:
                for sample_r in self._content['Table I']:
                    sample_r = sample_r.tolist()
                    if sample_r[0] == hue:
                        XYZ_cr = xyY_to_XYZ(sample_r[1:4]) / 100
                        break

                XYZ_ct = []
                metadata = {
                    'Color name': [],
                    'C*uv': [],
                }
                for sample_t in self._content[table]:
                    sample_t = sample_t.tolist()
                    if not sample_t[0] == hue:
                        continue

                    XYZ_ct.append(sample_t[2:])
                    metadata['Color name'].append(sample_t[0])
                    metadata['C*uv'].append(sample_t[1])

                self._content[key][hue] = (
                    ConstantPerceivedHueColourMatches_Hung1995(
                        hue, XYZ_r, XYZ_cr,
                        np.vstack(XYZ_ct) / 100, metadata))

        return self._content


_DATASET_LOADER_HUNG1995 = None
"""
Singleton instance of the *Hung and Berns (1995)*
*Constant Hue Loci Data* dataset loader.

_DATASET_LOADER_HUNG1995 : DatasetLoader_Hung1995
"""


def build_Hung1995(load=True):
    """
    Singleton factory that builds the *Hung and Berns (1995)*
    *Constant Hue Loci Data* dataset loader.

    Parameters
    ----------
    load : bool, optional
        Whether to load the dataset upon instantiation.

    Returns
    -------
    DatasetLoader_Hung1995
        Singleton instance of the *Hung and Berns (1995)*
        *Constant Hue Loci Data* dataset loader.

    References
    ----------
    :cite:`Hung1995`
    """

    global _DATASET_LOADER_HUNG1995

    if _DATASET_LOADER_HUNG1995 is None:
        _DATASET_LOADER_HUNG1995 = DatasetLoader_Hung1995()
        if load:
            _DATASET_LOADER_HUNG1995.load()

    return _DATASET_LOADER_HUNG1995
