"""
Prague Sky Model Datasets - Wilkie et al. (2021)
=================================================

Define the objects implementing support for *Wilkie et al. (2021)*
*Prague Sky Model* dataset loading:

-   :class:`colour_datasets.loaders.DatasetLoader_Wilkie2021`
-   :func:`colour_datasets.loaders.build_Wilkie2021`

References
----------
-   :cite:`Wilkie2021` : Wilkie, A., Vevoda, P., Bashford-Rogers, T.,
    Hosek, L., Iser, T., Kolarova, M., Rittig, T., & Krivanek, J. (2021).
    A fitted radiance and attenuation model for realistic atmospheres.
    ACM Transactions on Graphics (Proceedings of SIGGRAPH 2021), 40(4).
    doi:10.1145/3450626.3459758
-   :cite:`Vevoda2022` : Vevoda, P., Wilkie, A., & Krivanek, J. (2022).
    A wide spectral range sky radiance model. Computer Graphics Forum,
    43(1).
"""

from __future__ import annotations

import os
import typing

if typing.TYPE_CHECKING:
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
    "DatasetLoader_Wilkie2021",
    "build_Wilkie2021",
]

DATASET_FILES: Dict[str, str] = {
    "ground": "PragueSkyModelDatasetGround.dat",
    "full": "PragueSkyModelDatasetFull.dat",
    "swir": "PragueSkyModelDatasetSWIR.dat",
}
"""
Mapping of dataset variant names to filenames.
"""

GOOGLE_DRIVE_IDS: Dict[str, str] = {
    "1IflyFZTJxC_N298yXq_2GK4ycIsVJZk6": "PragueSkyModelDatasetGround.dat",
    "1IShL7T3umxGOEFvyYGQpHKMTneXEvyTM": "PragueSkyModelDatasetFull.dat",
    "1ZOizQCN6tH39JEwyX8KvAj7WEdX-EqJl": "PragueSkyModelDatasetSWIR.dat",
}
"""
Mapping of *Google Drive* file IDs to dataset filenames for post-sync renaming.
"""


class DatasetLoader_Wilkie2021(AbstractDatasetLoader):
    """
    Define the *Wilkie et al. (2021)* *Prague Sky Model* dataset loader.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.DatasetLoader_Wilkie2021.ID`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.DatasetLoader_Wilkie2021.__init__`
    -   :meth:`colour_datasets.loaders.DatasetLoader_Wilkie2021.load`

    References
    ----------
    :cite:`Wilkie2021`, :cite:`Vevoda2022`
    """

    ID: str = "19140728"
    """Dataset record id, i.e., the *Zenodo* record number."""

    def __init__(self) -> None:
        super().__init__(datasets()[DatasetLoader_Wilkie2021.ID])

    def load(self) -> Dict:
        """
        Sync, parse, convert and return the *Wilkie et al. (2021)*
        *Prague Sky Model* dataset content.

        Returns
        -------
        :class:`dict`
            *Wilkie et al. (2021)* *Prague Sky Model* dataset content,
            keyed by variant name (``"ground"``, ``"full"``, ``"swir"``).
            Values are :class:`SkyDataset_Wilkie2021` instances if
            ``colour >= 0.4.8`` is available, otherwise file paths.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = DatasetLoader_Wilkie2021()
        >>> with suppress_stdout():
        ...     dataset.load()  # doctest: +SKIP
        >>> sorted(dataset.content.keys())  # doctest: +SKIP
        ['full', 'ground', 'swir']
        """

        super().sync()

        # Rename files downloaded from *Google Drive* URLs whose query
        # string parameters are used as filenames.  Files pulled as
        # fallback from *Zenodo* already have proper names.
        dataset_path = os.path.join(self.record.repository, "dataset")
        if os.path.isdir(dataset_path):
            for entry in os.listdir(dataset_path):
                for drive_id, target_name in GOOGLE_DRIVE_IDS.items():
                    if drive_id in entry:
                        source = os.path.join(dataset_path, entry)
                        if os.path.isfile(source):
                            target = os.path.join(dataset_path, target_name)
                            if not os.path.isfile(target):
                                os.rename(source, target)
                        break

        try:
            from colour.phenomena.sky.wilkie2021 import (  # noqa: PLC0415
                SkyDataset_Wilkie2021,
            )
        except ImportError:
            SkyDataset_Wilkie2021 = None

        self._content = {}

        for variant, filename in DATASET_FILES.items():
            path = os.path.join(dataset_path, filename)
            if os.path.isfile(path):
                if SkyDataset_Wilkie2021 is not None:
                    self._content[variant] = SkyDataset_Wilkie2021(path)
                else:
                    self._content[variant] = path

        return self._content


_DATASET_LOADER_WILKIE2021: DatasetLoader_Wilkie2021 | None = None
"""
Singleton instance of the *Wilkie et al. (2021)*
*Prague Sky Model* dataset loader.
"""


def build_Wilkie2021(load: bool = True) -> DatasetLoader_Wilkie2021:
    """
    Singleton factory that builds the *Wilkie et al. (2021)*
    *Prague Sky Model* dataset loader.

    Parameters
    ----------
    load
        Whether to load the dataset upon instantiation.

    Returns
    -------
    :class:`colour_datasets.loaders.DatasetLoader_Wilkie2021`
        Singleton instance of the *Wilkie et al. (2021)*
        *Prague Sky Model* dataset loader.

    References
    ----------
    :cite:`Wilkie2021`, :cite:`Vevoda2022`
    """

    global _DATASET_LOADER_WILKIE2021  # noqa: PLW0603

    if _DATASET_LOADER_WILKIE2021 is None:
        _DATASET_LOADER_WILKIE2021 = DatasetLoader_Wilkie2021()
        if load:
            _DATASET_LOADER_WILKIE2021.load()

    return _DATASET_LOADER_WILKIE2021
