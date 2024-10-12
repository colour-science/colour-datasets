"""
Constant Perceived-Hue Data - Ebner and Fairchild (1998)
========================================================

Define the objects implementing support for *Ebner and Fairchild (1998)*
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

from __future__ import annotations

import codecs
import os
from collections import namedtuple

import numpy as np
from colour.hints import Dict, NDArrayFloat
from colour.utilities import as_float_array

from colour_datasets.loaders import AbstractDatasetLoader
from colour_datasets.records import datasets

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "ConstantPerceivedHueColourMatches_Ebner1998",
    "DatasetLoader_Ebner1998",
    "build_Ebner1998",
]


class ConstantPerceivedHueColourMatches_Ebner1998(
    namedtuple(
        "ConstantPerceivedHueColourMatches_Ebner1998",
        ("name", "XYZ_r", "XYZ_cr", "XYZ_ct", "metadata"),
    )
):
    """
    Define *Ebner and Fairchild (1998)* *Constant Perceived-Hue Data*
    colour matches data for a given hue angle.

    Parameters
    ----------
    name
        *Ebner and Fairchild (1998)* *Constant Perceived-Hue Data* hue angle or
        name.
    XYZ_r
        *CIE XYZ* tristimulus values of the reference illuminant.
    XYZ_cr
        *CIE XYZ* tristimulus values of the reference colour under the
        reference illuminant.
    XYZ_ct
        *CIE XYZ* tristimulus values of the colour matches under the reference
        illuminant.
    metadata
        Dataset metadata.
    """


class DatasetLoader_Ebner1998(AbstractDatasetLoader):
    """
    Define the *Ebner and Fairchild (1998)* *Constant Perceived-Hue Data*
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

    ID: str = "3362536"
    """Dataset record id, i.e., the *Zenodo* record number."""

    def __init__(self) -> None:
        super().__init__(datasets()[DatasetLoader_Ebner1998.ID])

    def load(
        self,
    ) -> Dict[str, Dict[int, ConstantPerceivedHueColourMatches_Ebner1998]]:
        """
        Sync, parse, convert and return the *Ebner and Fairchild (1998)*
        *Constant Perceived-Hue Data* dataset content.

        Returns
        -------
        :class:`dict`
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

        super().sync()

        self._content = {"Constant Perceived-Hue Data": {}}

        datafile_path = os.path.join(
            self.record.repository, "dataset", "Ebner_Constant_Hue_Data.txt"
        )

        def _parse_float_values(data: str) -> NDArrayFloat:
            """Parse float values from given data."""

            values = np.reshape(
                as_float_array([float(x) / 100 for x in data.split("\t") if x]),
                (-1, 3),
            )

            return np.squeeze(values)

        with codecs.open(datafile_path, encoding="utf-8") as database_file:
            lines = filter(None, (line.strip() for line in database_file.readlines()))

            for line in lines:
                if line.startswith("White Point"):
                    XYZ_r = _parse_float_values(line.split(":")[-1])
                elif line.startswith("reference hue"):
                    line = line.replace("reference hue ", "")  # noqa: PLW2901
                    attribute, value = line.split("\t", 1)
                    hue, data = int(attribute), _parse_float_values(value)

                    self._content["Constant Perceived-Hue Data"][
                        hue
                    ] = ConstantPerceivedHueColourMatches_Ebner1998(
                        f"Reference Hue Angle - {hue}",
                        XYZ_r,
                        data[0],
                        data[1:],
                        {"h": hue},
                    )

        return self._content


_DATASET_LOADER_EBNER1998: DatasetLoader_Ebner1998 | None = None
"""
Singleton instance of the *Ebner and Fairchild (1998)*
*Constant Perceived-Hue Data* dataset loader.
"""


def build_Ebner1998(load: bool = True) -> DatasetLoader_Ebner1998:
    """
    Singleton factory that builds the *Ebner and Fairchild (1998)*
    *Constant Perceived-Hue Data* dataset loader.

    Parameters
    ----------
    load
        Whether to load the dataset upon instantiation.

    Returns
    -------
    :class:`colour_datasets.loaders.DatasetLoader_Ebner1998`
        Singleton instance of the *Ebner and Fairchild (1998)*
        *Constant Perceived-Hue Data* dataset loader.

    References
    ----------
    :cite:`Ebner1998`
    """

    global _DATASET_LOADER_EBNER1998  # noqa: PLW0603

    if _DATASET_LOADER_EBNER1998 is None:
        _DATASET_LOADER_EBNER1998 = DatasetLoader_Ebner1998()
        if load:
            _DATASET_LOADER_EBNER1998.load()

    return _DATASET_LOADER_EBNER1998
