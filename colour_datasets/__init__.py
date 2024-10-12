"""
Colour - Datasets
=================

Colour science datasets for use with
`Colour <https://github.com/colour-science/colour>`__ or any Python package
manipulating colours. The datasets are hosted in
`Zenodo <https://zenodo.org>`__ under the `Colour Science - Datasets \
<https://zenodo.org/communities/colour-science-datasets>`__ community.

Subpackages
-----------
-   loaders: Dataset loaders.
-   records: *Zenodo* records management.
-   utilities:  Various utilities.
"""

import contextlib
import os
import subprocess

import colour
import numpy as np

from .loaders import load
from .records import Community, Configuration, Record, datasets, sandbox

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "Configuration",
]
__all__ += [
    "Community",
    "Record",
    "datasets",
]
__all__ += [
    "sandbox",
]
__all__ += [
    "load",
]

__application_name__ = "Colour - Datasets"

__major_version__ = "0"
__minor_version__ = "2"
__change_version__ = "6"
__version__ = ".".join((__major_version__, __minor_version__, __change_version__))

try:
    _version = (
        subprocess.check_output(
            ["git", "describe"],  # noqa: S603, S607
            cwd=os.path.dirname(__file__),
            stderr=subprocess.STDOUT,
        )
        .strip()
        .decode("utf-8")
    )
except Exception:
    _version = __version__

colour.utilities.ANCILLARY_COLOUR_SCIENCE_PACKAGES["colour-datasets"] = _version  # pyright: ignore

del _version

# TODO: Remove legacy printing support when deemed appropriate.
with contextlib.suppress(TypeError):
    np.set_printoptions(legacy="1.13")
