"""
Camera Dataset - Solomatov and Akkaynak (2023)
==============================================

Define the objects implementing support for *Solomatov and Akkaynak (2023)*
*Camera Dataset* dataset loading:

-   :class:`colour_datasets.loaders.DatasetLoader_Solomotav2023`
-   :func:`colour_datasets.loaders.build_Solomotav2023`

References
----------
-   :cite:`Solomotav2023` : Solomatov, G., & Akkaynak, D. (2023, July).
    Spectral sensitivity estimation without a camera. IEEE International
    Conference on Computational Photography (ICCP).
"""

from __future__ import annotations

import glob
import os

from colour.characterisation import RGB_CameraSensitivities
from colour.hints import Dict
from colour.io import read_sds_from_csv_file

from colour_datasets.loaders import AbstractDatasetLoader
from colour_datasets.records import datasets

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "DatasetLoader_Solomotav2023",
    "build_Solomotav2023",
]


class DatasetLoader_Solomotav2023(AbstractDatasetLoader):
    """
    Define the *Solomatov and Akkaynak (2023)* *Camera Dataset* dataset loader.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.DatasetLoader_Solomotav2023.ID`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.DatasetLoader_Solomotav2023.__init__`
    -   :meth:`colour_datasets.loaders.DatasetLoader_Solomotav2023.load`

    References
    ----------
    :cite:`Solomotav2023`
    """

    ID: str = "8314702"
    """Dataset record id, i.e., the *Zenodo* record number."""

    def __init__(self) -> None:
        super().__init__(datasets()[DatasetLoader_Solomotav2023.ID])

    def load(self) -> Dict[str, Dict[str, RGB_CameraSensitivities]]:
        """
        Sync, parse, convert and return the *Solomatov and Akkaynak (2023)*
        *Camera Dataset* dataset content.

        Returns
        -------
        :class:`dict`
            *Solomatov and Akkaynak (2023)* *Camera Dataset*
            dataset content.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = DatasetLoader_Solomotav2023()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.content.keys())
        2
        >>> len(dataset.content["Estimated"].keys())
        1012
        """

        super().sync()

        self._content = {"Estimated": {}, "Ground Truth": {}}

        for key, path in [
            ("Estimated", "csv"),
            ("Ground Truth", "ground-truths"),
        ]:
            csv_files = glob.glob(
                f'{os.path.join(self.record.repository, "dataset", path, path)}/'
                f"*.csv"
            )
            for csv_file in csv_files:
                camera_name = os.path.splitext(os.path.basename(csv_file))[0].replace(
                    "-", " "
                )
                self._content[key][camera_name] = RGB_CameraSensitivities(
                    read_sds_from_csv_file(csv_file), name=camera_name
                )

        return self._content


_DATASET_LOADER_SOLOMOTAV2023: DatasetLoader_Solomotav2023 | None = None
"""
Singleton instance of the *Solomatov and Akkaynak (2023)*
*Camera Dataset* dataset loader.
"""


def build_Solomotav2023(load: bool = True) -> DatasetLoader_Solomotav2023:
    """
    Singleton factory that builds the *Solomatov and Akkaynak (2023)*
    *Camera Dataset* dataset loader.

    Parameters
    ----------
    load
        Whether to load the dataset upon instantiation.

    Returns
    -------
    :class:`colour_datasets.loaders.DatasetLoader_Solomotav2023`
        Singleton instance of the *Solomatov and Akkaynak (2023)*
        *Camera Dataset* dataset loader.

    References
    ----------
    :cite:`Solomotav2023`
    """

    global _DATASET_LOADER_SOLOMOTAV2023  # noqa: PLW0603

    if _DATASET_LOADER_SOLOMOTAV2023 is None:
        _DATASET_LOADER_SOLOMOTAV2023 = DatasetLoader_Solomotav2023()
        if load:
            _DATASET_LOADER_SOLOMOTAV2023.load()

    return _DATASET_LOADER_SOLOMOTAV2023
