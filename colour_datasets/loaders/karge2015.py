"""
Spectral Database of Commonly Used Cine Lighting - Karge et al. (2015)
======================================================================

Define the objects implementing support for *Karge, Froehlich and Eberhardt
(2015)* *Spectral Database of Commonly Used Cine Lighting* dataset loading:

-   :class:`colour_datasets.loaders.DatasetLoader_Karge2015`
-   :func:`colour_datasets.loaders.build_Karge2015`

References
----------
-   :cite:`Karge2015` : Karge, A., Froehlich, J., & Eberhardt, B. (2015). A
    Spectral Database of Commonly Used Cine Lighting. Color and Imaging
    Conference, 2015. https://www.researchgate.net/publication/\
282908037_A_Spectral_Database_of_Commonly_Used_Cine_Lighting
"""

from __future__ import annotations

import os
import re
from collections import defaultdict

from colour.algebra import LinearInterpolator
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
    "DatasetLoader_Karge2015",
    "build_Karge2015",
]


class DatasetLoader_Karge2015(AbstractDatasetLoader):
    """
    Define the *Karge et al. (2015)*
    *Spectral Database of Commonly Used Cine Lighting* dataset loader.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.DatasetLoader_Karge2015.ID`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.DatasetLoader_Karge2015.__init__`
    -   :meth:`colour_datasets.loaders.DatasetLoader_Karge2015.load`

    References
    ----------
    :cite:`Karge2015`
    """

    ID: str = "4642271"
    """Dataset record id, i.e., the *Zenodo* record number."""

    def __init__(self) -> None:
        super().__init__(datasets()[DatasetLoader_Karge2015.ID])

    def load(self) -> Dict[str, Dict[str, Dict]]:
        """
        Sync, parse, convert and return the *Karge et al. (2015)*
        *Spectral Database of Commonly Used Cine Lighting* dataset content.

        Returns
        -------
        :class:`dict`
            *Karge et al. (2015)*
            *Spectral Database of Commonly Used Cine Lighting* dataset content.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = DatasetLoader_Karge2015()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.content.keys())
        7
        """

        super().sync()

        self._content = defaultdict(lambda: defaultdict(dict))

        database_root = os.path.join(
            self.record.repository, "dataset", "OFTP_full-sample-package_v2"
        )
        for path in sorted(os.listdir(database_root)):
            if path.split("_")[0] not in ("Arri", "Bron", "CMT", "Dedolight"):
                continue

            type_ = (
                os.path.splitext(path)[0]
                .replace("_v2", "")
                .replace("_normalized", "")
                .replace("_", " ")
            )
            category = "Normalised" if "normalized" in path else "Raw"
            path = os.path.join(database_root, path)  # noqa: PLW2901

            sds = {}
            for name, sd in read_sds_from_csv_file(
                path, transpose=True, delimiter=";"
            ).items():
                if re.match("f\\d", name):
                    continue

                sd.interpolator = LinearInterpolator
                sds[name] = sd

            self._content[type_][category] = sds

        return dict(self._content)


_DATASET_LOADER_KARGE2015: DatasetLoader_Karge2015 | None = None
"""
Singleton instance of the *Karge et al. (2015)*
*Spectral Database of Commonly Used Cine Lighting* dataset loader.
"""


def build_Karge2015(load: bool = True) -> DatasetLoader_Karge2015:
    """
    Singleton factory that builds the *Karge et al. (2015)*
    *Spectral Database of Commonly Used Cine Lighting* dataset loader.

    Parameters
    ----------
    load
        Whether to load the dataset upon instantiation.

    Returns
    -------
    :class:`colour_datasets.loaders.DatasetLoader_Karge2015`
        Singleton instance of the *Karge et al. (2015)*
        *Spectral Database of Commonly Used Cine Lighting* dataset loader.

    References
    ----------
    :cite:`Karge2015`
    """

    global _DATASET_LOADER_KARGE2015  # noqa: PLW0603

    if _DATASET_LOADER_KARGE2015 is None:
        _DATASET_LOADER_KARGE2015 = DatasetLoader_Karge2015()
        if load:
            _DATASET_LOADER_KARGE2015.load()

    return _DATASET_LOADER_KARGE2015
