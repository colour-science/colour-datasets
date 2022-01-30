"""
Observer Function Database - Asano (2015)
=========================================

Defines the objects implementing support for *Asano (2015)* *Observer Function
Database* dataset loading:

-   :class:`colour_datasets.loaders.DatasetLoader_Asano2015`
-   :func:`colour_datasets.loaders.build_Asano2015`

References
----------
-   :cite:`Asano2015` : Asano, Y. (2015). Individual Colorimetric Observers for
    Personalized Color Imaging. R.I.T.
"""

import numpy as np
import os
import xlrd
from collections import namedtuple

from colour import SpectralShape
from colour.colorimetry import (
    XYZ_ColourMatchingFunctions,
    LMS_ConeFundamentals,
)
from colour.utilities import as_float_array, tstack

from colour_datasets.loaders import AbstractDatasetLoader
from colour_datasets.records import datasets
from colour_datasets.utilities import cell_range_values, index_to_column

__author__ = "Colour Developers"
__copyright__ = "Copyright (C) 2019-2021 - Colour Developers"
__license__ = "New BSD License - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "Specification_Asano2015",
    "DatasetLoader_Asano2015",
    "build_Asano2015",
]


class Specification_Asano2015(
    namedtuple(
        "Specification_Asano2015",
        ("XYZ_2", "XYZ_10", "LMS_2", "LMS_10", "parameters", "others"),
    )
):
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
        :class:`colour_datasets.loaders.asano2015.Specification_Asano2015`
        class.
        """

        return super().__new__(
            cls, XYZ_2, XYZ_10, LMS_2, LMS_10, parameters, others
        )


class DatasetLoader_Asano2015(AbstractDatasetLoader):
    """
    Defines the *Asano (2015)* *Observer Function Database* dataset loader.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.DatasetLoader_Asano2015.ID`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.DatasetLoader_Asano2015.__init__`
    -   :meth:`colour_datasets.loaders.DatasetLoader_Asano2015.load`
    -   :meth:`colour_datasets.loaders.DatasetLoader_Asano2015.\
parse_workbook_Asano2015`

    References
    ----------
    :cite:`Asano2015`
    """

    ID = "3252742"
    """
    Dataset record id, i.e. the *Zenodo* record number.

    ID : str
    """

    def __init__(self):
        super().__init__(datasets()[DatasetLoader_Asano2015.ID])

    def load(self):
        """
        Syncs, parses, converts and returns the *Asano (2015)*
        *Observer Function Database* dataset content.

        Returns
        -------
        dict
            *Asano (2015)* *Observer Function Database* dataset content.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = DatasetLoader_Asano2015()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.content.keys())
        2
        """

        super().sync()

        self._content = dict(
            [
                ("Categorical Observers", dict()),
                ("Colour Normal Observers", dict()),
            ]
        )

        # Categorical Observers
        workbook_path = os.path.join(
            self.record.repository, "dataset", "Data_10CatObs.xls"
        )

        observers = (1, 10)
        template = "Asano 2015 {0} Categorical Observer No. {1} {2}"
        for index, observer in self.parse_workbook_Asano2015(
            workbook_path, template, observers
        ).items():
            self._content["Categorical Observers"][
                index
            ] = Specification_Asano2015(
                observer["XYZ_2"],
                observer["XYZ_10"],
                observer["LMS_2"],
                observer["LMS_10"],
                observer["parameters"],
            )

        # Colour Normal Observers
        workbook_path = os.path.join(
            self.record.repository, "dataset", "Data_151Obs.xls"
        )

        observers = (1, 151)

        # Other Information
        column_in, column_out = (
            index_to_column(observers[0] - 1),
            index_to_column(observers[1]),
        )
        workbook = xlrd.open_workbook(workbook_path)
        values = cell_range_values(
            workbook.sheet_by_index(5), f"{column_in}2:{column_out}9"
        )
        values.extend(
            cell_range_values(
                workbook.sheet_by_index(5), f"{column_in}12:{column_out}16"
            )
        )
        values = np.transpose(values)
        header, values = values[0], values[1:]

        template = "Asano 2015 {0} Colour Normal Observer No. {1} {2}"
        for i, (index, observer) in enumerate(
            self.parse_workbook_Asano2015(
                workbook_path, template, observers
            ).items()
        ):
            self._content["Colour Normal Observers"][
                index
            ] = Specification_Asano2015(
                observer["XYZ_2"],
                observer["XYZ_10"],
                observer["LMS_2"],
                observer["LMS_10"],
                observer["parameters"],
                dict(zip(header, values[i])),
            )

        return self._content

    @staticmethod
    def parse_workbook_Asano2015(workbook, template, observers=(1, 10)):
        """
        Parses given *Asano (2015)* *Observer Function Database* workbook.

        Parameters
        ----------
        workbook : str
            *Asano (2015)* *Observer Function Database* workbook path.
        template : str
            Template used to create the *CMFS* names.
        observers : tuple, optional
            Observers range.

        Returns
        -------
        dict
            *Asano (2015)* *Observer Function Database* workbook observer data.
        """

        workbook = xlrd.open_workbook(workbook)

        # "CIE XYZ" and "LMS" CMFS.
        column_in, column_out = (
            index_to_column(observers[0] + 1),
            index_to_column(observers[1] + 1),
        )

        shape = SpectralShape(390, 780, 5)
        wavelengths = shape.range()
        data = dict()

        for i, cmfs in enumerate(
            [
                (XYZ_ColourMatchingFunctions, "XYZ"),
                (LMS_ConeFundamentals, "LMS"),
            ]
        ):

            for j, degree in enumerate(
                [(2, "2$^\\circ$"), (10, "10$^\\circ$")]
            ):

                sheet = workbook.sheet_by_index(j + (i * 2))

                x = np.transpose(
                    cell_range_values(sheet, f"{column_in}3:{column_out}81")
                )
                y = np.transpose(
                    cell_range_values(sheet, f"{column_in}82:{column_out}160")
                )
                z = np.transpose(
                    cell_range_values(sheet, f"{column_in}161:{column_out}239")
                )

                for k in range(observers[1]):
                    observer = k + 1
                    rgb = tstack([x[k], y[k], z[k]])
                    if data.get(observer) is None:
                        data[observer] = dict()

                    key = f"{cmfs[1]}_{degree[0]}"
                    data[observer][key] = cmfs[0](
                        rgb,
                        domain=wavelengths,
                        name=template.format(degree[0], observer, cmfs[1]),
                        strict_name=template.format(
                            degree[0], observer, cmfs[1]
                        ),
                    )

        # Parameters
        column_in, column_out = (
            index_to_column(observers[0] - 1),
            index_to_column(observers[1]),
        )

        values = np.transpose(
            cell_range_values(
                workbook.sheet_by_index(4), f"{column_in}2:{column_out}10"
            )
        )
        header, values = values[0], values[1:]

        for i in range(observers[1]):
            observer = i + 1
            data[observer]["parameters"] = dict(
                zip(header, as_float_array(values[i]))
            )

        return data


_DATASET_LOADER_ASANO2015 = None
"""
Singleton instance of the *Asano (2015)* *Observer Function Database* dataset
loader.

_DATASET_LOADER_ASANO2015 : DatasetLoader_Asano2015
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
    DatasetLoader_Asano2015
        Singleton instance of the *Asano (2015)*
        *Observer Function Database* dataset loader.

    References
    ----------
    :cite:`Asano2015`
    """

    global _DATASET_LOADER_ASANO2015

    if _DATASET_LOADER_ASANO2015 is None:
        _DATASET_LOADER_ASANO2015 = DatasetLoader_Asano2015()
        if load:
            _DATASET_LOADER_ASANO2015.load()

    return _DATASET_LOADER_ASANO2015
