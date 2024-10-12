"""
LUTCHI Colour Appearance Data - Luo and Rhodes (1997)
=====================================================

Define the objects implementing support for *Luo and Rhodes (1997)*
*LUTCHI Colour Appearance Data* dataset loading:

-   :class:`colour_datasets.loaders.DatasetLoader_Luo1997`
-   :func:`colour_datasets.loaders.build_Luo1997`

References
----------
-   :cite:`Luo1991` : Luo, M. R., Clarke, A. A., Rhodes, P. A., Schappo, A.,
    Scrivener, S. A. R., & Tait, C. J. (1991b). Quantifying colour appearance.
    Part I. Lutchi colour appearance data. Color Research & Application, 16(3),
    166-180. doi:10.1002/col.5080160307
-   :cite:`Luo1991a` : Luo, M. R., Clarke, A. A., Rhodes, P. A., Schappo, A.,
    Scrivener, S. A. R., & Tait, C. J. (1991a). Quantifying colour appearance.
    Part II. Testing colour models performance using lutchi colour appearance
    data. Color Research & Application, 16(3), 181-197.
    doi:10.1002/col.5080160308
-   :cite:`Luo1993` : Luo, M. R., Gao, X. W., Rhodes, P. A., Xin, H. J.,
    Clarke, A. A., & Scrivener, S. A. R. (1993). Quantifying colour appearance.
    part III. Supplementary LUTCHI colour appearance data. Color Research &
    Application, 18(2), 98-113. doi:10.1002/col.5080180207
-   :cite:`Luo1997` : Luo, M. R., & Rhodes, P. A. (1997). Using the LUTCHI
    Colour Appearance Data. Retrieved September 10, 2019, from
    https://web.archive.org/web/20040212195937/\
http://colour.derby.ac.uk:80/colour/info/lutchi/
"""

from __future__ import annotations

import os
from collections import namedtuple

import numpy as np
from colour.hints import Dict, Tuple
from colour.utilities import as_float_array, usage_warning

from colour_datasets.loaders import AbstractDatasetLoader
from colour_datasets.records import datasets

__author__ = "Colour Developers"
__copyright__ = "Copyright (C) 2019 - Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-science@googlegroups.com"
__status__ = "Production"

__all__ = [
    "ExperimentalGroupLuo1997",
    "ExperimentalPhaseLuo1997",
    "DatasetLoader_Luo1997",
    "build_Luo1997",
]


class ExperimentalGroupLuo1997(
    namedtuple("ExperimentalGroupLuo1997", ("name", "phases", "metadata"))
):
    """
    Define a *Luo and Rhodes (1997)* *LUTCHI Colour Appearance Data*
    experimental group, i.e., a group of experimental phases.

    Parameters
    ----------
    name
        *Luo and Rhodes (1997)* *LUTCHI Colour Appearance Data* experimental
        group name.
    phases
        Experimental phases.
    metadata
        Experimental group metadata.
    """


class ExperimentalPhaseLuo1997(
    namedtuple(
        "ExperimentalPhaseLuo1997",
        (
            "name",
            "JQCH_v",
            "xyY_c",
            "S_Y_c",
            "Y_b",
            "Y_r",
            "XYZ_o",
            "metadata",
        ),
    )
):
    """
    Define a *Luo and Rhodes (1997)* *LUTCHI Colour Appearance Data*
    experimental phase.

    Parameters
    ----------
    name
        *Luo and Rhodes (1997)* *LUTCHI Colour Appearance Data* experimental
        phase name.
    JQCH_v
        :math:`JQCH_v` array from the visual file where :math:`JQ`, :math:`C`,
        and :math:`H` are the mean visual results of the lightness or
        brightness, colourfulness and hue. The arithmetic mean was used for
        calculating lightness (0 for black, 100 for white) and hue (0 for red,
        100 for yellow, 200 for green, 300 for blue and 400 for red) results,
        the geometric mean for brightness (0 for black) and colourfulness (0
        for neutral colours) results in open ended scales.
    xyY_c
        *CIE xyY* colourspace array :math:`xyY_c` from the colorimetric file
        and measured using a telespectroradiometer (TSR).
    S_Y_c
        Scaling factor :math:`S_Y` of the Y values used for adjusting those in
        the colorimetric file, i.e., *CIE xyY* colourspace array :math:`xyY_c`.
    Y_b
        Relative luminance of background :math:`Y_b` in :math:`cd/m^2`.
    Y_r
        Reference white sample luminance :math:`Y_r` in :math:`cd/m^2`.
    XYZ_o
        *CIE XYZ* tristimulus values of the illuminant.
    metadata
        Experimental phase metadata.
    """


class DatasetLoader_Luo1997(AbstractDatasetLoader):
    """
    Define the *Luo and Rhodes (1997)* *LUTCHI Colour Appearance Data* dataset
    loader.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.DatasetLoader_Luo1997.ID`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.DatasetLoader_Luo1997.__init__`
    -   :meth:`colour_datasets.loaders.DatasetLoader_Luo1997.load`

    References
    ----------
    :cite:`Luo1991`, :cite:`Luo1991a`, :cite:`Luo1993`, :cite:`Luo1997`
    """

    ID: str = "4394536"
    """Dataset record id, i.e., the *Zenodo* record number."""

    def __init__(self) -> None:
        super().__init__(datasets()[DatasetLoader_Luo1997.ID])

    def load(self) -> Dict[str, ExperimentalGroupLuo1997]:
        """
        Sync, parse, convert and return the *Luo and Rhodes (1997)*
        *LUTCHI Colour Appearance Data* dataset content.

        Returns
        -------
        :class:`dict`
            *Luo and Rhodes (1997)* *LUTCHI Colour Appearance Data* dataset
            content.

        Notes
        -----
        -   The *cold65wnl* file located at the following url:
            https://web.archive.org/web/20031230164218/\
http://colour.derby.ac.uk/colour/info/lutchi/data/cold65wnl is empty. Mark
            Fairchild's archive located at the following url:
            http://www.rit-mcsl.org/fairchild/files/LUTCHI_Data.sit also
            contains an empty *cold65wnl* file. A single line break has been
            added to the original file so that it can be uploaded to *Zenodo*.
        -   The *BIT.p\\*.\\** files are effectively named *bit_p\\*.\\**.
        -   The *cola.l* file does not exist and is assumed to be named
            *colal.l*.
        -   The *Self-luminous* entry for
            *Table I: Summary of the experimental groups* is named *CRT* in
            the sub-sequent tables.
        -   The *mean4.p\\** and *col.rf.p\\** files should all have 40
            samples, unexpectedly all the *col.rf.p\\** files have 41 samples.
            The first data rows are used as they are better correlated between
            the two datasets. The last row could be the experimental
            whitepoint.
        -   The *mean4.p7*, *mean4.p8*, *mean4.p9*, *mean4.p10*, *mean4.p11*,
            and *mean4.p12* files represent brightness experimental results.
        -   The *bit_p3.vis* file has 5 columns instead of 4 only the last 3
            are accounted for.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = DatasetLoader_Luo1997()
        >>> with suppress_stdout():
        ...     dataset.load()
        ...
        >>> len(dataset.content.keys())
        8
        """

        super().sync()

        group_metadata_headers = (
            "No. of phases",
            "Description of each data group",
            "Reference no.",
        )

        phase_metadata_headers = (
            "No. of Samples",
            "Neutrals",
        )

        experimental_groups_summary: Dict[str, Tuple] = {
            "R-HL": (
                6,
                "Reflective media with luminances ranging 364-232 cd/m2",
                1,
            ),
            "R-LL": (
                6,
                "Reflective media with luminances ranging 44-41 cd/m2",
                1,
            ),
            "R-VL": (
                12,
                "Reflective media with luminances ranging 843-0.4 cd/m2",
                2,
            ),
            "R-textile": (
                3,
                "Large textile samples with luminances ranging 730-340 cd/m2",
                4,
            ),
            "CRT": (
                11,
                "Monitor colours with luminances ranging 45-20 cd/m2",
                1,
            ),
            "35mm": (
                6,
                "35mm transparency with luminances ranging 113-45 cd/m2",
                3,
            ),
            "LT": (
                10,
                ("Cut-sheet transparency with luminances ranging 2100-320 cd/m2"),
                3,
            ),
            "BIT": (
                5,
                "Isolated viewing field with luminances ranging 90-3.6 cd/m2",
                5,
            ),
        }

        experimental_groups: Dict[str, Tuple] = {
            "R-HL": (
                (
                    1,
                    "nlmean.wh",
                    "cold50wnl",
                    105,
                    41,
                    46,
                    0.88,
                    100,
                    264,
                    np.array([97.13, 100, 76.62]),
                ),
                (
                    2,
                    "nlmean.bh",
                    "cold50gb",
                    105,
                    41,
                    46,
                    0.84,
                    6.2,
                    252,
                    np.array([97.09, 100, 83.1]),
                ),
                (
                    3,
                    "nlmean.gh",
                    "cold50gb",
                    105,
                    41,
                    46,
                    0.84,
                    21.5,
                    252,
                    np.array([97.09, 100, 83.1]),
                ),
                (
                    4,
                    "nld65.gh",
                    "cold65",
                    105,
                    41,
                    46,
                    0.81,
                    21.5,
                    243,
                    np.array([94.52, 100, 114.98]),
                ),
                (
                    5,
                    "nlwf.gh",
                    "colwf",
                    105,
                    41,
                    46,
                    0.84,
                    21.5,
                    252,
                    np.array([102.5, 100, 47.93]),
                ),
                (
                    6,
                    "nla.gh",
                    "colah",
                    105,
                    41,
                    46,
                    0.84,
                    21.5,
                    232,
                    np.array([112.92, 100, 28.62]),
                ),
            ),
            "R-LL": (
                (
                    1,
                    "nlmean.wl",
                    "cold50wnl",
                    105,
                    41,
                    46,
                    0.88,
                    100,
                    44,
                    np.array([97.13, 100, 76.62]),
                ),
                (
                    2,
                    "nlmean.bl",
                    "cold50gb",
                    105,
                    41,
                    46,
                    0.84,
                    6.2,
                    42,
                    np.array([97.09, 100, 83.1]),
                ),
                (
                    3,
                    "nlmean.gl",
                    "cold50gb",
                    105,
                    41,
                    46,
                    0.84,
                    21.5,
                    42,
                    np.array([97.09, 100, 83.1]),
                ),
                (
                    4,
                    "nld65.gl",
                    "cold65",
                    105,
                    41,
                    46,
                    0.81,
                    21.5,
                    40.5,
                    np.array([94.52, 100, 114.98]),
                ),
                (
                    5,
                    "nlwf.gl",
                    "colwf",
                    105,
                    41,
                    46,
                    0.84,
                    21.5,
                    42,
                    np.array([102.5, 100, 47.93]),
                ),
                (
                    6,
                    "nla.gl",
                    "colal",
                    105,
                    41,
                    46,
                    0.84,
                    21.4,
                    42,
                    np.array([117.26, 100, 22.44]),
                ),
            ),
            "R-VL": (
                (
                    1,
                    "mean4.p1",
                    "col.rf.p1",
                    40,
                    37,
                    40,
                    1,
                    21.5,
                    843,
                    np.array([94.04, 100, 76.29]),
                ),
                (
                    2,
                    "mean4.p2",
                    "col.rf.p2",
                    40,
                    37,
                    40,
                    1,
                    21.5,
                    200,
                    np.array([93.04, 100, 72.24]),
                ),
                (
                    3,
                    "mean4.p3",
                    "col.rf.p3",
                    40,
                    37,
                    40,
                    1,
                    21.5,
                    62,
                    np.array([93.94, 100, 73.51]),
                ),
                (
                    4,
                    "mean4.p4",
                    "col.rf.p4",
                    40,
                    37,
                    40,
                    1,
                    21.5,
                    17,
                    np.array([93.44, 100, 72.49]),
                ),
                (
                    5,
                    "mean4.p5",
                    "col.rf.p5",
                    40,
                    37,
                    40,
                    1,
                    21.5,
                    6,
                    np.array([92.22, 100, 70.12]),
                ),
                (
                    6,
                    "mean4.p6",
                    "col.rf.p6",
                    40,
                    37,
                    40,
                    1,
                    21.5,
                    0.4,
                    np.array([90.56, 100, 58.59]),
                ),
                (
                    7,
                    "mean4.p7",
                    "col.rf.p1",
                    40,
                    37,
                    40,
                    1,
                    21.5,
                    843,
                    np.array([94.04, 100, 76.29]),
                ),
                (
                    8,
                    "mean4.p8",
                    "col.rf.p2",
                    40,
                    37,
                    40,
                    1,
                    21.5,
                    200,
                    np.array([93.04, 100, 72.24]),
                ),
                (
                    9,
                    "mean4.p9",
                    "col.rf.p3",
                    40,
                    37,
                    40,
                    1,
                    21.5,
                    62,
                    np.array([93.94, 100, 73.51]),
                ),
                (
                    10,
                    "mean4.p10",
                    "col.rf.p4",
                    40,
                    37,
                    40,
                    1,
                    21.5,
                    17,
                    np.array([93.44, 100, 72.49]),
                ),
                (
                    11,
                    "mean4.p11",
                    "col.rf.p5",
                    40,
                    37,
                    40,
                    1,
                    21.5,
                    6,
                    np.array([92.22, 100, 70.12]),
                ),
                (
                    12,
                    "mean4.p12",
                    "col.rf.p6",
                    40,
                    37,
                    40,
                    1,
                    21.5,
                    0.4,
                    np.array([90.56, 100, 58.59]),
                ),
            ),
            "R-textile": (
                (
                    1,
                    "kuo.d65.vis",
                    "kuo.d65.col",
                    240,
                    1,
                    12,
                    0.74,
                    16,
                    250,
                    np.array([96.46, 100, 108.62]),
                ),
                (
                    2,
                    "kuo.tl84.vis",
                    "kuo.tl84.col",
                    239,
                    1,
                    10,
                    0.74,
                    16,
                    540,
                    np.array([103.07, 100, 64.29]),
                ),
                (
                    3,
                    "kuo.a.vis",
                    "kuo.a.col",
                    239,
                    1,
                    11,
                    0.74,
                    16,
                    250,
                    np.array([115.19, 100, 23.75]),
                ),
            ),
            "CRT": (
                (
                    1,
                    "lmean.ww",
                    "cold50wl",
                    94,
                    39,
                    44,
                    0.89,
                    100,
                    40,
                    np.array([97.13, 100, 76.62]),
                ),
                (
                    2,
                    "lmean.bb",
                    "cold50gbl",
                    100,
                    39,
                    44,
                    0.89,
                    5,
                    44.5,
                    np.array([97.13, 100, 76.62]),
                ),
                (
                    3,
                    "lmean.gg",
                    "cold50gbl",
                    100,
                    39,
                    44,
                    0.89,
                    20,
                    44.5,
                    np.array([97.13, 100, 76.62]),
                ),
                (
                    4,
                    "lmean.gw",
                    "cold50gbl",
                    100,
                    39,
                    44,
                    0.89,
                    20,
                    44.5,
                    np.array([97.13, 100, 76.62]),
                ),
                (
                    5,
                    "lmean.gb",
                    "cold50gbl",
                    100,
                    39,
                    44,
                    0.89,
                    20,
                    44.5,
                    np.array([97.13, 100, 76.62]),
                ),
                (
                    6,
                    "ld65.gg",
                    "cold65.l",
                    103,
                    39,
                    44,
                    0.81,
                    21.5,
                    40.5,
                    np.array([94.52, 100, 114.98]),
                ),
                (
                    7,
                    "ld65.gw",
                    "cold65.l",
                    103,
                    39,
                    44,
                    0.81,
                    21.5,
                    40.5,
                    np.array([94.52, 100, 114.98]),
                ),
                (
                    8,
                    "lwf.gg",
                    "colwf.l",
                    103,
                    39,
                    44,
                    0.84,
                    21.5,
                    28.4,
                    np.array([102.5, 100, 47.93]),
                ),
                (
                    9,
                    "lwf.gw",
                    "colwf.l",
                    103,
                    39,
                    44,
                    0.84,
                    21.5,
                    28.4,
                    np.array([102.5, 100, 47.93]),
                ),
                (
                    10,
                    "la.gg",
                    "colal.l",
                    61,
                    29,
                    34,
                    0.84,
                    21.5,
                    20.3,
                    np.array([117.26, 100, 22.44]),
                ),
                (
                    11,
                    "la.gw",
                    "colal.l",
                    61,
                    29,
                    34,
                    0.84,
                    21.5,
                    20.3,
                    np.array([117.26, 100, 22.44]),
                ),
            ),
            "35mm": (
                (
                    1,
                    "mean.35.p1",
                    "col.35.p1",
                    99,
                    93,
                    99,
                    1,
                    15.6,
                    75,
                    np.array([92.9, 100, 46.1]),
                ),
                (
                    2,
                    "mean.35.p2",
                    "col.35.p2",
                    99,
                    93,
                    98,
                    1,
                    14.7,
                    75,
                    np.array([86.71, 100, 75.49]),
                ),
                (
                    3,
                    "mean.35.p3",
                    "col.35.p3",
                    99,
                    93,
                    99,
                    1,
                    18.9,
                    113,
                    np.array([92.57, 100, 45.47]),
                ),
                (
                    4,
                    "mean.35.p4",
                    "col.35.p1",
                    99,
                    93,
                    99,
                    1,
                    18.9,
                    45,
                    np.array([92.9, 100, 46.1]),
                ),
                (
                    5,
                    "mean.35.p5",
                    "col.35.p5",
                    95,
                    89,
                    95,
                    1,
                    19.2,
                    47,
                    np.array([93.8, 100, 52.39]),
                ),
                (
                    6,
                    "mean.35.p6",
                    "col.35.p6",
                    36,
                    26,
                    30,
                    1,
                    18.9,
                    113,
                    np.array([95.32, 100, 53.37]),
                ),
            ),
            "LT": (
                (
                    1,
                    "mean.p1",
                    "col.p1",
                    98,
                    94,
                    98,
                    1,
                    15.9,
                    2259,
                    np.array([93.09, 100, 62.02]),
                ),
                (
                    2,
                    "mean.p2",
                    "col.p2",
                    98,
                    94,
                    98,
                    1,
                    17.1,
                    689,
                    np.array([93.23, 100, 61.15]),
                ),
                (
                    3,
                    "mean.p3",
                    "col.p3",
                    98,
                    94,
                    98,
                    1,
                    16.9,
                    325,
                    np.array([92.36, 100, 59.91]),
                ),
                (
                    4,
                    "mean.p4",
                    "col.p4",
                    98,
                    94,
                    98,
                    1,
                    17.4,
                    670,
                    np.array([93.05, 100, 58.58]),
                ),
                (
                    5,
                    "mean.p5t",
                    "col.p5t",
                    97,
                    93,
                    97,
                    1,
                    9.6,
                    1954,
                    np.array([93.3, 100, 59.54]),
                ),
                (
                    6,
                    "mean.p6t",
                    "col.p6t",
                    94,
                    90,
                    94,
                    1,
                    9.5,
                    619,
                    np.array([93.2, 100, 60.48]),
                ),
                (
                    7,
                    "mean.p7t",
                    "col.p7t",
                    93,
                    89,
                    93,
                    1,
                    9.8,
                    319,
                    np.array([92.43, 100, 59.21]),
                ),
                (
                    8,
                    "mean.p8",
                    "col.p8",
                    98,
                    94,
                    98,
                    1,
                    9.4,
                    642,
                    np.array([93.34, 100, 57.98]),
                ),
                (
                    9,
                    "mean.p10",
                    "col.p10",
                    98,
                    94,
                    98,
                    1,
                    9.6,
                    658,
                    np.array([93.34, 100, 57.98]),
                ),
                (
                    10,
                    "mean.p1t",
                    "col.p1t",
                    94,
                    90,
                    94,
                    1,
                    17.5,
                    680,
                    np.array([93.34, 100, 57.98]),
                ),
            ),
            "BIT": (
                (
                    1,
                    "bit_p1.vis",
                    "bit_p1.col",
                    120,
                    1,
                    16,
                    1,
                    0.6,
                    90,
                    np.array([100.6, 100, 113.2]),
                ),
                (
                    2,
                    "bit_p2.vis",
                    "bit_p2.col",
                    120,
                    1,
                    18,
                    1,
                    0.6,
                    3.6,
                    np.array([100.6, 100, 113.2]),
                ),
                (
                    3,
                    "bit_p3.vis",
                    "bit_p3.col",
                    120,
                    1,
                    15,
                    1,
                    0.6,
                    90,
                    np.array([100.6, 100, 113.2]),
                ),
                (
                    4,
                    "bit_p4.vis",
                    "bit_p4.col",
                    90,
                    1,
                    18,
                    1,
                    0.6,
                    90,
                    np.array([100.6, 100, 113.2]),
                ),
                (
                    5,
                    "bit_p5.vis",
                    "bit_p5.col",
                    90,
                    1,
                    12,
                    1,
                    0.6,
                    3.6,
                    np.array([100.6, 100, 113.2]),
                ),
            ),
        }

        filenames = set()
        self._content = {}
        for group, phases in experimental_groups.items():
            experimental_phases = {}
            for (
                phase,
                visual_filename,
                colorimetric_filename,
                samples_count,
                neutrals_start,
                neutrals_end,
                S_Y_c,
                Y_b,
                Y_r,
                XYZ_o,
            ) in phases:
                filenames.add(visual_filename)
                filenames.add(colorimetric_filename)
                phase = str(phase)  # noqa: PLW2901
                visual_path = os.path.join(
                    self.record.repository, "dataset", visual_filename
                )
                visual_data = np.loadtxt(visual_path)
                if visual_data.shape[1] >= 4:
                    visual_data = visual_data[..., -3:]

                colorimetric_path = os.path.join(
                    self.record.repository, "dataset", colorimetric_filename
                )
                colorimetric_data = np.loadtxt(colorimetric_path)
                if colorimetric_data.shape[1] >= 4:
                    colorimetric_data = colorimetric_data[..., -3:]

                if visual_data.shape != colorimetric_data.shape:
                    usage_warning(
                        f'"{visual_filename}" visual and '
                        f'"{colorimetric_filename}" colorimetric file have '
                        f"different shape, using first data rows!"
                    )
                    colorimetric_data = colorimetric_data[:-1, ...]

                experimental_phases[phase] = ExperimentalPhaseLuo1997(
                    phase,
                    as_float_array(visual_data),
                    as_float_array(colorimetric_data),
                    S_Y_c,
                    Y_b,
                    Y_r,
                    XYZ_o,
                    dict(
                        zip(
                            phase_metadata_headers,
                            [samples_count, (neutrals_start, neutrals_end)],
                        )
                    ),
                )

            self._content[group] = ExperimentalGroupLuo1997(
                group,
                experimental_phases,
                dict(
                    zip(
                        group_metadata_headers,
                        experimental_groups_summary[group],
                    )
                ),
            )

        return self._content


_DATASET_LOADER_LUO1997: DatasetLoader_Luo1997 | None = None
"""
Singleton instance of the *Luo and Rhodes (1997)*
*LUTCHI Colour Appearance Data* dataset loader.
"""


def build_Luo1997(load: bool = True) -> DatasetLoader_Luo1997:
    """
    Singleton factory that the builds *Luo and Rhodes (1997)*
    *LUTCHI Colour Appearance Data* dataset loader.

    Parameters
    ----------
    load
        Whether to load the dataset upon instantiation.

    Returns
    -------
    :class:`colour_datasets.loaders.DatasetLoader_Luo1997`
        Singleton instance of the *Luo and Rhodes (1997)*
        *LUTCHI Colour Appearance Data* dataset loader.

    References
    ----------
    :cite:`Luo1991`, :cite:`Luo1991a`, :cite:`Luo1993`, :cite:`Luo1997`
    """

    global _DATASET_LOADER_LUO1997  # noqa: PLW0603

    if _DATASET_LOADER_LUO1997 is None:
        _DATASET_LOADER_LUO1997 = DatasetLoader_Luo1997()
        if load:
            _DATASET_LOADER_LUO1997.load()

    return _DATASET_LOADER_LUO1997
