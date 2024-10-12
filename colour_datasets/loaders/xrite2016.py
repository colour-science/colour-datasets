"""
New Color Specifications for ColorChecker SG and Classic Charts - X-Rite (2016)
===============================================================================

Define the objects implementing support for *X-Rite (2016)* *New Color
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

from __future__ import annotations

import codecs
import os

import numpy as np
from colour import CCS_ILLUMINANTS, Lab_to_XYZ, XYZ_to_xyY
from colour.characterisation import ColourChecker
from colour.hints import Dict

from colour_datasets.loaders import AbstractDatasetLoader
from colour_datasets.records import datasets

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "DatasetLoader_XRite2016",
    "build_XRite2016",
]


class DatasetLoader_XRite2016(AbstractDatasetLoader):
    """
    Define the *X-Rite (2016)*
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

    ID: str = "3245895"
    """Dataset record id, i.e., the *Zenodo* record number."""

    def __init__(self) -> None:
        super().__init__(datasets()[DatasetLoader_XRite2016.ID])

    def load(self) -> Dict[str, ColourChecker]:
        """
        Sync, parse, convert and return the *X-Rite (2016)*
        *New Color Specifications for ColorChecker SG and Classic Charts*
        dataset content.

        Returns
        -------
        :class:`dict`
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

        super().sync()

        keys = (
            "ColorChecker24 - After November 2014",
            "ColorChecker24 - Before November 2014",
            "ColorCheckerSG - After November 2014",
            "ColorCheckerSG - Before November 2014",
        )
        filenames = (
            "ColorChecker24_After_Nov2014.txt",
            "ColorChecker24_Before_Nov2014.txt",
            "ColorCheckerSG_After_Nov2014.txt",
            "ColorCheckerSG_Before_Nov2014.txt",
        )

        # TODO: Implement support for "CGATS" file format in "Colour":
        # https://github.com/colour-science/colour/issues/354
        illuminant = CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["ICC D50"]

        self._content = {}
        for key, filename in zip(keys, filenames):
            directory = os.path.splitext(filename)[0]
            path = os.path.join(self.record.repository, "dataset", directory, filename)

            with codecs.open(path, encoding="utf-8") as xrite_file:
                samples_data = []
                is_data = False
                lines = filter(None, (line.strip() for line in xrite_file.readlines()))
                for line in lines:
                    if line == "END_DATA":
                        is_data = False

                    if is_data:
                        tokens = line.split()
                        samples_data.append(
                            [
                                tokens[0],
                                [
                                    float(value.replace(",", "."))
                                    for value in tokens[1:]
                                ],
                            ]
                        )

                    if line == "BEGIN_DATA":
                        is_data = True

            i, j = (6, 4) if len(samples_data) == 24 else (14, 10)
            samples = np.transpose(
                np.reshape(np.array(samples_data, dtype=object), (i, j, 2)),
                [1, 0, 2],
            )
            keys, values = zip(*np.reshape(samples, (-1, 2)))
            values = XYZ_to_xyY(Lab_to_XYZ(values, illuminant))
            self._content[key] = ColourChecker(
                key, dict(zip(keys, values)), illuminant, j, i
            )

        return self._content


_DATASET_LOADER_XRITE2016: DatasetLoader_XRite2016 | None = None
"""
Singleton instance of the *X-Rite (2016)*
*New Color Specifications for ColorChecker SG and Classic Charts* dataset
loader.
"""


def build_XRite2016(load: bool = True) -> DatasetLoader_XRite2016:
    """
    Singleton factory that the builds *X-Rite (2016)*
    *New Color Specifications for ColorChecker SG and Classic Charts* dataset
    loader.

    Parameters
    ----------
    load
        Whether to load the dataset upon instantiation.

    Returns
    -------
    :class:`colour_datasets.loaders.DatasetLoader_XRite2016`
        Singleton instance of the *X-Rite (2016)*
        *New Color Specifications for ColorChecker SG and Classic Charts*
        dataset loader.

    References
    ----------
    :cite:`X-Rite2016`
    """

    global _DATASET_LOADER_XRITE2016  # noqa: PLW0603

    if _DATASET_LOADER_XRITE2016 is None:
        _DATASET_LOADER_XRITE2016 = DatasetLoader_XRite2016()
        if load:
            _DATASET_LOADER_XRITE2016.load()

    return _DATASET_LOADER_XRITE2016
