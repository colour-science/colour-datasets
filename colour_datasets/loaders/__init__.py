# -*- coding: utf-8 -*-

from __future__ import absolute_import

from colour.utilities import CaseInsensitiveMapping, warning

from colour_datasets.records import datasets

from .abstract import AbstractDatasetLoader
from .asano2015 import Asano2015DatasetLoader, build_Asano2015
from .jiang2013 import Jiang2013DatasetLoader, build_Jiang2013
from .labsphere2019 import Labsphere2019DatasetLoader, build_Labsphere2019
from .xrite2016 import XRite2016DatasetLoader, build_XRite2016

__all__ = ['AbstractDatasetLoader']
__all__ += ['Asano2015DatasetLoader', 'build_Asano2015']
__all__ += ['Jiang2013DatasetLoader', 'build_Jiang2013']
__all__ += ['Labsphere2019DatasetLoader', 'build_Labsphere2019']
__all__ += ['XRite2016DatasetLoader', 'build_XRite2016']

DATASET_LOADERS = CaseInsensitiveMapping({
    Asano2015DatasetLoader.ID: build_Asano2015,
    Jiang2013DatasetLoader.ID: build_Jiang2013,
    Labsphere2019DatasetLoader.ID: build_Labsphere2019,
    XRite2016DatasetLoader.ID: build_XRite2016,
})
DATASET_LOADERS.__doc__ = """
Dataset loaders ids and callables.

DATASET_LOADERS : CaseInsensitiveMapping
"""

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
    dataset : unicode
        Dataset id, i.e. the *Zenodo* record number or title.

    Returns
    -------
    object
        Dataset data.

    Examples
    --------
    >>> len(load('3245883').keys())
    28
    >>> len(load('Camera Spectral Sensitivity Database').keys())
    28
    """

    global _HAS_TITLE_KEYS

    if not _HAS_TITLE_KEYS:
        for key in list(DATASET_LOADERS.keys())[:]:
            title = datasets()[key].title
            if title in DATASET_LOADERS:
                warning('"{0}" key is already defined in the dataset loaders!'.
                        format(title))
            DATASET_LOADERS[title] = DATASET_LOADERS[key]
        _HAS_TITLE_KEYS = True

    return DATASET_LOADERS[dataset]().data


__all__ += ['DATASET_LOADERS', 'load']
