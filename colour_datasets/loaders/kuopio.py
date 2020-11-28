# -*- coding: utf-8 -*-
"""
University of Kuopio
====================

Defines the objects implementing support for the *University of Kuopio*
datasets loading:

-   :class:`colour_datasets.loaders.DatasetLoader_KuopioUniversity`
-   :func:`colour_datasets.loaders.build_KuopioUniversity`

Notes
----
-   The various *University of Kuopio* datasets loading classes are built at
    module import time.

References
----------
-   :cite:`Haanpalo` : Haanpalo, J., & University of Kuopio. (n.d.). Munsell
    Colors Glossy (Spectrofotometer Measured). doi:10.5281/zenodo.3269916
-   :cite:`Haanpaloa` : Haanpalo, J., & University of Kuopio. (n.d.). Paper
    Spectra. doi:10.5281/zenodo.3269922
-   :cite:`Hauta-Kasari` : Hauta-Kasari, M., & University of Kuopio. (n.d.).
    Munsell Colors Matt (Spectrofotometer Measured). doi:10.5281/zenodo.3269912
-   :cite:`Hauta-Kasaria` : Hauta-Kasari, M., & University of Kuopio. (n.d.).
    Munsell Colors Matt (AOTF Measured). doi:10.5281/zenodo.3269914
-   :cite:`Hiltunen` : Hiltunen, J., & University of Kuopio. (n.d.). Lumber
    Spectra. doi:10.5281/zenodo.3269924
-   :cite:`Marszalec` : Marszalec, E., & University of Kuopio. (n.d.). Agfa
    IT8.7/2 Set. doi:10.5281/zenodo.3269926
-   :cite:`Orava` : Orava, J., & University of Kuopio. (n.d.). Munsell Colors
    Glossy (All) (Spectrofotometer Measured). doi:10.5281/zenodo.3269918
-   :cite:`Silvennoinen` : Silvennoinen, R., & University of Kuopio. (n.d.).
    Forest Colors. doi:10.5281/zenodo.3269920
"""

from __future__ import division, unicode_literals

import functools
import numpy as np
import os
import re
import scipy.io
import six
import sys
from collections import OrderedDict, namedtuple

from colour import SpectralDistribution, SpectralShape

from colour_datasets import datasets
from colour_datasets.loaders import AbstractDatasetLoader

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019-2020 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = [
    'MatFileMetadata_KuopioUniversity',
    'read_sds_from_mat_file_KuopioUniversity',
    'DatasetLoader_KuopioUniversity', 'build_KuopioUniversity',
    'DATA_KUOPIO_UNIVERSITY', 'DATASET_LOADERS_KUOPIO_UNIVERSITY'
]


class MatFileMetadata_KuopioUniversity(
        namedtuple('MatFileMetadata_KuopioUniversity',
                   ('key', 'shape', 'transpose', 'identifiers'))):
    """
    Metadata storage for an *University of Kuopio* dataset spectral
    distributions.

    Parameters
    ----------
    key : unicode
        *Matlab* *.mat* file key to extract the data from.
    shape : SpectralShape
        Spectral distributions shape.
    transpose : bool
        Whether to transpose the data.
    identifiers : array_like
        Identifiers for the spectral distributions.
    """


def read_sds_from_mat_file_KuopioUniversity(mat_file, metadata):
    """
    Reads the spectral distributions from given *University of Kuopio*
    *Matlab* *.mat* file.

    Parameters
    ----------
    mat_file : unicode
        *Matlab* *.mat* file.
    metadata : MatFileMetadata_KuopioUniversity
        Metadata required to read the spectral distributions in the *Matlab*
        *.mat* file.

    Returns
    -------
    OrderedDict
        Spectral distributions from the *Matlab* *.mat* file.
    """

    matlab_data = scipy.io.loadmat(mat_file)

    sds = OrderedDict()
    table = matlab_data[metadata.key]
    wavelengths = metadata.shape.range()

    if metadata.transpose:
        table = np.transpose(table)

    for i, data in enumerate(table):
        identifier = six.text_type(i + 1 if metadata.identifiers is None else
                                   matlab_data[metadata.identifiers][
                                       i].strip())

        if identifier in sds:
            identifier = '{0} ({1})'.format(identifier, i)

        sds[identifier] = SpectralDistribution(
            dict(zip(wavelengths, data)), name=identifier)

    return sds


class DatasetLoader_KuopioUniversity(AbstractDatasetLoader):
    """
    Defines the base class for a *University of Kuopio* dataset loader.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.DatasetLoader_KuopioUniversity.ID`
    -   :attr:`colour_datasets.loaders.DatasetLoader_KuopioUniversity.METADATA`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.DatasetLoader_KuopioUniversity.__init__`
    -   :meth:`colour_datasets.loaders.DatasetLoader_KuopioUniversity.load`
    """

    ID = None
    """
    Dataset record id, i.e. the *Zenodo* record number.

    ID : unicode
    """

    METADATA = None
    """
    Mapping of paths and
    :class:`colour_datasets.loaders.kuopio.MatFileMetadata_KuopioUniversity`
    class instances.

    METADATA : dict
    """

    def __init__(self):
        super(DatasetLoader_KuopioUniversity,
              self).__init__(datasets()[self.ID])

    def load(self):
        """
        Syncs, parses, converts and returns the *University of Kuopio* dataset
        content.

        Returns
        -------
        OrderedDict
            *University of Kuopio* dataset content.
        """

        super(DatasetLoader_KuopioUniversity, self).sync()

        self._content = OrderedDict()

        for path, metadata in self.METADATA.items():
            mat_path = os.path.join(self.record.repository, 'dataset', *path)

            self._content[
                metadata.key] = read_sds_from_mat_file_KuopioUniversity(
                    mat_path, metadata)

        return self._content


def _build_dataset_loader_class_KuopioUniversity(id_, title, citation_key,
                                                 metadata):
    """
    Class factory building *University of Kuopio* dataset loaders.

    Parameters
    ----------
    id_ : unicode
        Dataset record id, i.e. the *Zenodo* record number.
    title : unicode
        *University of Kuopio* dataset loader title.
    citation_key : unicode
        *University of Kuopio* dataset citation key.
    metadata : dict
        Mapping of paths and
        :class:`colour_datasets.loaders.kuopio.MatFileMetadata_KuopioUniversity`
        class instances.

    Returns
    -------
    object
        *University of Kuopio* dataset loader class.
    """

    class_docstring = """
    Defines the *University of Kuopio* *{0}* dataset loader.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.{0}.ID`
    -   :attr:`colour_datasets.loaders.{0}.METADATA`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.{0}.__init__`
    -   :meth:`colour_datasets.loaders.{0}.load`

    References
    ----------
    :cite:`{1}`""" [1:].format(title, citation_key)

    load_method_docstring = """
        Syncs, parses, converts and returns the *University of Kuopio* *{0}*
        dataset content.

        Returns
        -------
        OrderedDict
            *University of Kuopio* *{0}* dataset content. """ [1:].format(
        title)

    module = sys.modules['colour_datasets.loaders.kuopio']

    prefix = re.sub('\\.|\\(|\\)|/|\\s', '', title)
    class_attribute = 'DatasetLoader_{0}'.format(prefix)
    dataset_loader_class = type(
        str(class_attribute), (DatasetLoader_KuopioUniversity, ), {
            'ID': id_,
            'METADATA': metadata
        })

    dataset_loader_class.__doc__ = class_docstring
    try:
        dataset_loader_class.load.__doc__ = load_method_docstring
    except AttributeError:
        pass

    setattr(module, class_attribute, dataset_loader_class)

    return dataset_loader_class


def build_KuopioUniversity(dataset_loader_class, load=True):
    """
    Singleton factory that builds a *University of Kuopio* dataset loader.

    Parameters
    ----------
    dataset_loader_class : object
         *University of Kuopio* dataset loader class.
    load : bool, optional
        Whether to load the dataset upon instantiation.

    Returns
    -------
    DatasetLoader_KuopioUniversity
        Singleton instance of a *University of Kuopio* dataset loader.
    """

    module = sys.modules['colour_datasets.loaders.kuopio']

    prefix = dataset_loader_class.__name__.replace('DatasetLoader', '')
    prefix = re.sub('([A-Z]+)', r'_\1', prefix).replace('__', '_').upper()
    dataset_loader_attribute = 'DATASET_LOADER_{0}'.format(prefix)

    if not hasattr(module, dataset_loader_attribute):
        setattr(module, dataset_loader_attribute, dataset_loader_class())
        if load:
            getattr(module, dataset_loader_attribute).load()

    return getattr(module, dataset_loader_attribute)


# TODO: Implement support for *Natural Colors*:
# https://sandbox.zenodo.org/record/315640
# http://www.uef.fi/web/spectral/natural-colors
DATA_KUOPIO_UNIVERSITY = {
    '3269912': [
        'Munsell Colors Matt (Spectrofotometer Measured)', 'Hauta-Kasari', {
            ('munsell380_800_1_mat', 'munsell380_800_1.mat'):
                MatFileMetadata_KuopioUniversity('munsell',
                                                 SpectralShape(380, 800, 1),
                                                 True, 'S')
        }
    ],
    '3269914': [
        'Munsell Colors Matt (AOTF Measured)', 'Hauta-Kasaria', {
            ('munsell400_700_5_mat', 'munsell400_700_5.mat'):
                MatFileMetadata_KuopioUniversity('munsell',
                                                 SpectralShape(400, 700, 5),
                                                 True, 'S')
        }
    ],
    '3269916': [
        'Munsell Colors Glossy (Spectrofotometer Measured)', 'Haanpalo', {
            ('munsell400_700_10_mat', 'munsell400_700_10.mat'):
                MatFileMetadata_KuopioUniversity('munsell',
                                                 SpectralShape(400, 700, 10),
                                                 True, 'S')
        }
    ],
    '3269918': [
        'Munsell Colors Glossy (All) (Spectrofotometer Measured)', 'Orava', {
            ('munsell380_780_1_glossy_mat', 'munsell380_780_1_glossy.mat'):
                MatFileMetadata_KuopioUniversity('X', SpectralShape(
                    380, 780, 1), True, None)
        }
    ],
    '3269920': [
        'Forest Colors', 'Silvennoinen', {
            ('forest_matlab', 'birch.mat'):
                MatFileMetadata_KuopioUniversity('birch',
                                                 SpectralShape(380, 850, 5),
                                                 True, None),
            ('forest_matlab', 'pine.mat'):
                MatFileMetadata_KuopioUniversity('pine',
                                                 SpectralShape(380, 850, 5),
                                                 True, None),
            ('forest_matlab', 'spruce.mat'):
                MatFileMetadata_KuopioUniversity('spruce',
                                                 SpectralShape(380, 850, 5),
                                                 True, None)
        }
    ],
    '3269922': [
        'Paper Spectra', 'Haanpaloa', {
            ('paper_matlab', 'cardboardsce.mat'):
                MatFileMetadata_KuopioUniversity('cardboardsce',
                                                 SpectralShape(400, 700, 10),
                                                 True, None),
            ('paper_matlab', 'cardboardsci.mat'):
                MatFileMetadata_KuopioUniversity('cardboardsci',
                                                 SpectralShape(400, 700, 10),
                                                 True, None),
            ('paper_matlab', 'mirrorsci.mat'):
                MatFileMetadata_KuopioUniversity('mirrorsci',
                                                 SpectralShape(400, 700, 10),
                                                 True, None),
            ('paper_matlab', 'newsprintsce.mat'):
                MatFileMetadata_KuopioUniversity('newsprintsce',
                                                 SpectralShape(400, 700, 10),
                                                 True, None),
            ('paper_matlab', 'newsprintsci.mat'):
                MatFileMetadata_KuopioUniversity('newsprintsci',
                                                 SpectralShape(400, 700, 10),
                                                 True, None),
            ('paper_matlab', 'papersce.mat'):
                MatFileMetadata_KuopioUniversity('papersce',
                                                 SpectralShape(400, 700, 10),
                                                 True, None),
            ('paper_matlab', 'papersci.mat'):
                MatFileMetadata_KuopioUniversity('papersci',
                                                 SpectralShape(400, 700, 10),
                                                 True, None),
        }
    ],
    '3269924': [
        'Lumber Spectra', 'Hiltunen', {
            ('lumber_matlab', 'aspenWb.mat'):
                MatFileMetadata_KuopioUniversity('aspenWb',
                                                 SpectralShape(380, 2700, 1),
                                                 True, None),
            ('lumber_matlab', 'aspenWp.mat'):
                MatFileMetadata_KuopioUniversity('aspenWp',
                                                 SpectralShape(380, 2700, 1),
                                                 True, None),
            ('lumber_matlab', 'birchWb.mat'):
                MatFileMetadata_KuopioUniversity('birchWb',
                                                 SpectralShape(380, 2700, 1),
                                                 True, None),
            ('lumber_matlab', 'birchWp.mat'):
                MatFileMetadata_KuopioUniversity('birchWp',
                                                 SpectralShape(380, 2700, 1),
                                                 True, None),
            ('lumber_matlab', 'pineWb.mat'):
                MatFileMetadata_KuopioUniversity('pineWb',
                                                 SpectralShape(380, 2700, 1),
                                                 True, None),
            ('lumber_matlab', 'pineWp.mat'):
                MatFileMetadata_KuopioUniversity('pineWp',
                                                 SpectralShape(380, 2700, 1),
                                                 True, None),
            ('lumber_matlab', 'spruceWb.mat'):
                MatFileMetadata_KuopioUniversity('spruceWb',
                                                 SpectralShape(380, 2700, 1),
                                                 True, None),
            ('lumber_matlab', 'spruceWp.mat'):
                MatFileMetadata_KuopioUniversity('spruceWp',
                                                 SpectralShape(380, 2700, 1),
                                                 True, None)
        }
    ],
    '3269926': [
        'Agfa IT8.7/2 Set', 'Marszalec', {
            ('agfait872_mat', 'agfait872.mat'):
                MatFileMetadata_KuopioUniversity('agfa',
                                                 SpectralShape(400, 700, 10),
                                                 True, None)
        }
    ],
}

_singleton_factory_docstring_template = """
    Singleton factory that the builds *University of Kuopio* *{1}* dataset
    loader.

    Parameters
    ----------
    load : bool, optional
        Whether to load the dataset upon instantiation.

    Returns
    -------
    {0}
        Singleton instance of the *University of Kuopio* *{1}* dataset loader.

    References
    ----------
    :cite:`{2}`""" [1:]

DATASET_LOADERS_KUOPIO_UNIVERSITY = {}
"""
*University of Kuopio* dataset loaders.

References
----------
:cite:`Hauta-Kasari`, :cite:`Hauta-Kasaria`, :cite:`Haanpalo`, :cite:`Orava`,
:cite:`Silvennoinen`, :cite:`Haanpaloa`, :cite:`Hiltunen`, :cite:`Marszalec`

DATASET_LOADERS_KUOPIO_UNIVERSITY : dict
"""

for _id, _data in DATA_KUOPIO_UNIVERSITY.items():
    _module = sys.modules['colour_datasets.loaders.kuopio']
    _dataset_loader_class = _build_dataset_loader_class_KuopioUniversity(
        _id, *_data)
    _partial_function = functools.partial(build_KuopioUniversity,
                                          _dataset_loader_class)
    _partial_function.__doc__ = _singleton_factory_docstring_template.format(
        _dataset_loader_class.__name__, *_data[:-1])

    _build_function_name = 'build_{0}'.format(
        _dataset_loader_class.__name__.replace('DatasetLoader_', ''))

    setattr(_module, _build_function_name, _partial_function)

    DATASET_LOADERS_KUOPIO_UNIVERSITY[_id] = _partial_function

    __all__ += [_dataset_loader_class.__name__, _build_function_name]

del _id, _data, _module, _partial_function, _build_function_name
