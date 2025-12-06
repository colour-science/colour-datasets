"""
Colour - Datasets
=================

Colour science datasets for use with
`Colour <https://github.com/colour-science/colour>`__ or any Python package
manipulating colours. The datasets are hosted in
`Zenodo <https://zenodo.org>`__ under the `Colour Science - Datasets \
<https://zenodo.org/communities/colour-science-datasets>`__ community.

This package provides access to standardised colour science datasets including
spectral power distributions, colour matching functions, and experimental data
from research publications.

Subpackages
-----------
-   loaders: Dataset loading and parsing utilities.
-   records: *Zenodo* records management and configuration.
-   utilities: Common utilities for dataset processing.
"""

from __future__ import annotations

import contextlib
import os
import subprocess

import colour
import numpy as np

# isort: split

from .loaders import load

# isort: split

from .records import Community, Configuration, Record, datasets, sandbox

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "load",
]
__all__ += [
    "Community",
    "Configuration",
    "Record",
    "datasets",
    "sandbox",
]

__application_name__ = "Colour - Datasets"

__major_version__ = "0"
__minor_version__ = "2"
__change_version__ = "7"
__version__ = f"{__major_version__}.{__minor_version__}.{__change_version__}"

try:
    _version = (
        subprocess.check_output(
            ["git", "describe"],  # noqa: S607
            cwd=os.path.dirname(__file__),
            stderr=subprocess.STDOUT,
        )
        .strip()
        .decode("utf-8")
    )
except Exception:  # noqa: BLE001
    _version = __version__

colour.utilities.ANCILLARY_COLOUR_SCIENCE_PACKAGES["colour-datasets"] = _version  # pyright: ignore

del _version

# TODO: Remove legacy printing support when deemed appropriate.
with contextlib.suppress(TypeError):
    np.set_printoptions(legacy="1.13")
