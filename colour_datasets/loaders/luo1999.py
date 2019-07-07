# -*- coding: utf-8 -*-
"""
Corresponding-Colour Datasets - Luo and Rhodes (1999)
=====================================================

Defines the objects implementing support for *Luo and Rhodes (1999)*
*Corresponding-Colour Datasets* dataset loading:

-   :class:`colour_datasets.loaders.Luo1999DatasetLoader`
-   :func:`colour_datasets.loaders.build_Luo1999`

References
----------
-   :cite:`Luo1999` : Luo, M. R., & Rhodes, P. A. (1999). Corresponding-colour
    datasets. Color Research & Application, 24(4), 295–296.
    doi:10.1002/(SICI)1520-6378(199908)24:4<295::AID-COL10>3.0.CO;2-K
"""

from __future__ import division, unicode_literals

import codecs
import os
from collections import OrderedDict, namedtuple
from colour.utilities import as_float_array

from colour_datasets.records import datasets
from colour_datasets.loaders import AbstractDatasetLoader

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = [
    'CorrespondingColourDataset', 'Luo1999DatasetLoader', 'build_Luo1999'
]


class CorrespondingColourDataset(
        namedtuple(
            'CorrespondingColourDataset',
            ('name', 'XYZ_r', 'XYZ_t', 'XYZ_cr', 'XYZ_ct', 'metadata'))):
    """
    Defines a *Luo and Rhodes (1999)* *Corresponding-Colour Datasets* dataset.

    Parameters
    ----------
    name : unicode
        *Luo and Rhodes (1999)* *Corresponding-Colour Datasets* dataset name.
    XYZ_r : array_like
        *CIE XYZ* tristimulus values of the reference illuminant.
    XYZ_t : array_like
        *CIE XYZ* tristimulus values of the test illuminant.
    XYZ_cr : array_like
        Corresponding *CIE XYZ* tristimulus values under the reference
        illuminant.
    XYZ_ct : array_like
        Corresponding *CIE XYZ* tristimulus values under the test illuminant.
    metadata : dict
        Dataset metadata.
    """


class Luo1999DatasetLoader(AbstractDatasetLoader):
    """
    Defines the *Luo and Rhodes (1999)*
    *Corresponding-Colour Datasets* dataset
    loader.

    Attributes
    ----------
    ID

    Methods
    -------
    load

    References
    ----------
    :cite:`Luo1999`
    """

    ID = '3270903'
    """
    Dataset record id, i.e. the *Zenodo* record number.

    ID : unicode
    """

    def __init__(self):
        super(Luo1999DatasetLoader,
              self).__init__(datasets()[Luo1999DatasetLoader.ID])

    def load(self):
        """
        Syncs, parses, converts and returns the *Luo and Rhodes (1999)*
        *Corresponding-Colour Datasets* dataset content.

        Returns
        -------
        OrderedDict
            Dataset content as an :class:`OrderedDict` of
            *Colour Checkers* and their
            :class:`colour.characterisation.ColourChecker` class instances.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = Luo1999DatasetLoader()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.data.keys())
        37
        """

        super(Luo1999DatasetLoader, self).sync()

        metadata_headers = (
            'No. of Phases',
            'No. of Samples',
            'Illuminant Test',
            'Illuminant Ref.',
            'Illuminance (lux)',
            'Background (Y%)',
            'Sample Size',
            'Medium',
            'Experimental Method',
        )

        corresponding_colour_datasets = OrderedDict([
            ('CSAJ-C', [('CSAJ.da.dat', ),
                        (
                            1,
                            87,
                            'D65',
                            'A',
                            '1000',
                            20,
                            'S',
                            'Refl.',
                            'Haploscopic',
                        )]),
            ('CSAJ-Hunt', [(
                'CSAJ.10.dat',
                'CSAJ.50.dat',
                'CSAJ.1000.dat',
                'CSAJ.3000.dat',
            ),
                           (
                               4,
                               20,
                               'D65',
                               'D65',
                               '10-3000',
                               20,
                               'S',
                               'Refl.',
                               'Haploscopic',
                           )]),
            ('CSAJ-Stevens', [(
                'Steve.10.dat',
                'Steve.50.dat',
                'Steve.1000.dat',
                'Steve.3000.dat',
            ),
                              (
                                  4,
                                  19,
                                  'D65',
                                  'D65',
                                  '10-3000',
                                  20,
                                  'S',
                                  'Refl.',
                                  'Haploscopic',
                              )]),
            ('Helson', [('helson.ca.dat', ),
                        (
                            1,
                            59,
                            'D65',
                            'A',
                            '1000',
                            20,
                            'S',
                            'Refl.',
                            'Memory',
                        )]),
            ('Lam & Rigg', [('lam.da.dat', ),
                            (
                                1,
                                58,
                                'D65',
                                'A',
                                '1000',
                                20,
                                'L',
                                'Refl.',
                                'Memory',
                            )]),
            ('Lutchi (A)', [('lutchi.da.dat', ),
                            (
                                1,
                                43,
                                'D65',
                                'A',
                                '1000',
                                20,
                                'S',
                                'Refl.',
                                'Magnitude',
                            )]),
            ('Lutchi (D50)', [('lutchi.dd.dat', ),
                              (
                                  1,
                                  44,
                                  'D65',
                                  'D50',
                                  '1000',
                                  20,
                                  'S',
                                  'Refl.',
                                  'Magnitude',
                              )]),
            ('Lutchi (WF)', [('lutchi.dw.dat', ),
                             (
                                 1,
                                 41,
                                 'D65',
                                 'WF',
                                 '1000',
                                 20,
                                 'S',
                                 'Refl.',
                                 'Magnitude',
                             )]),
            ('Kuo & Luo (A)', [('Kuo.da.dat', ),
                               (
                                   1,
                                   40,
                                   'D65',
                                   'A',
                                   '1000',
                                   20,
                                   'L',
                                   'Refl.',
                                   'Magnitude',
                               )]),
            ('Kuo & Luo (TL84)', [('Kuo.dt.dat', ),
                                  (
                                      1,
                                      41,
                                      'D65',
                                      'TL84',
                                      '1000',
                                      20,
                                      'S',
                                      'Refl.',
                                      'Magnitude',
                                  )]),
            ('Breneman-C', [(
                'Brene.p1.dat',
                'Brene.p2.dat',
                'Brene.p3.dat',
                'Brene.p4.dat',
                'Brene.p6.dat',
                'Brene.p8.dat',
                'Brene.p9.dat',
                'Brene.p11.dat',
                'Brene.p12.dat',
            ),
                            (
                                9,
                                107,
                                'D65, 55',
                                'A, P, G',
                                '50-3870',
                                30,
                                'S',
                                'Trans.',
                                'Magnitude',
                            )]),
            ('Breneman-L', [(
                'Brene.p5.dat',
                'Brene.p7.dat',
                'Brene.p10.dat',
            ),
                            (
                                3,
                                36,
                                'D55',
                                'D55',
                                '50-3870',
                                30,
                                'S',
                                'Trans.',
                                'Haploscopic',
                            )]),
            ('Braun & Fairchild', [(
                'RIT.1.dat',
                'RIT.2.dat',
                'RIT.3.dat',
                'RIT.4.dat',
            ),
                                   (
                                       4,
                                       66,
                                       'D65',
                                       'D30, 65, 95',
                                       '129',
                                       20,
                                       'S',
                                       'Mon., Refl.',
                                       'Matching',
                                   )]),
            ('McCann', [(
                'mcan.b.dat',
                'mcan.g.dat',
                'mcan.grey.dat',
                'mcan.r.dat',
                'mcan.y.dat',
            ),
                        (
                            5,
                            85,
                            'D65',
                            'R, Y, G, B',
                            '14-40',
                            30,
                            'S',
                            'Refl.',
                            'Haploscopic',
                        )]),
        ])

        self._data = OrderedDict()
        for key, (filenames,
                  metadata) in corresponding_colour_datasets.items():
            for filename in filenames:
                path = os.path.join(self.record.repository, 'dataset',
                                    filename)

                XYZ_r = XYZ_t = None
                XYZ_cr, XYZ_ct = [], []
                with codecs.open(path, encoding='utf-8') as dat_file:
                    lines = filter(
                        None, (line.strip() for line in dat_file.readlines()))
                    for i, line in enumerate(lines):
                        values = line.split()
                        if i == 0:
                            XYZ_r = as_float_array(
                                list(map(float, values[:3])))
                            XYZ_t = as_float_array(
                                list(map(float, values[3:])))
                        elif len(values) == 1:
                            continue
                        else:
                            XYZ_cr.append(
                                as_float_array(list(map(float, values[:3]))))
                            XYZ_ct.append(
                                as_float_array(list(map(float, values[3:]))))

                name = '{0} - {1}'.format(key, filename.split('.')[1])

                self._data[name] = CorrespondingColourDataset(
                    name,
                    XYZ_r,
                    XYZ_t,
                    as_float_array(XYZ_cr),
                    as_float_array(XYZ_ct),
                    OrderedDict(zip(metadata_headers, metadata)),
                )

        return self._data


_LUO1999_DATASET_LOADER = None
"""
Singleton instance of the *Luo and Rhodes (1999)*
*Corresponding-Colour Datasets* dataset loader.

_LUO1999_DATASET_LOADER : Luo1999DatasetLoader
"""


def build_Luo1999(load=True):
    """
    Singleton factory that the builds *Luo and Rhodes (1999)*
    *Corresponding-Colour Datasets* dataset loader.

    Parameters
    ----------
    load : bool, optional
        Whether to load the dataset upon instantiation.

    Returns
    -------
    Luo1999DatasetLoader
        Singleton instance of the *Luo and Rhodes (1999)*
        *Corresponding-Colour Datasets* dataset loader.

    References
    ----------
    :cite:`Luo1999`
    """

    global _LUO1999_DATASET_LOADER

    if _LUO1999_DATASET_LOADER is None:
        _LUO1999_DATASET_LOADER = Luo1999DatasetLoader()
        if load:
            _LUO1999_DATASET_LOADER.load()

    return _LUO1999_DATASET_LOADER
