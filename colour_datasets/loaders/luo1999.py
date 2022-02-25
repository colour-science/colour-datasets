"""
Corresponding-Colour Datasets - Luo and Rhodes (1999)
=====================================================

Defines the objects implementing support for *Luo and Rhodes (1999)*
*Corresponding-Colour Datasets* dataset loading:

-   :class:`colour_datasets.loaders.DatasetLoader_Luo1999`
-   :func:`colour_datasets.loaders.build_Luo1999`

References
----------
-   :cite:`Breneman1987b` : Breneman, E. J. (1987). Corresponding
    chromaticities for different states of adaptation to complex visual fields.
    Journal of the Optical Society of America A, 4(6), 1115.
    doi:10.1364/JOSAA.4.001115
-   :cite:`Luo1999` : Luo, M. R., & Rhodes, P. A. (1999). Corresponding-colour
    datasets. Color Research & Application, 24(4), 295-296.
    doi:10.1002/(SICI)1520-6378(199908)24:4<295::AID-COL10>3.0.CO;2-K
-   :cite:`McCann1976` : McCann, J. J., McKee, S. P., & Taylor, T. H. (1976).
    Quantitative studies in retinex theory a comparison between theoretical
    predictions and observer responses to the "color mondrian" experiments.
    Vision Research, 16(5), 445-IN3. doi:10.1016/0042-6989(76)90020-1
"""

from __future__ import annotations

import codecs
import numpy as np
import os
from collections import namedtuple

from colour.hints import Boolean, Dict, Optional, Tuple
from colour.utilities import as_float_array

from colour_datasets.loaders import AbstractDatasetLoader
from colour_datasets.records import datasets

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "New BSD License - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "CorrespondingColourDataset_Luo1999",
    "DatasetLoader_Luo1999",
    "build_Luo1999",
]


class CorrespondingColourDataset_Luo1999(
    namedtuple(
        "CorrespondingColourDataset_Luo1999",
        (
            "name",
            "XYZ_r",
            "XYZ_t",
            "XYZ_cr",
            "XYZ_ct",
            "Y_r",
            "Y_t",
            "B_r",
            "B_t",
            "metadata",
        ),
    )
):
    """
    Define a *Luo and Rhodes (1999)* *Corresponding-Colour Datasets* dataset.

    Parameters
    ----------
    name
        *Luo and Rhodes (1999)* *Corresponding-Colour Datasets* dataset name.
    XYZ_r
        *CIE XYZ* tristimulus values of the reference illuminant.
    XYZ_t
        *CIE XYZ* tristimulus values of the test illuminant.
    XYZ_cr
        Corresponding *CIE XYZ* tristimulus values under the reference
        illuminant.
    XYZ_ct
        Corresponding *CIE XYZ* tristimulus values under the test illuminant.
    Y_r
        Reference white luminance :math:`Y_r` in :math:`cd/m^2`.
    Y_t
        Test white luminance :math:`Y_t` in :math:`cd/m^2`.
    B_r
         Luminance factor :math:`B_r` of reference achromatic background as
         percentage.
    B_t
         Luminance factor :math:`B_t` of test achromatic background as
         percentage.
    metadata
        Dataset metadata.
    """


class DatasetLoader_Luo1999(AbstractDatasetLoader):
    """
    Define the *Luo and Rhodes (1999)* *Corresponding-Colour Datasets* dataset
    loader.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.DatasetLoader_Luo1999.ID`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.DatasetLoader_Luo1999.__init__`
    -   :meth:`colour_datasets.loaders.DatasetLoader_Luo1999.load`

    References
    ----------
    :cite:`Breneman1987b`, :cite:`Luo1999`, :cite:`McCann1976`
    """

    ID: str = "3270903"
    """Dataset record id, i.e. the *Zenodo* record number."""

    def __init__(self):
        super().__init__(datasets()[DatasetLoader_Luo1999.ID])

    def load(self) -> Dict[str, CorrespondingColourDataset_Luo1999]:
        """
        Sync, parse, convert and return the *Luo and Rhodes (1999)*
        *Corresponding-Colour Datasets* dataset content.

        Returns
        -------
        :class:`dict`
            *Luo and Rhodes (1999)* *Corresponding-Colour Datasets* dataset
            content.

        Notes
        -----
        -   *Brene.p6.dat* has only 11 samples while *Breneman (1987)* has 12
            results.
        -   The illuminance in :math:`Lux` for *Breneman (1987)* datasets given
            by *Luo and Rhodes (1999)* is in domain [50, 3870] while
            *Breneman (1987)* reports luminance in :math:`cd/m^2` in domain
            [15, 11100], i.e. [47, 34871.69] in :math:`Lux`. The metadata has
            been corrected accordingly.
        -   The illuminance values, i.e. 14 and 40, for
            *McCann, McKee and Taylor (1976)* datasets given by
            *Luo and Rhodes (1999)* were not found in :cite:`McCann1976`. The
            values in use are the average of both.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = DatasetLoader_Luo1999()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.content.keys())
        37
        """

        super().sync()

        metadata_headers = (
            "No. of Phases",
            "No. of Samples",
            "Illuminant Test",
            "Illuminant Ref.",
            "Illuminance (lux)",
            "Background (Y%)",
            "Sample Size",
            "Medium",
            "Experimental Method",
        )

        corresponding_colour_datasets: Dict[str, Tuple] = dict(
            [
                (
                    "CSAJ-C",
                    (
                        ("CSAJ.da.dat",),
                        (
                            1,
                            87,
                            "D65",
                            "A",
                            np.tile(1000, [1, 2]),
                            np.tile(20, [1, 2]),
                            "S",
                            "Refl.",
                            "Haploscopic",
                        ),
                    ),
                ),
                (
                    "CSAJ-Hunt",
                    (
                        (
                            "CSAJ.10.dat",
                            "CSAJ.50.dat",
                            "CSAJ.1000.dat",
                            "CSAJ.3000.dat",
                        ),
                        (
                            4,
                            20,
                            "D65",
                            "D65",
                            np.repeat([10, 50, 1000, 3000], 2, -1).reshape(
                                -1, 2
                            ),
                            np.tile(20, [4, 2]),
                            "S",
                            "Refl.",
                            "Haploscopic",
                        ),
                    ),
                ),
                (
                    "CSAJ-Stevens",
                    (
                        (
                            "Steve.10.dat",
                            "Steve.50.dat",
                            "Steve.1000.dat",
                            "Steve.3000.dat",
                        ),
                        (
                            4,
                            19,
                            "D65",
                            "D65",
                            np.repeat([10, 50, 1000, 3000], 2, -1).reshape(
                                -1, 2
                            ),
                            np.tile(20, [4, 2]),
                            "S",
                            "Refl.",
                            "Haploscopic",
                        ),
                    ),
                ),
                (
                    "Helson",
                    (
                        ("helson.ca.dat",),
                        (
                            1,
                            59,
                            "D65",
                            "A",
                            np.tile(1000, [1, 2]),
                            np.tile(20, [1, 2]),
                            "S",
                            "Refl.",
                            "Memory",
                        ),
                    ),
                ),
                (
                    "Lam & Rigg",
                    (
                        ("lam.da.dat",),
                        (
                            1,
                            58,
                            "D65",
                            "A",
                            np.tile(1000, [1, 2]),
                            np.tile(20, [1, 2]),
                            "L",
                            "Refl.",
                            "Memory",
                        ),
                    ),
                ),
                (
                    "Lutchi (A)",
                    (
                        ("lutchi.da.dat",),
                        (
                            1,
                            43,
                            "D65",
                            "A",
                            np.tile(1000, [1, 2]),
                            np.tile(20, [1, 2]),
                            "S",
                            "Refl.",
                            "Magnitude",
                        ),
                    ),
                ),
                (
                    "Lutchi (D50)",
                    (
                        ("lutchi.dd.dat",),
                        (
                            1,
                            44,
                            "D65",
                            "D50",
                            np.tile(1000, [1, 2]),
                            np.tile(20, [1, 2]),
                            "S",
                            "Refl.",
                            "Magnitude",
                        ),
                    ),
                ),
                (
                    "Lutchi (WF)",
                    (
                        ("lutchi.dw.dat",),
                        (
                            1,
                            41,
                            "D65",
                            "WF",
                            np.tile(1000, [1, 2]),
                            np.tile(20, [1, 2]),
                            "S",
                            "Refl.",
                            "Magnitude",
                        ),
                    ),
                ),
                (
                    "Kuo & Luo (A)",
                    (
                        ("Kuo.da.dat",),
                        (
                            1,
                            40,
                            "D65",
                            "A",
                            np.tile(1000, [1, 2]),
                            np.tile(20, [1, 2]),
                            "L",
                            "Refl.",
                            "Magnitude",
                        ),
                    ),
                ),
                (
                    "Kuo & Luo (TL84)",
                    (
                        ("Kuo.dt.dat",),
                        (
                            1,
                            41,
                            "D65",
                            "TL84",
                            np.tile(1000, [1, 2]),
                            np.tile(20, [1, 2]),
                            "S",
                            "Refl.",
                            "Magnitude",
                        ),
                    ),
                ),
                (
                    "Breneman-C",
                    (
                        (
                            "Brene.p1.dat",
                            "Brene.p2.dat",
                            "Brene.p3.dat",
                            "Brene.p4.dat",
                            "Brene.p6.dat",
                            "Brene.p8.dat",
                            "Brene.p9.dat",
                            "Brene.p11.dat",
                            "Brene.p12.dat",
                        ),
                        (
                            9,
                            107,
                            "D65, 55",
                            "A, P, G",
                            np.reshape(
                                np.repeat(
                                    [
                                        1500,
                                        1500,
                                        75,
                                        75,
                                        11100,
                                        350,
                                        15,
                                        1560,
                                        75,
                                    ],
                                    2,
                                    -1,
                                ),
                                (-1, 2),
                            ),
                            np.tile(30, [9, 2]),
                            "S",
                            "Trans.",
                            "Magnitude",
                        ),
                    ),
                ),
                (
                    "Breneman-L",
                    (
                        (
                            "Brene.p5.dat",
                            "Brene.p7.dat",
                            "Brene.p10.dat",
                        ),
                        (
                            3,
                            36,
                            "D55",
                            "D55",
                            np.array([[130, 2120], [850, 11100], [15, 270]]),
                            np.tile(30, [3, 2]),
                            "S",
                            "Trans.",
                            "Haploscopic",
                        ),
                    ),
                ),
                (
                    "Braun & Fairchild",
                    (
                        (
                            "RIT.1.dat",
                            "RIT.2.dat",
                            "RIT.3.dat",
                            "RIT.4.dat",
                        ),
                        (
                            4,
                            66,
                            "D65",
                            "D30, 65, 95",
                            np.tile(129, [4, 2]),
                            np.tile(20, [4, 2]),
                            "S",
                            "Mon., Refl.",
                            "Matching",
                        ),
                    ),
                ),
                (
                    "McCann",
                    (
                        (
                            "mcan.b.dat",
                            "mcan.g.dat",
                            "mcan.grey.dat",
                            "mcan.r.dat",
                            "mcan.y.dat",
                        ),
                        (
                            5,
                            85,
                            "D65",
                            "R, Y, G, B",
                            np.tile((14 + 40) / 2, [5, 2]),
                            np.tile(30, [5, 2]),
                            "S",
                            "Refl.",
                            "Haploscopic",
                        ),
                    ),
                ),
            ]
        )

        self._content = dict()
        for key, (
            filenames,
            metadata,
        ) in corresponding_colour_datasets.items():
            for i, filename in enumerate(filenames):
                path = os.path.join(
                    self.record.repository, "dataset", filename
                )

                XYZ_r, XYZ_t = [], []
                XYZ_cr, XYZ_ct = [], []
                with codecs.open(path, encoding="utf-8") as dat_file:
                    lines = filter(
                        None, (line.strip() for line in dat_file.readlines())
                    )
                    for j, line in enumerate(lines):
                        values = line.split()
                        if j == 0:
                            XYZ_r = list(map(float, values[:3]))
                            XYZ_t = list(map(float, values[3:]))
                        elif len(values) == 1:
                            continue
                        else:
                            XYZ_cr.append(list(map(float, values[:3])))
                            XYZ_ct.append(list(map(float, values[3:])))

                name = f"{key} - {filename.split('.')[1]}"
                dataset_metadata = dict(zip(metadata_headers, metadata))

                Y_r = dataset_metadata["Illuminance (lux)"][i][0]
                Y_t = dataset_metadata["Illuminance (lux)"][i][1]

                B_r = dataset_metadata["Background (Y%)"][i][0]
                B_t = dataset_metadata["Background (Y%)"][i][1]

                dataset_metadata["Illuminance (lux)"] = dataset_metadata[
                    "Illuminance (lux)"
                ][i]
                dataset_metadata["Background (Y%)"] = dataset_metadata[
                    "Background (Y%)"
                ][i]

                self._content[name] = CorrespondingColourDataset_Luo1999(
                    name,
                    as_float_array(XYZ_r) / 100,
                    as_float_array(XYZ_t) / 100,
                    as_float_array(XYZ_cr) / 100,
                    as_float_array(XYZ_ct) / 100,
                    Y_r * np.pi,
                    Y_t * np.pi,
                    B_r,
                    B_t,
                    dataset_metadata,
                )

        return self._content


_DATASET_LOADER_LUO1999: Optional[DatasetLoader_Luo1999] = None
"""
Singleton instance of the *Luo and Rhodes (1999)*
*Corresponding-Colour Datasets* dataset loader.
"""


def build_Luo1999(load: Boolean = True) -> DatasetLoader_Luo1999:
    """
    Singleton factory that the builds *Luo and Rhodes (1999)*
    *Corresponding-Colour Datasets* dataset loader.

    Parameters
    ----------
    load
        Whether to load the dataset upon instantiation.

    Returns
    -------
    :class:`colour_datasets.loaders.DatasetLoader_Luo1999`
        Singleton instance of the *Luo and Rhodes (1999)*
        *Corresponding-Colour Datasets* dataset loader.

    References
    ----------
    :cite:`Breneman1987b`, :cite:`Luo1999`, :cite:`McCann1976`
    """

    global _DATASET_LOADER_LUO1999

    if _DATASET_LOADER_LUO1999 is None:
        _DATASET_LOADER_LUO1999 = DatasetLoader_Luo1999()
        if load:
            _DATASET_LOADER_LUO1999.load()

    return _DATASET_LOADER_LUO1999
