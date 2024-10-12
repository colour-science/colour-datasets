"""
Measured Commercial LED Spectra - Brendel (2020)
================================================

Define the objects implementing support for *Brendel (2020)*
*Measured Commercial LED Spectra* dataset loading:

-   :class:`colour_datasets.loaders.DatasetLoader_Brendel2020`
-   :func:`colour_datasets.loaders.build_Brendel2020`

References
----------
-   :cite:`Brendel2020` : Brendel, H. (2020). Measured Commercial LED Spectra.
    Retrieved September 26, 2020, from
    https://haraldbrendel.com/files/led_spd_350_700.csv
"""

from __future__ import annotations

import os

import numpy as np
from colour import LinearInterpolator, SpectralDistribution, SpectralShape
from colour.hints import Dict
from colour.utilities import as_int

from colour_datasets.loaders import AbstractDatasetLoader
from colour_datasets.records import datasets

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "DatasetLoader_Brendel2020",
    "build_Brendel2020",
]


class DatasetLoader_Brendel2020(AbstractDatasetLoader):
    """
    Define the *Brendel (2020)* *Measured Commercial LED Spectra* dataset
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

    ID: str = "4051012"
    """Dataset record id, i.e., the *Zenodo* record number."""

    def __init__(self) -> None:
        super().__init__(datasets()[DatasetLoader_Brendel2020.ID])

    def load(self) -> Dict[str, SpectralDistribution]:
        """
        Sync, parse, convert and return the *Brendel (2020)*
        *Measured Commercial LED Spectra* dataset content.

        Returns
        -------
        :class:`dict`
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

        super().sync()

        self._content = {}

        wavelengths = SpectralShape(350, 700, 2).range()

        csv_path = os.path.join(
            self.record.repository, "dataset", "led_spd_350_700.csv"
        )

        for i, values in enumerate(np.loadtxt(csv_path, delimiter=",", skiprows=1)):
            peak = as_int(wavelengths[np.argmax(values)])
            name = f"{peak}nm - LED {i} - Brendel (2020)"

            self._content[name] = SpectralDistribution(
                values, wavelengths, name=name, interpolator=LinearInterpolator
            )

        return self._content


_DATASET_LOADER_BRENDEL2020: DatasetLoader_Brendel2020 | None = None
"""
Singleton instance of the *Brendel (2020)* *Measured Commercial LED Spectra*
dataset loader.
"""


def build_Brendel2020(load: bool = True) -> DatasetLoader_Brendel2020:
    """
    Singleton factory that builds the *Brendel (2020)*
    *Measured Commercial LED Spectra* dataset loader.

    Parameters
    ----------
    load
        Whether to load the dataset upon instantiation.

    Returns
    -------
    :class:`colour_datasets.loaders.DatasetLoader_Brendel2020`
        Singleton instance of the *Brendel (2020)*
        *Measured Commercial LED Spectra* dataset loader.

    References
    ----------
    :cite:`Brendel2020`
    """

    global _DATASET_LOADER_BRENDEL2020  # noqa: PLW0603

    if _DATASET_LOADER_BRENDEL2020 is None:
        _DATASET_LOADER_BRENDEL2020 = DatasetLoader_Brendel2020()
        if load:
            _DATASET_LOADER_BRENDEL2020.load()

    return _DATASET_LOADER_BRENDEL2020
