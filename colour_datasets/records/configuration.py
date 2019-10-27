# -*- coding: utf-8 -*-
"""
Configuration
=============

Defines various objects related to the configuration of *Colour - Datasets*.
"""

from __future__ import division, unicode_literals

import functools
import os

from colour.utilities import Structure
from colour.utilities.documentation import DocstringDict

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['DEFAULT_CONFIGURATION', 'Configuration', 'use_sandbox', 'sandbox']

DEFAULT_CONFIGURATION = DocstringDict({
    'repository':
        os.environ.get(
            'COLOUR_SCIENCE__COLOUR_DATASETS__REPOSITORY',
            os.path.join(
                os.path.expanduser('~'),
                '.colour-science',
                'colour-datasets',
            )),
    'downloads_directory':
        'downloads',
    'deflate_directory':
        'dataset',
    'api_url':
        'https://zenodo.org/api',
    'community':
        'colour-science-datasets',
    'urls_txt_file':
        'urls.txt',
})

DEFAULT_CONFIGURATION.__doc__ = """
*Colour - Datasets* default configuration.

DEFAULT_CONFIGURATION : dict
"""


class Configuration(Structure):
    """
    *Colour - Datasets* configuration factory based on
    :class:`colour.utilities.Structure` class and allowing to access key values
    using dot syntax.

    Parameters
    ----------
    configuration : dict, optional
        Configuration to use instead of the default one.
    """

    def __init__(self, configuration=None):
        super(Configuration, self).__init__(
            DEFAULT_CONFIGURATION if configuration is None else configuration)


def use_sandbox(state=True,
                api_url='https://sandbox.zenodo.org/api',
                community='colour-science-datasets'):
    """
    Modifies the *Colour - Datasets* configuration to use *Zenodo* sandbox.

    Parameters
    ----------
    state : bool, optional
        Whether to use *Zenodo* sandbox.
    api_url : unicode, optional
        *Zenodo* sandbox url.
    community : unicode, optional
        *Zenodo* community.
    """

    global DEFAULT_CONFIGURATION

    if state:
        DEFAULT_CONFIGURATION['api_url'] = api_url
        DEFAULT_CONFIGURATION['community'] = community
    else:
        DEFAULT_CONFIGURATION['api_url'] = 'https://zenodo.org/api'
        DEFAULT_CONFIGURATION['community'] = 'colour-science-datasets'


class sandbox(object):
    """
    A context manager and decorator temporarily setting the configuration to
    use *Zenodo* sandbox.

    Parameters
    ----------
    api_url : unicode, optional
        *Zenodo* sandbox url.
    community : unicode, optional
        *Zenodo* community.
    """

    def __init__(self,
                 api_url='https://sandbox.zenodo.org/api',
                 community='colour-science-datasets'):

        self._api_url = api_url
        self._community = community

    def __enter__(self):
        """
        Called upon entering the context manager and decorator.
        """

        use_sandbox(True, self._api_url, self._community)

        return self

    def __exit__(self, *args):
        """
        Called upon exiting the context manager and decorator.
        """

        use_sandbox(False)

    def __call__(self, function):
        """
        Calls the wrapped definition.
        """

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            with self:
                return function(*args, **kwargs)

        return wrapper
