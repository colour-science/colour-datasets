"""
Observer Function Database - Asano (2015)
=========================================

Define the objects implementing support for *Asano (2015)* *Observer Function
Database* dataset loading:

-   :class:`colour_datasets.loaders.DatasetLoader_Asano2015`
-   :func:`colour_datasets.loaders.build_Asano2015`

References
----------
-   :cite:`Asano2015` : Asano, Y. (2015). Individual Colorimetric Observers for
    Personalized Color Imaging. R.I.T.
"""

from __future__ import annotations

import os
from collections import namedtuple

import numpy as np
import xlrd
from colour import SpectralShape
from colour.colorimetry import (
    LMS_ConeFundamentals,
    XYZ_ColourMatchingFunctions,
)
from colour.hints import Dict, NDArrayFloat
from colour.utilities import as_float_array, tstack

from colour_datasets.loaders import AbstractDatasetLoader
from colour_datasets.records import datasets
from colour_datasets.utilities import cell_range_values, index_to_column

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
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
    Define the *Asano (2015)* specification for an observer.

    Parameters
    ----------
    XYZ_2
        *CIE XYZ* 2 degree colour matching functions.
    XYZ_10
        *CIE XYZ* 10 degree colour matching functions.
    LMS_2
        *LMS* 2 degree cone fundamentals.
    LMS_10
        *LMS* 10 degree cone fundamentals.
    parameters
        Observer parameters.
    others
        Other information.

    References
    ----------
    :cite:`Asano2015`
    """  # noqa: D405, D407, D410, D411

    def __new__(
        cls,
        XYZ_2: XYZ_ColourMatchingFunctions,
        XYZ_10: XYZ_ColourMatchingFunctions,
        LMS_2: LMS_ConeFundamentals,
        LMS_10: LMS_ConeFundamentals,
        parameters: NDArrayFloat,
        others: Dict | None = None,
    ):
        """
        Return a new instance of the
        :class:`colour_datasets.loaders.asano2015.Specification_Asano2015`
        class.
        """

        return super().__new__(cls, XYZ_2, XYZ_10, LMS_2, LMS_10, parameters, others)


class DatasetLoader_Asano2015(AbstractDatasetLoader):
    """
    Define the *Asano (2015)* *Observer Function Database* dataset loader.

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

    ID: str = "3252742"
    """Dataset record id, i.e., the *Zenodo* record number."""

    def __init__(self) -> None:
        super().__init__(datasets()[DatasetLoader_Asano2015.ID])

    def load(self) -> Dict[str, Dict[int, Specification_Asano2015]]:
        """
        Sync, parse, convert and return the *Asano (2015)*
        *Observer Function Database* dataset content.

        Returns
        -------
        :class:`dict`
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

        self._content = {
            "Categorical Observers": {},
            "Colour Normal Observers": {},
        }

        # Categorical Observers
        workbook_path = os.path.join(
            self.record.repository, "dataset", "Data_10CatObs.xls"
        )

        observers = (1, 10)
        template = "Asano 2015 {0} Categorical Observer No. {1} {2}"
        for index, observer in self.parse_workbook_Asano2015(
            workbook_path, template, observers
        ).items():
            self._content["Categorical Observers"][index] = Specification_Asano2015(
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
        values_data = cell_range_values(
            workbook.sheet_by_index(5), f"{column_in}2:{column_out}9"
        )
        values_data.extend(
            cell_range_values(
                workbook.sheet_by_index(5), f"{column_in}12:{column_out}16"
            )
        )
        values_transposed = np.transpose(values_data)
        header, values = values_transposed[0], values_transposed[1:]

        template = "Asano 2015 {0} Colour Normal Observer No. {1} {2}"
        for i, (index, observer) in enumerate(
            self.parse_workbook_Asano2015(workbook_path, template, observers).items()
        ):
            self._content["Colour Normal Observers"][index] = Specification_Asano2015(
                observer["XYZ_2"],
                observer["XYZ_10"],
                observer["LMS_2"],
                observer["LMS_10"],
                observer["parameters"],
                dict(zip(header, values[i])),
            )

        return self._content

    @staticmethod
    def parse_workbook_Asano2015(
        workbook: str, template: str, observers: tuple = (1, 10)
    ) -> Dict[str, Dict]:
        """
        Parse given *Asano (2015)* *Observer Function Database* workbook.

        Parameters
        ----------
        workbook
            *Asano (2015)* *Observer Function Database* workbook path.
        template
            Template used to create the *CMFS* names.
        observers
            Observers range.

        Returns
        -------
        :class:`dict`
            *Asano (2015)* *Observer Function Database* workbook observer data.
        """

        book = xlrd.open_workbook(workbook)

        # "CIE XYZ" and "LMS" CMFS.
        column_in, column_out = (
            index_to_column(observers[0] + 1),
            index_to_column(observers[1] + 1),
        )

        shape = SpectralShape(390, 780, 5)
        wavelengths = shape.range()
        data: Dict = {}

        for i, cmfs in enumerate(
            [
                (XYZ_ColourMatchingFunctions, "XYZ"),
                (LMS_ConeFundamentals, "LMS"),
            ]
        ):
            for j, degree in enumerate([(2, "2$^\\circ$"), (10, "10$^\\circ$")]):
                sheet = book.sheet_by_index(j + (i * 2))

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
                        data[observer] = {}

                    key = f"{cmfs[1]}_{degree[0]}"
                    data[observer][key] = cmfs[0](
                        rgb,
                        domain=wavelengths,
                        name=template.format(degree[0], observer, cmfs[1]),
                        display_name=template.format(degree[0], observer, cmfs[1]),
                    )

        # Parameters
        column_in, column_out = (
            index_to_column(observers[0] - 1),
            index_to_column(observers[1]),
        )

        values = np.transpose(
            cell_range_values(book.sheet_by_index(4), f"{column_in}2:{column_out}10")
        )
        header, values = values[0], values[1:]

        for i in range(observers[1]):
            observer = i + 1
            data[observer]["parameters"] = dict(zip(header, as_float_array(values[i])))

        return data


_DATASET_LOADER_ASANO2015: DatasetLoader_Asano2015 | None = None
"""
Singleton instance of the *Asano (2015)* *Observer Function Database* dataset
loader.
"""


def build_Asano2015(load: bool = True) -> DatasetLoader_Asano2015:
    """
    Singleton factory that the builds *Asano (2015)*
    *Observer Function Database* dataset loader.

    Parameters
    ----------
    load
        Whether to load the dataset upon instantiation.

    Returns
    -------
    :class:`colour_datasets.loaders.DatasetLoader_Asano2015`
        Singleton instance of the *Asano (2015)* *Observer Function Database*
        dataset loader.

    References
    ----------
    :cite:`Asano2015`
    """

    global _DATASET_LOADER_ASANO2015  # noqa: PLW0603

    if _DATASET_LOADER_ASANO2015 is None:
        _DATASET_LOADER_ASANO2015 = DatasetLoader_Asano2015()
        if load:
            _DATASET_LOADER_ASANO2015.load()

    return _DATASET_LOADER_ASANO2015


if __name__ == "__main__":
    import colour_datasets

    colour_datasets.load("3252742")
