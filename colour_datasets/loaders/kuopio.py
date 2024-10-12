"""
University of Kuopio
====================

Define the objects implementing support for the *University of Kuopio*
datasets loading:

-   :class:`colour_datasets.loaders.DatasetLoader_KuopioUniversity`
-   :func:`colour_datasets.loaders.build_KuopioUniversity`

Notes
-----
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

from __future__ import annotations

import contextlib
import functools
import os
import re
import sys
from collections import namedtuple
from typing import ClassVar

import numpy as np
import scipy.io
from colour import SpectralDistribution, SpectralShape
from colour.hints import Any, Dict, Tuple, Type, cast

from colour_datasets.loaders import AbstractDatasetLoader
from colour_datasets.records import datasets

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "MatFileMetadata_KuopioUniversity",
    "read_sds_from_mat_file_KuopioUniversity",
    "DatasetLoader_KuopioUniversity",
    "build_KuopioUniversity",
    "DATA_KUOPIO_UNIVERSITY",
    "DATASET_LOADERS_KUOPIO_UNIVERSITY",
]


class MatFileMetadata_KuopioUniversity(
    namedtuple(
        "MatFileMetadata_KuopioUniversity",
        ("key", "shape", "transpose", "identifiers"),
    )
):
    """
    Metadata storage for an *University of Kuopio* dataset spectral
    distributions.

    Parameters
    ----------
    key
        *Matlab* *.mat* file key to extract the data from.
    shape
        Spectral distributions shape.
    transpose
        Whether to transpose the data.
    identifiers
        Identifiers for the spectral distributions.
    """


def read_sds_from_mat_file_KuopioUniversity(
    mat_file: str, metadata: MatFileMetadata_KuopioUniversity
) -> Dict[str, SpectralDistribution]:
    """
    Read the spectral distributions from given *University of Kuopio*
    *Matlab* *.mat* file.

    Parameters
    ----------
    mat_file
        *Matlab* *.mat* file.
    metadata
        Metadata required to read the spectral distributions in the *Matlab*
        *.mat* file.

    Returns
    -------
    :class:`dict`
        Spectral distributions from the *Matlab* *.mat* file.
    """

    matlab_data = scipy.io.loadmat(mat_file)

    sds = {}
    table = matlab_data[metadata.key]
    wavelengths = metadata.shape.range()

    if metadata.transpose:
        table = np.transpose(table)

    for i, data in enumerate(table):
        identifier = str(
            i + 1
            if metadata.identifiers is None
            else matlab_data[metadata.identifiers][i].strip()
        )

        if identifier in sds:
            identifier = f"{identifier} ({i})"

        sds[identifier] = SpectralDistribution(
            dict(zip(wavelengths, data)), name=identifier
        )

    return sds


class DatasetLoader_KuopioUniversity(AbstractDatasetLoader):
    """
    Define the base class for a *University of Kuopio* dataset loader.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.DatasetLoader_KuopioUniversity.ID`
    -   :attr:`colour_datasets.loaders.DatasetLoader_KuopioUniversity.METADATA`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.DatasetLoader_KuopioUniversity.__init__`
    -   :meth:`colour_datasets.loaders.DatasetLoader_KuopioUniversity.load`
    """

    ID: str = "Undefined"
    """Dataset record id, i.e., the *Zenodo* record number."""

    METADATA: ClassVar[Dict] = {}
    """
    Mapping of paths and
    :class:`colour_datasets.loaders.kuopio.MatFileMetadata_KuopioUniversity`
    class instances.
    """

    def __init__(self) -> None:
        super().__init__(datasets()[self.ID])

    def load(self) -> Dict[str, Dict[str, SpectralDistribution]]:
        """
        Sync, parse, convert and return the *University of Kuopio* dataset
        content.

        Returns
        -------
        :class:`dict`
            *University of Kuopio* dataset content.
        """

        super().sync()

        self._content = {}

        for path, metadata in self.METADATA.items():
            mat_path = os.path.join(self.record.repository, "dataset", *path)

            self._content[metadata.key] = read_sds_from_mat_file_KuopioUniversity(
                mat_path, metadata
            )

        return self._content


def _build_dataset_loader_class_KuopioUniversity(
    id_: str,
    title: str,
    citation_key: str,
    metadata: Dict[str, Tuple[str, str, Dict[Tuple, MatFileMetadata_KuopioUniversity]]],
) -> Any:
    """
    Class factory building *University of Kuopio* dataset loaders.

    Parameters
    ----------
    id_
        Dataset record id, i.e., the *Zenodo* record number.
    title
        *University of Kuopio* dataset loader title.
    citation_key
        *University of Kuopio* dataset citation key.
    metadata
        Mapping of paths and
        :class:`colour_datasets.loaders.kuopio.MatFileMetadata_KuopioUniversity`
        class instances.

    Returns
    -------
    object
        *University of Kuopio* dataset loader class.
    """

    class_docstring = f"""
    Defines the *University of Kuopio* *{title}* dataset loader.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.{title}.ID`
    -   :attr:`colour_datasets.loaders.{title}.METADATA`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.{title}.__init__`
    -   :meth:`colour_datasets.loaders.{title}.load`

    References
    ----------
    :cite:`{citation_key}`"""[1:]

    load_method_docstring = f"""
        Sync, parse, convert and return the *University of Kuopio* *{title}*
        dataset content.

        Returns
        -------
        dict
            *University of Kuopio* *{title}* dataset content."""[1:]

    module = sys.modules["colour_datasets.loaders.kuopio"]

    prefix = re.sub("\\.|\\(|\\)|/|\\s", "", title)
    class_attribute = f"DatasetLoader_{prefix}"
    dataset_loader_class = cast(
        DatasetLoader_KuopioUniversity,
        type(
            str(class_attribute),
            (DatasetLoader_KuopioUniversity,),
            {"ID": id_, "METADATA": metadata},
        ),
    )

    dataset_loader_class.__doc__ = class_docstring
    with contextlib.suppress(AttributeError):
        dataset_loader_class.load.__doc__ = load_method_docstring

    setattr(module, class_attribute, dataset_loader_class)

    return dataset_loader_class


def build_KuopioUniversity(
    dataset_loader_class: Type[DatasetLoader_KuopioUniversity],
    load: bool = True,
) -> DatasetLoader_KuopioUniversity:
    """
    Singleton factory that builds a *University of Kuopio* dataset loader.

    Parameters
    ----------
    dataset_loader_class
         *University of Kuopio* dataset loader class.
    load
        Whether to load the dataset upon instantiation.

    Returns
    -------
    :class:`colour_datasets.loaders.DatasetLoader_KuopioUniversity`
        Singleton instance of a *University of Kuopio* dataset loader.
    """

    module = sys.modules["colour_datasets.loaders.kuopio"]

    prefix = dataset_loader_class.__name__.replace("DatasetLoader", "")
    prefix = re.sub("([A-Z]+)", r"_\1", prefix).replace("__", "_").upper()
    dataset_loader_attribute = f"DATASET_LOADER_{prefix}"

    if not hasattr(module, dataset_loader_attribute):
        setattr(module, dataset_loader_attribute, dataset_loader_class())
        if load:
            getattr(module, dataset_loader_attribute).load()

    return getattr(module, dataset_loader_attribute)


# TODO: Implement support for *Natural Colors*:
# https://sandbox.zenodo.org/record/315640
# http://www.uef.fi/web/spectral/natural-colors
DATA_KUOPIO_UNIVERSITY: Dict = {
    "3269912": (
        "Munsell Colors Matt (Spectrofotometer Measured)",
        "Hauta-Kasari",
        {
            (
                "munsell380_800_1_mat",
                "munsell380_800_1.mat",
            ): MatFileMetadata_KuopioUniversity(
                "munsell", SpectralShape(380, 800, 1), True, "S"
            )
        },
    ),
    "3269914": (
        "Munsell Colors Matt (AOTF Measured)",
        "Hauta-Kasaria",
        {
            (
                "munsell400_700_5_mat",
                "munsell400_700_5.mat",
            ): MatFileMetadata_KuopioUniversity(
                "munsell", SpectralShape(400, 700, 5), True, "S"
            )
        },
    ),
    "3269916": (
        "Munsell Colors Glossy (Spectrofotometer Measured)",
        "Haanpalo",
        {
            (
                "munsell400_700_10_mat",
                "munsell400_700_10.mat",
            ): MatFileMetadata_KuopioUniversity(
                "munsell", SpectralShape(400, 700, 10), True, "S"
            )
        },
    ),
    "3269918": (
        "Munsell Colors Glossy (All) (Spectrofotometer Measured)",
        "Orava",
        {
            (
                "munsell380_780_1_glossy_mat",
                "munsell380_780_1_glossy.mat",
            ): MatFileMetadata_KuopioUniversity(
                "X", SpectralShape(380, 780, 1), True, None
            )
        },
    ),
    "3269920": (
        "Forest Colors",
        "Silvennoinen",
        {
            ("forest_matlab", "birch.mat"): MatFileMetadata_KuopioUniversity(
                "birch", SpectralShape(380, 850, 5), True, None
            ),
            ("forest_matlab", "pine.mat"): MatFileMetadata_KuopioUniversity(
                "pine", SpectralShape(380, 850, 5), True, None
            ),
            ("forest_matlab", "spruce.mat"): MatFileMetadata_KuopioUniversity(
                "spruce", SpectralShape(380, 850, 5), True, None
            ),
        },
    ),
    "3269922": (
        "Paper Spectra",
        "Haanpaloa",
        {
            (
                "paper_matlab",
                "cardboardsce.mat",
            ): MatFileMetadata_KuopioUniversity(
                "cardboardsce", SpectralShape(400, 700, 10), True, None
            ),
            (
                "paper_matlab",
                "cardboardsci.mat",
            ): MatFileMetadata_KuopioUniversity(
                "cardboardsci", SpectralShape(400, 700, 10), True, None
            ),
            (
                "paper_matlab",
                "mirrorsci.mat",
            ): MatFileMetadata_KuopioUniversity(
                "mirrorsci", SpectralShape(400, 700, 10), True, None
            ),
            (
                "paper_matlab",
                "newsprintsce.mat",
            ): MatFileMetadata_KuopioUniversity(
                "newsprintsce", SpectralShape(400, 700, 10), True, None
            ),
            (
                "paper_matlab",
                "newsprintsci.mat",
            ): MatFileMetadata_KuopioUniversity(
                "newsprintsci", SpectralShape(400, 700, 10), True, None
            ),
            ("paper_matlab", "papersce.mat"): MatFileMetadata_KuopioUniversity(
                "papersce", SpectralShape(400, 700, 10), True, None
            ),
            ("paper_matlab", "papersci.mat"): MatFileMetadata_KuopioUniversity(
                "papersci", SpectralShape(400, 700, 10), True, None
            ),
        },
    ),
    "3269924": (
        "Lumber Spectra",
        "Hiltunen",
        {
            ("lumber_matlab", "aspenWb.mat"): MatFileMetadata_KuopioUniversity(
                "aspenWb", SpectralShape(380, 2700, 1), True, None
            ),
            ("lumber_matlab", "aspenWp.mat"): MatFileMetadata_KuopioUniversity(
                "aspenWp", SpectralShape(380, 2700, 1), True, None
            ),
            ("lumber_matlab", "birchWb.mat"): MatFileMetadata_KuopioUniversity(
                "birchWb", SpectralShape(380, 2700, 1), True, None
            ),
            ("lumber_matlab", "birchWp.mat"): MatFileMetadata_KuopioUniversity(
                "birchWp", SpectralShape(380, 2700, 1), True, None
            ),
            ("lumber_matlab", "pineWb.mat"): MatFileMetadata_KuopioUniversity(
                "pineWb", SpectralShape(380, 2700, 1), True, None
            ),
            ("lumber_matlab", "pineWp.mat"): MatFileMetadata_KuopioUniversity(
                "pineWp", SpectralShape(380, 2700, 1), True, None
            ),
            (
                "lumber_matlab",
                "spruceWb.mat",
            ): MatFileMetadata_KuopioUniversity(
                "spruceWb", SpectralShape(380, 2700, 1), True, None
            ),
            (
                "lumber_matlab",
                "spruceWp.mat",
            ): MatFileMetadata_KuopioUniversity(
                "spruceWp", SpectralShape(380, 2700, 1), True, None
            ),
        },
    ),
    "3269926": (
        "Agfa IT8.7/2 Set",
        "Marszalec",
        {
            (
                "agfait872_mat",
                "agfait872.mat",
            ): MatFileMetadata_KuopioUniversity(
                "agfa", SpectralShape(400, 700, 10), True, None
            )
        },
    ),
}

_singleton_factory_docstring_template: str = """
    Singleton factory that the builds *University of Kuopio* *{1}* dataset
    loader.

    Parameters
    ----------
    load
        Whether to load the dataset upon instantiation.

    Returns
    -------
    {0}
        Singleton instance of the *University of Kuopio* *{1}* dataset loader.

    References
    ----------
    :cite:`{2}`"""[1:]

DATASET_LOADERS_KUOPIO_UNIVERSITY: Dict = {}
"""
*University of Kuopio* dataset loaders.

References
----------
:cite:`Hauta-Kasari`, :cite:`Hauta-Kasaria`, :cite:`Haanpalo`, :cite:`Orava`,
:cite:`Silvennoinen`, :cite:`Haanpaloa`, :cite:`Hiltunen`, :cite:`Marszalec`
"""

for _id, _data in DATA_KUOPIO_UNIVERSITY.items():
    _module = sys.modules["colour_datasets.loaders.kuopio"]
    _dataset_loader_class = _build_dataset_loader_class_KuopioUniversity(_id, *_data)
    _partial_function = functools.partial(build_KuopioUniversity, _dataset_loader_class)
    _partial_function.__doc__ = _singleton_factory_docstring_template.format(
        _dataset_loader_class.__name__, *_data[:-1]
    )

    _build_function_name = (
        f"build_{_dataset_loader_class.__name__.replace('DatasetLoader_', '')}"
    )

    setattr(_module, _build_function_name, _partial_function)

    DATASET_LOADERS_KUOPIO_UNIVERSITY[_id] = _partial_function

    __all__ += [  # noqa: PLE0604
        _dataset_loader_class.__name__,
        _build_function_name,
    ]

del _id, _data, _module, _partial_function, _build_function_name
