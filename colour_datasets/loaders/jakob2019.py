"""
Spectral Upsampling Coefficient Tables - Jakob and Hanika (2019)
================================================================

Define the objects implementing support for *Jakob and Hanika (2019)*
*Spectral Upsampling Coefficient Tables* dataset loading:

-   :class:`colour_datasets.loaders.DatasetLoader_Jakob2019`
-   :func:`colour_datasets.loaders.build_Jakob2019`

References
----------
-   :cite:`Jakob2019` : Jakob, W., & Hanika, J. (2019). A Low-Dimensional
    Function Space for Efficient Spectral Upsampling. Computer Graphics Forum,
    38(2), 147-155. doi:10.1111/cgf.13626
"""

from __future__ import annotations

import glob
import os

from colour.hints import Dict
from colour.recovery import LUT3D_Jakob2019

from colour_datasets.loaders import AbstractDatasetLoader
from colour_datasets.records import datasets

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "DatasetLoader_Jakob2019",
    "build_Jakob2019",
]


class DatasetLoader_Jakob2019(AbstractDatasetLoader):
    """
    Define the *Jakob and Hanika (2019)*
    *Spectral Upsampling Coefficient Tables* dataset loader.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.DatasetLoader_Jakob2019.ID`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.DatasetLoader_Jakob2019.__init__`
    -   :meth:`colour_datasets.loaders.DatasetLoader_Jakob2019.load`

    References
    ----------
    :cite:`Jakob2019`
    """

    ID: str = "4050598"
    """Dataset record id, i.e., the *Zenodo* record number."""

    def __init__(self) -> None:
        super().__init__(datasets()[DatasetLoader_Jakob2019.ID])

    def load(self) -> Dict[str, LUT3D_Jakob2019]:
        """
        Sync, parse, convert and return the *Jakob and Hanika (2019)*
        *Spectral Upsampling Coefficient Tables* dataset content.

        Returns
        -------
        :class:`dict`
            *Jakob and Hanika (2019)* *Spectral Upsampling Coefficient Tables*
            dataset content.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = DatasetLoader_Jakob2019()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.content.keys())
        4
        """

        super().sync()

        self._content = {}

        tables_path = os.path.join(
            self.record.repository,
            "dataset",
            "Jakob2019Spectral",
            "supplement",
            "tables",
        )

        coeff_file_to_RGB_colourspace = {
            "rec2020": "ITU-R BT.2020",
            "srgb": "sRGB",
            "aces2065_1": "ACES2065-1",
            "prophotorgb": "ProPhoto RGB",
        }

        for coeff_file in glob.glob(f"{tables_path}/*.coeff"):
            key = os.path.splitext(os.path.basename(coeff_file))[0]
            key = coeff_file_to_RGB_colourspace.get(key, key)

            LUT = LUT3D_Jakob2019()
            LUT.read(coeff_file)

            self._content[key] = LUT

        return self._content


_DATASET_LOADER_JAKOB2019: DatasetLoader_Jakob2019 | None = None
"""
Singleton instance of the *Jakob and Hanika (2019)*
*Spectral Upsampling Coefficient Tables* dataset loader.
"""


def build_Jakob2019(load: bool = True) -> DatasetLoader_Jakob2019:
    """
    Singleton factory that builds the *Jakob and Hanika (2019)*
    *Spectral Upsampling Coefficient Tables* dataset loader.

    Parameters
    ----------
    load
        Whether to load the dataset upon instantiation.

    Returns
    -------
    :class:`colour_datasets.loaders.DatasetLoader_Jakob2019`
        Singleton instance of the *Jakob and Hanika (2019)*
        *Spectral Upsampling Coefficient Tables* dataset loader.

    References
    ----------
    :cite:`Jakob2019`
    """

    global _DATASET_LOADER_JAKOB2019  # noqa: PLW0603

    if _DATASET_LOADER_JAKOB2019 is None:
        _DATASET_LOADER_JAKOB2019 = DatasetLoader_Jakob2019()
        if load:
            _DATASET_LOADER_JAKOB2019.load()

    return _DATASET_LOADER_JAKOB2019
