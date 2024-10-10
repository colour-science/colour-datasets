"""
Spectral Sensitivity Database - Zhao et al. (2009)
==================================================

Define the objects implementing support for *Zhao, Kawakami, Tan and Ikeuchi
(2009)* *Spectral Sensitivity Database* dataset loading:

-   :class:`colour_datasets.loaders.DatasetLoader_Zhao2009`
-   :func:`colour_datasets.loaders.build_Zhao2009`

References
----------
-   :cite:`Zhao2009` : Zhao, H., Kawakami, R., Tan, R. T., & Ikeuchi, K.
    (2009). Estimating basis functions for spectral sensitivity of digital
    cameras.
"""

from __future__ import annotations

import os

import numpy as np
from colour.characterisation import RGB_CameraSensitivities
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
    "DatasetLoader_Zhao2009",
    "build_Zhao2009",
]


class DatasetLoader_Zhao2009(AbstractDatasetLoader):
    """
    Define the *Zhao et al. (2009)* *Spectral Sensitivity Database*
    dataset loader.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.DatasetLoader_Zhao2009.ID`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.DatasetLoader_Zhao2009.__init__`
    -   :meth:`colour_datasets.loaders.DatasetLoader_Zhao2009.load`

    References
    ----------
    :cite:`Zhao2009`
    """

    ID: str = "4297288"
    """Dataset record id, i.e., the *Zenodo* record number."""

    def __init__(self) -> None:
        super().__init__(datasets()[DatasetLoader_Zhao2009.ID])

    def load(self) -> Dict[str, RGB_CameraSensitivities]:
        """
        Sync, parse, convert and return the *Zhao et al. (2009)*
        *Spectral Sensitivity Database* dataset content.

        Returns
        -------
        :class:`dict`
            *Zhao et al. (2009)* *Spectral Sensitivity Database*
            dataset content.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = DatasetLoader_Zhao2009()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.content.keys())
        12
        """

        super().sync()

        cameras = [
            "SONY DXC 930",
            "KODAK DCS 420",
            "NIKON D1X",
            "SONY DXC 9000",
            "CANON 10D",
            "NIKON D70",
            "KODAK DCS 460",
            "CANON 400D",
            "CANON 5D",
            "CANON 5D Mark 2",
            "Ladybug2",
            "KODAK DCS 200",
        ]

        self._content = {}

        for i, camera in enumerate(cameras):
            data = np.loadtxt(
                os.path.join(self.record.repository, "dataset", f"camera_{i}.spectra")
            )
            self._content[camera] = RGB_CameraSensitivities(
                data[..., 1:], data[..., 0], name=camera
            )

        return self._content


_DATASET_LOADER_JIANG2009: DatasetLoader_Zhao2009 | None = None
"""
Singleton instance of the *Zhao et al. (2009)*
*Spectral Sensitivity Database* dataset loader.
"""


def build_Zhao2009(load: bool = True) -> DatasetLoader_Zhao2009:
    """
    Singleton factory that builds the *Zhao et al. (2009)*
    *Spectral Sensitivity Database* dataset loader.

    Parameters
    ----------
    load
        Whether to load the dataset upon instantiation.

    Returns
    -------
    :class:`colour_datasets.loaders.DatasetLoader_Zhao2009`
        Singleton instance of the *Zhao et al. (2009)*
        *Spectral Sensitivity Database* dataset loader.

    References
    ----------
    :cite:`Zhao2009`
    """

    global _DATASET_LOADER_JIANG2009  # noqa: PLW0603

    if _DATASET_LOADER_JIANG2009 is None:
        _DATASET_LOADER_JIANG2009 = DatasetLoader_Zhao2009()
        if load:
            _DATASET_LOADER_JIANG2009.load()

    return _DATASET_LOADER_JIANG2009
