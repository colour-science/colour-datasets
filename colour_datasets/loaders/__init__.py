# -*- coding: utf-8 -*-

from __future__ import absolute_import

import six
import sys

from colour.utilities import CaseInsensitiveMapping, warning

from colour_datasets.records import datasets

from .abstract import AbstractDatasetLoader
from .asano2015 import DatasetLoader_Asano2015, build_Asano2015
from .brendel2020 import DatasetLoader_Brendel2020, build_Brendel2020
from .dyer2017 import DatasetLoader_Dyer2017, build_Dyer2017
from .ebner1998 import DatasetLoader_Ebner1998, build_Ebner1998
from .hung1995 import DatasetLoader_Hung1995, build_Hung1995
from .jakob2019 import DatasetLoader_Jakob2019, build_Jakob2019
from .jiang2013 import DatasetLoader_Jiang2013, build_Jiang2013
from .labsphere2019 import DatasetLoader_Labsphere2019, build_Labsphere2019
from .luo1999 import DatasetLoader_Luo1999, build_Luo1999
from .xrite2016 import DatasetLoader_XRite2016, build_XRite2016

__all__ = ['AbstractDatasetLoader']
__all__ += ['DatasetLoader_Asano2015', 'build_Asano2015']
__all__ += ['DatasetLoader_Brendel2020', 'build_Brendel2020']
__all__ += ['DatasetLoader_Dyer2017', 'build_Dyer2017']
__all__ += ['DatasetLoader_Ebner1998', 'build_Ebner1998']
__all__ += ['DatasetLoader_Hung1995', 'build_Hung1995']
__all__ += ['DatasetLoader_Jakob2019', 'build_Jakob2019']
__all__ += ['DatasetLoader_Jiang2013', 'build_Jiang2013']
__all__ += ['DatasetLoader_Labsphere2019', 'build_Labsphere2019']
__all__ += ['DatasetLoader_Luo1999', 'build_Luo1999']
__all__ += ['DatasetLoader_XRite2016', 'build_XRite2016']

DATASET_LOADERS = CaseInsensitiveMapping({
    DatasetLoader_Asano2015.ID: build_Asano2015,
    DatasetLoader_Brendel2020.ID: build_Brendel2020,
    DatasetLoader_Dyer2017.ID: build_Dyer2017,
    DatasetLoader_Ebner1998.ID: build_Ebner1998,
    DatasetLoader_Hung1995.ID: build_Hung1995,
    DatasetLoader_Jakob2019.ID: build_Jakob2019,
    DatasetLoader_Jiang2013.ID: build_Jiang2013,
    DatasetLoader_Labsphere2019.ID: build_Labsphere2019,
    DatasetLoader_Luo1999.ID: build_Luo1999,
    DatasetLoader_XRite2016.ID: build_XRite2016,
})
DATASET_LOADERS.__doc__ = """
Dataset loaders ids and callables.

DATASET_LOADERS : CaseInsensitiveMapping
"""

from .kuopio import DATASET_LOADERS_KUOPIO_UNIVERSITY  # noqa

DATASET_LOADERS.update(DATASET_LOADERS_KUOPIO_UNIVERSITY)

from . import kuopio  # noqa

_module = sys.modules['colour_datasets.loaders']

for _export in kuopio.__all__:
    if _export.startswith('DatasetLoader_') or _export.startswith('build_'):

        setattr(_module, _export, getattr(kuopio, _export))

        __all__ += [_export]

del _module, _export

_HAS_TITLE_KEYS = False
"""
Whether the :attr:`colour_datasets.loaders.DATASET_LOADERS` attribute has
been updated with dataset titles. This variable is used in the one time
initialisation step that ensures that datasets can also be loaded using their
titles.

_HAS_TITLE_KEYS : bool
"""


def load(dataset):
    """
    Loads given dataset: The dataset is pulled locally, i.e. synced if required
    and then its data is loaded.

    Parameters
    ----------
    dataset : unicode or int
        Dataset id, i.e. the *Zenodo* record number or title.

    Returns
    -------
    object
        Dataset data.

    Examples
    --------
    >>> len(load('3245883').keys())
    28
    >>> len(load(
    ...     'Camera Spectral Sensitivity Database - '
    ...     'Jiang et al. (2013)').keys())
    28
    """

    global _HAS_TITLE_KEYS

    if not _HAS_TITLE_KEYS:
        for key in list(DATASET_LOADERS.keys())[:]:
            dataset_loader = datasets().get(key)
            if not dataset_loader:
                continue

            title = dataset_loader.title
            if title in DATASET_LOADERS:
                warning('"{0}" key is already defined in the dataset loaders!'.
                        format(title))
            DATASET_LOADERS[title] = DATASET_LOADERS[key]
        _HAS_TITLE_KEYS = True

    return DATASET_LOADERS[six.text_type(dataset)]().content


__all__ += ['DATASET_LOADERS', 'load']
