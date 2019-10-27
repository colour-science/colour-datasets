# -*- coding: utf-8 -*-
"""
Observer Function Database - Asano (2015)
=========================================

Defines the objects implementing support for *Asano (2015)*
*Observer Function Database* dataset loading:

-   :class:`colour_datasets.loaders.Asano2015DatasetLoader`
-   :func:`colour_datasets.loaders.build_Asano2015`

References
----------
-   :cite:`Asano2015` : Asano, Y. (2015). Individual Colorimetric Observers for
    Personalized Color Imaging. R.I.T.
"""

from __future__ import division, unicode_literals

import numpy as np
import os
import xlrd
from collections import OrderedDict, namedtuple

from colour import SpectralShape
from colour.colorimetry import (XYZ_ColourMatchingFunctions,
                                LMS_ConeFundamentals)
from colour.utilities import as_float_array, tstack

from colour_datasets.records import datasets
from colour_datasets.loaders import AbstractDatasetLoader
from colour_datasets.utilities import cell_range_values, index_to_column

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = [
    'Asano2015_Specification', 'Asano2015DatasetLoader', 'build_Asano2015'
]


class Asano2015_Specification(
        namedtuple(
            'Asano2015_Specification',
            ('XYZ_2', 'XYZ_10', 'LMS_2', 'LMS_10', 'parameters', 'others'))):
    """
    Defines the *Asano (2015)* specification for an observer.

    Parameters
    ----------
    XYZ_2 : XYZ_ColourMatchingFunctions
        *CIE XYZ* 2 degree colour matching functions.
    XYZ_10 : XYZ_ColourMatchingFunctions
        *CIE XYZ* 10 degree colour matching functions.
    LMS_2 : LMS_ConeFundamentals
        *LMS* 2 degree cone fundamentals.
    LMS_10 : LMS_ConeFundamentals
        *LMS* 10 degree cone fundamentals.
    parameters : array_like
        Observer parameters.
    others : array_like
        Other information.

    References
    ----------
    :cite:`Asano2015`
    """

    def __new__(cls, XYZ_2, XYZ_10, LMS_2, LMS_10, parameters, others=None):
        """
        Returns a new instance of the
        :class:`colour_datasets.loaders.asano2015.Asano2015_Specification`
        class.
        """

        return super(Asano2015_Specification, cls).__new__(
            cls, XYZ_2, XYZ_10, LMS_2, LMS_10, parameters, others)


class Asano2015DatasetLoader(AbstractDatasetLoader):
    """
    Defines the *Asano (2015)* *Observer Function Database* dataset loader.

    Attributes
    ----------
    ID

    Methods
    -------
    load
    parse_workbook_Asano2015

    References
    ----------
    :cite:`Asano2015`
    """

    ID = '3252742'
    """
    Dataset record id, i.e. the *Zenodo* record number.

    ID : unicode
    """

    def __init__(self):
        super(Asano2015DatasetLoader,
              self).__init__(datasets()[Asano2015DatasetLoader.ID])

    def load(self):
        """
        Syncs, parses, converts and returns the *Asano (2015)*
        *Observer Function Database* dataset content.

        Returns
        -------
        OrderedDict
            *Asano (2015)* *Observer Function Database* dataset content.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = Asano2015DatasetLoader()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.content.keys())
        2
        """

        super(Asano2015DatasetLoader, self).sync()

        self._content = OrderedDict([
            ('Categorical Observers', OrderedDict()),
            ('Colour Normal Observers', OrderedDict()),
        ])

        # Categorical Observers
        workbook_path = os.path.join(self.record.repository, 'dataset',
                                     'Data_10CatObs.xls')

        observers = (1, 10)
        template = 'Asano 2015 {0} Categorical Observer No. {1} {2}'
        for index, observer in self.parse_workbook_Asano2015(
                workbook_path, template, observers).items():
            self._content['Categorical Observers'][index] = (
                Asano2015_Specification(
                    observer['XYZ_2'],
                    observer['XYZ_10'],
                    observer['LMS_2'],
                    observer['LMS_10'],
                    observer['parameters'],
                ))

        # Colour Normal Observers
        workbook_path = os.path.join(self.record.repository, 'dataset',
                                     'Data_151Obs.xls')

        observers = (1, 151)

        # Other Information
        column_in, column_out = (index_to_column(observers[0] - 1),
                                 index_to_column(observers[1]))
        workbook = xlrd.open_workbook(workbook_path)
        values = cell_range_values(
            workbook.sheet_by_index(5), '{0}2:{1}9'.format(
                column_in, column_out))
        values.extend(
            cell_range_values(
                workbook.sheet_by_index(5), '{0}12:{1}16'.format(
                    column_in, column_out)))
        values = np.transpose(values)
        header, values = values[0], values[1:]

        template = 'Asano 2015 {0} Colour Normal Observer No. {1} {2}'
        for i, (index, observer) in enumerate(
                self.parse_workbook_Asano2015(workbook_path, template,
                                              observers).items()):
            self._content['Colour Normal Observers'][index] = (
                Asano2015_Specification(
                    observer['XYZ_2'],
                    observer['XYZ_10'],
                    observer['LMS_2'],
                    observer['LMS_10'],
                    observer['parameters'],
                    OrderedDict(zip(header, values[i])),
                ))

        return self._content

    @staticmethod
    def parse_workbook_Asano2015(workbook, template, observers=(1, 10)):
        """
        Parses given *Asano (2015)* *Observer Function Database* workbook.

        Parameters
        ----------
        workbook : unicode
            *Asano (2015)* *Observer Function Database* workbook path.
        template : unicode
            Template used to create the *CMFS* names.
        observers : tuple, optional
            Observers range.

        Returns
        -------
        OrderedDict
            *Asano (2015)* *Observer Function Database* workbook observer data.
        """

        workbook = xlrd.open_workbook(workbook)

        # "CIE XYZ" and "LMS" CMFS.
        column_in, column_out = (index_to_column(observers[0] + 1),
                                 index_to_column(observers[1] + 1))

        shape = SpectralShape(390, 780, 5)
        wavelengths = shape.range()
        data = OrderedDict()

        for i, cmfs in enumerate([(XYZ_ColourMatchingFunctions, 'XYZ'),
                                  (LMS_ConeFundamentals, 'LMS')]):

            for j, degree in enumerate([(2, '2$^\\circ$'), (10,
                                                            '10$^\\circ$')]):

                sheet = workbook.sheet_by_index(j + (i * 2))

                x = np.transpose(
                    cell_range_values(
                        sheet, '{0}3:{1}81'.format(column_in, column_out)))
                y = np.transpose(
                    cell_range_values(
                        sheet, '{0}82:{1}160'.format(column_in, column_out)))
                z = np.transpose(
                    cell_range_values(
                        sheet, '{0}161:{1}239'.format(column_in, column_out)))

                for k in range(observers[1]):
                    observer = k + 1
                    rgb = tstack([x[k], y[k], z[k]])
                    if data.get(observer) is None:
                        data[observer] = OrderedDict()

                    key = '{0}_{1}'.format(cmfs[1], degree[0])
                    data[observer][key] = cmfs[0](
                        rgb,
                        domain=wavelengths,
                        name=template.format(degree[0], observer, cmfs[1]),
                        strict_name=template.format(degree[0], observer,
                                                    cmfs[1]))

        # Parameters
        column_in, column_out = (index_to_column(observers[0] - 1),
                                 index_to_column(observers[1]))

        values = np.transpose(
            cell_range_values(
                workbook.sheet_by_index(4), '{0}2:{1}10'.format(
                    column_in, column_out)))
        header, values = values[0], values[1:]

        for i in range(observers[1]):
            observer = i + 1
            data[observer]['parameters'] = OrderedDict(
                zip(header, as_float_array(values[i])))

        return data


_ASANO2015_DATASET_LOADER = None
"""
Singleton instance of the *Asano (2015)* *Observer Function Database* dataset
loader.

_ASANO2015_DATASET_LOADER : Asano2015DatasetLoader
"""


def build_Asano2015(load=True):
    """
    Singleton factory that the builds *Asano (2015)*
    *Observer Function Database* dataset loader.

    Parameters
    ----------
    load : bool, optional
        Whether to load the dataset upon instantiation.

    Returns
    -------
    Asano2015DatasetLoader
        Singleton instance of the *Asano (2015)*
        *Observer Function Database* dataset loader.

    References
    ----------
    :cite:`Asano2015`
    """

    global _ASANO2015_DATASET_LOADER

    if _ASANO2015_DATASET_LOADER is None:
        _ASANO2015_DATASET_LOADER = Asano2015DatasetLoader()
        if load:
            _ASANO2015_DATASET_LOADER.load()

    return _ASANO2015_DATASET_LOADER
