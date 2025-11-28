"""
Constant Hue Loci Data - Hung and Berns (1995)
==============================================

Define the objects implementing support for *Hung and Berns (1995)* *Constant
Hue Loci Data* dataset loading:

-   :class:`colour_datasets.loaders.DatasetLoader_Hung1995`
-   :func:`colour_datasets.loaders.build_Hung1995`

References
----------
-   :cite:`Hung1995` : Hung, P.-C., & Berns, R. S. (1995). Determination of
    constant Hue Loci for a CRT gamut and their predictions using color
    appearance spaces. Color Research & Application, 20(5), 285-295.
    doi:10.1002/col.5080200506
"""

from __future__ import annotations

import csv
import os
import typing
from dataclasses import dataclass

import numpy as np
from colour import CCS_ILLUMINANTS, xy_to_XYZ, xyY_to_XYZ

if typing.TYPE_CHECKING:
    from colour.hints import Dict, NDArrayFloat

from colour.utilities import as_float_array

from colour_datasets.loaders import AbstractDatasetLoader
from colour_datasets.records import datasets

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "ConstantPerceivedHueColourMatches_Hung1995",
    "DatasetLoader_Hung1995",
    "build_Hung1995",
]


@dataclass(frozen=True)
class ConstantPerceivedHueColourMatches_Hung1995:
    """
    Define *Hung and Berns (1995)* *Constant Hue Loci Data*
    colour matches data for a given hue angle.

    Parameters
    ----------
    name
        *Hung and Berns (1995)* *Constant Hue Loci Data* hue angle or
        name.
    XYZ_r
        *CIE XYZ* tristimulus values of the reference illuminant.
    XYZ_cr
        *CIE XYZ* tristimulus values of the reference colour under the
        reference illuminant.
    XYZ_ct
        *CIE XYZ* tristimulus values of the colour matches under the reference
        illuminant.
    metadata
        Dataset metadata.
    """

    name: str
    XYZ_r: NDArrayFloat
    XYZ_cr: NDArrayFloat
    XYZ_ct: NDArrayFloat
    metadata: Dict

    def __post_init__(self) -> None:
        """Post-initialise the class."""

        object.__setattr__(self, "XYZ_r", as_float_array(self.XYZ_r))
        object.__setattr__(self, "XYZ_cr", as_float_array(self.XYZ_cr))
        object.__setattr__(self, "XYZ_ct", as_float_array(self.XYZ_ct))


class DatasetLoader_Hung1995(AbstractDatasetLoader):
    """
    Define the *Hung and Berns (1995)* *Constant Hue Loci Data*
    dataset loader.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.DatasetLoader_Hung1995.ID`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.DatasetLoader_Hung1995.__init__`
    -   :meth:`colour_datasets.loaders.DatasetLoader_Hung1995.load`

    References
    ----------
    :cite:`Hung1995`
    """

    ID: str = "3367463"
    """Dataset record id, i.e., the *Zenodo* record number."""

    def __init__(self) -> None:
        super().__init__(datasets()[DatasetLoader_Hung1995.ID])

    def load(
        self,
    ) -> Dict[str, Dict[str, ConstantPerceivedHueColourMatches_Hung1995]]:
        """
        Sync, parse, convert and return the *Hung and Berns (1995)*
        *Constant Hue Loci Data* dataset content.

        Returns
        -------
        :class:`dict`
            *Hung and Berns (1995)* *Constant Hue Loci Data* dataset content.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = DatasetLoader_Hung1995()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.content.keys())
        6
        """

        super().sync()

        self._content = {}

        filenames = {
            "Table I.csv": "Reference colors.",
            "Table II.csv": "Intra- and interobserver variances for each "
            "reference hue expressed in circumferential "
            "hue-angle difference.",
            "Table III.csv": "Weight-averaged constant hue loci for the CL experiment.",
            "Table IV.csv": "Weight-averaged constant hue loci for the VL experiment.",
        }

        for filename in filenames:
            datafile_path = os.path.join(self.record.repository, "dataset", filename)

            # NOTE: Use csv module to avoid NumPy 2.x genfromtxt dtype=None errors
            with open(datafile_path, encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                headers = [h.strip().replace(" ", "_") for h in next(reader)]
                rows = []
                for row in reader:
                    converted = []
                    for value in row:
                        try:
                            converted.append(float(value))
                        except ValueError:
                            converted.append(value)
                    rows.append(tuple(converted))

            dtypes = [(name, object) for name in headers]
            data = np.array(rows, dtype=dtypes)
            self._content[filename.split(".")[0]] = data

        hues = [
            "Red",
            "Red-yellow",
            "Yellow",
            "Yellow-green",
            "Green",
            "Green-cyan",
            "Cyan",
            "Cyan-blue",
            "Blue",
            "Blue-magenta",
            "Magenta",
            "Magenta-red",
        ]

        XYZ_r = xy_to_XYZ(CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["C"])

        for table, experiment in [("Table III", "CL"), ("Table IV", "VL")]:
            key = f"Constant Hue Loci Data - {experiment}"
            self._content[key] = {}
            for hue in hues:
                for sample_r in self._content["Table I"]:
                    sample_r = sample_r.tolist()  # noqa: PLW2901
                    if sample_r[0] == hue:
                        XYZ_cr = xyY_to_XYZ(sample_r[1:4]) / 100
                        break

                XYZ_ct = []
                metadata: Dict = {
                    "Color name": [],
                    "C*uv": [],
                }
                for sample_t in self._content[table]:
                    sample_t = sample_t.tolist()  # noqa: PLW2901
                    if sample_t[0] != hue:
                        continue

                    XYZ_ct.append(sample_t[2:])
                    metadata["Color name"].append(sample_t[0])
                    metadata["C*uv"].append(sample_t[1])

                self._content[key][hue] = ConstantPerceivedHueColourMatches_Hung1995(
                    hue, XYZ_r, XYZ_cr, np.vstack(XYZ_ct) / 100, metadata
                )

        return self._content


_DATASET_LOADER_HUNG1995: DatasetLoader_Hung1995 | None = None
"""
Singleton instance of the *Hung and Berns (1995)*
*Constant Hue Loci Data* dataset loader.
"""


def build_Hung1995(load: bool = True) -> DatasetLoader_Hung1995:
    """
    Singleton factory that builds the *Hung and Berns (1995)*
    *Constant Hue Loci Data* dataset loader.

    Parameters
    ----------
    load
        Whether to load the dataset upon instantiation.

    Returns
    -------
    :class:`colour_datasets.loaders.DatasetLoader_Hung1995`
        Singleton instance of the *Hung and Berns (1995)*
        *Constant Hue Loci Data* dataset loader.

    References
    ----------
    :cite:`Hung1995`
    """

    global _DATASET_LOADER_HUNG1995  # noqa: PLW0603

    if _DATASET_LOADER_HUNG1995 is None:
        _DATASET_LOADER_HUNG1995 = DatasetLoader_Hung1995()
        if load:
            _DATASET_LOADER_HUNG1995.load()

    return _DATASET_LOADER_HUNG1995
