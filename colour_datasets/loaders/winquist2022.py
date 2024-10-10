"""
Physlight - Camera Spectral Sensitivity Curves - Winquist et al. (2022)
=======================================================================

Define the objects implementing support for *Winquist et al. (2022)*
*Physlight - Camera Spectral Sensitivity Curves* dataset loading:

-   :class:`colour_datasets.loaders.DatasetLoader_Winquist2022`
-   :func:`colour_datasets.loaders.build_Winquist2022`

References
----------
-   :cite:`Winquist2022` : Winquist, E., Thurston, K., & Weta Digital. (2022).
    Physlight - Camera Spectral Sensitivity Curves. Retrieved May 28, 2022,
    from https://github.com/quister/physlight/commit/\
20100bce85c75fb7389949508d319d640e5d2be3
"""

from __future__ import annotations

import glob
import os

from colour.hints import Dict

from colour_datasets.loaders import AbstractDatasetLoader
from colour_datasets.loaders.dyer2017 import MultiSpectralDistributions_AMPAS
from colour_datasets.records import datasets

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "DatasetLoader_Winquist2022",
    "build_Winquist2022",
]


class DatasetLoader_Winquist2022(AbstractDatasetLoader):
    """
    Define the *Winquist et al. (2022)*
    *Physlight - Camera Spectral Sensitivity Curves* dataset /loader.

    Attributes
    ----------
    ID

    Methods
    -------
    load

    References
    ----------
    :cite:`Winquist2022`
    """

    ID: str = "6590768"
    """Dataset record id, i.e., the *Zenodo* record number."""

    def __init__(self) -> None:
        super().__init__(datasets()[DatasetLoader_Winquist2022.ID])

    def load(self) -> Dict[str, MultiSpectralDistributions_AMPAS]:
        """
        Sync, parse, convert and return the *Winquist et al. (2022)*
        *Physlight - Camera Spectral Sensitivity Curves* dataset content.

        Returns
        -------
        :class:`dict`
            *Winquist et al. (2022)*
            *Physlight - Camera Spectral Sensitivity Curves* dataset content.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = DatasetLoader_Winquist2022()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.content.keys())
        17
        """

        super().sync()

        self._content = {}

        glob_pattern = os.path.join(self.record.repository, "dataset", "*.json")
        for path in glob.glob(glob_pattern):
            msds = MultiSpectralDistributions_AMPAS(path).read()
            self._content[msds.name] = msds

        return self._content


_DATASET_LOADER_WINQUIST2022: DatasetLoader_Winquist2022 | None = None
"""
Singleton instance of the *Winquist et al. (2022)*
*Physlight - Camera Spectral Sensitivity Curves* dataset loader.
"""


def build_Winquist2022(load: bool = True) -> DatasetLoader_Winquist2022:
    """
    Singleton factory that builds the *Winquist et al. (2022)*
    *Physlight - Camera Spectral Sensitivity Curves* dataset loader.

    Parameters
    ----------
    load
        Whether to load the dataset upon instantiation.

    Returns
    -------
    :class:`colour_datasets.loaders.DatasetLoader_Winquist2022`
        Singleton instance of the *Winquist et al. (2022)*
        *Physlight - Camera Spectral Sensitivity Curves* dataset loader.

    References
    ----------
    :cite:`Winquist2022`
    """

    global _DATASET_LOADER_WINQUIST2022  # noqa: PLW0603

    if _DATASET_LOADER_WINQUIST2022 is None:
        _DATASET_LOADER_WINQUIST2022 = DatasetLoader_Winquist2022()
        if load:
            _DATASET_LOADER_WINQUIST2022.load()

    return _DATASET_LOADER_WINQUIST2022
