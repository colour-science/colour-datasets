from __future__ import annotations

import sys

from colour.hints import Any
from colour.utilities import CanonicalMapping, warning

from colour_datasets.records import datasets

from .abstract import AbstractDatasetLoader
from .asano2015 import DatasetLoader_Asano2015, build_Asano2015
from .brendel2020 import DatasetLoader_Brendel2020, build_Brendel2020
from .dyer2017 import DatasetLoader_Dyer2017, build_Dyer2017
from .ebner1998 import DatasetLoader_Ebner1998, build_Ebner1998
from .hung1995 import DatasetLoader_Hung1995, build_Hung1995
from .jakob2019 import DatasetLoader_Jakob2019, build_Jakob2019
from .jiang2013 import DatasetLoader_Jiang2013, build_Jiang2013
from .karge2015 import DatasetLoader_Karge2015, build_Karge2015
from .labsphere2019 import DatasetLoader_Labsphere2019, build_Labsphere2019
from .luo1997 import DatasetLoader_Luo1997, build_Luo1997
from .luo1999 import DatasetLoader_Luo1999, build_Luo1999
from .solomotav2023 import DatasetLoader_Solomotav2023, build_Solomotav2023
from .winquist2022 import DatasetLoader_Winquist2022, build_Winquist2022
from .xrite2016 import DatasetLoader_XRite2016, build_XRite2016
from .zhao2009 import DatasetLoader_Zhao2009, build_Zhao2009

__all__ = [
    "AbstractDatasetLoader",
]
__all__ += [
    "DatasetLoader_Asano2015",
    "build_Asano2015",
]
__all__ += [
    "DatasetLoader_Brendel2020",
    "build_Brendel2020",
]
__all__ += [
    "DatasetLoader_Dyer2017",
    "build_Dyer2017",
]
__all__ += [
    "DatasetLoader_Ebner1998",
    "build_Ebner1998",
]
__all__ += [
    "DatasetLoader_Hung1995",
    "build_Hung1995",
]
__all__ += [
    "DatasetLoader_Jakob2019",
    "build_Jakob2019",
]
__all__ += [
    "DatasetLoader_Jiang2013",
    "build_Jiang2013",
]
__all__ += [
    "DatasetLoader_Karge2015",
    "build_Karge2015",
]
__all__ += [
    "DatasetLoader_Labsphere2019",
    "build_Labsphere2019",
]
__all__ += [
    "DatasetLoader_Luo1997",
    "build_Luo1997",
]
__all__ += [
    "DatasetLoader_Luo1999",
    "build_Luo1999",
]
__all__ += [
    "DatasetLoader_Solomotav2023",
    "build_Solomotav2023",
]
__all__ += [
    "DatasetLoader_Winquist2022",
    "build_Winquist2022",
]
__all__ += [
    "DatasetLoader_XRite2016",
    "build_XRite2016",
]
__all__ += [
    "DatasetLoader_Zhao2009",
    "build_Zhao2009",
]

DATASET_LOADERS: CanonicalMapping = CanonicalMapping(
    {
        DatasetLoader_Asano2015.ID: build_Asano2015,
        DatasetLoader_Brendel2020.ID: build_Brendel2020,
        DatasetLoader_Dyer2017.ID: build_Dyer2017,
        DatasetLoader_Ebner1998.ID: build_Ebner1998,
        DatasetLoader_Hung1995.ID: build_Hung1995,
        DatasetLoader_Jakob2019.ID: build_Jakob2019,
        DatasetLoader_Jiang2013.ID: build_Jiang2013,
        DatasetLoader_Karge2015.ID: build_Karge2015,
        DatasetLoader_Labsphere2019.ID: build_Labsphere2019,
        DatasetLoader_Luo1997.ID: build_Luo1997,
        DatasetLoader_Luo1999.ID: build_Luo1999,
        DatasetLoader_Solomotav2023.ID: build_Solomotav2023,
        DatasetLoader_Winquist2022.ID: build_Winquist2022,
        DatasetLoader_XRite2016.ID: build_XRite2016,
        DatasetLoader_Zhao2009.ID: build_Zhao2009,
    }
)
DATASET_LOADERS.__doc__ = """
Dataset loaders ids and callables.
"""

from .kuopio import DATASET_LOADERS_KUOPIO_UNIVERSITY  # noqa: E402

DATASET_LOADERS.update(DATASET_LOADERS_KUOPIO_UNIVERSITY)

from . import kuopio  # noqa: E402

_module = sys.modules["colour_datasets.loaders"]

for _export in kuopio.__all__:
    if _export.startswith(("DatasetLoader_", "build_")):
        setattr(_module, _export, getattr(kuopio, _export))

        __all__ += [_export]  # noqa: PLE0604

del _module, _export

_HAS_TITLE_KEYS: bool = False
"""
Whether the :attr:`colour_datasets.loaders.DATASET_LOADERS` attribute has
been updated with dataset titles. This variable is used in the one time
initialisation step that ensures that datasets can also be loaded using their
titles.
"""


def load(dataset: int | str) -> Any:
    """
    Load given dataset: The dataset is pulled locally, i.e., synced if required
    and then its data is loaded.

    Parameters
    ----------
    dataset
        Dataset id, i.e., the *Zenodo* record number or title.

    Returns
    -------
    :class:`object`
        Dataset data.

    Examples
    --------
    >>> len(load("3245883").keys())  # doctest: +SKIP
    28
    >>> len(
    ...     load("Camera Spectral Sensitivity Database - " "Jiang et al. (2013)").keys()
    ... )
    ... # doctest: +SKIP
    28
    """

    global _HAS_TITLE_KEYS  # noqa: PLW0603

    if not _HAS_TITLE_KEYS:
        for key in list(DATASET_LOADERS.keys())[:]:
            dataset_loader = datasets().get(key)
            if not dataset_loader:
                continue

            title = dataset_loader.title
            if title in DATASET_LOADERS:
                warning(f'"{title}" key is already defined in the dataset loaders!')
            DATASET_LOADERS[title] = DATASET_LOADERS[key]
        _HAS_TITLE_KEYS = True

    return DATASET_LOADERS[str(dataset)]().content


__all__ += [
    "DATASET_LOADERS",
    "load",
]
