# -*- coding: utf-8 -*-
"""
Colour - Datasets
=================

Colour science datasets for use with
`Colour <https://github.com/colour-science/colour>`_ or any Python package
manipulating colours. The datasets are hosted in `Zenodo <https://zenodo.org>`_
under the `Colour Science - Datasets \
<https://zenodo.org/communities/colour-science-datasets/>`_ community.

Subpackages
-----------
-   loaders: Dataset loaders.
-   records: *Zenodo* records management.
-   utilities:  Various utilities.
"""

from __future__ import absolute_import

import numpy as np
import os
import subprocess  # nosec

import colour

from .records import Configuration
from .records import Community, Record, datasets
from .records import sandbox
from .loaders import load

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['Configuration']
__all__ += ['Community', 'Record', 'datasets']
__all__ += ['sandbox']
__all__ += ['load']

__application_name__ = 'Colour - Datasets'

__major_version__ = '0'
__minor_version__ = '1'
__change_version__ = '0'
__version__ = '.'.join(
    (__major_version__,
     __minor_version__,
     __change_version__))  # yapf: disable

try:
    version = subprocess.check_output(  # nosec
        ['git', 'describe'],
        cwd=os.path.dirname(__file__),
        stderr=subprocess.STDOUT).strip()
    version = version.decode('utf-8')
except Exception:
    version = __version__

colour.utilities.ANCILLARY_COLOUR_SCIENCE_PACKAGES['colour-datasets'] = (
    version)

# TODO: Remove legacy printing support when deemed appropriate.
try:
    np.set_printoptions(legacy='1.13')
except TypeError:
    pass
