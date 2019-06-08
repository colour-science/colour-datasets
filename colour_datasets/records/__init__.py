# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .configuration import Configuration, sandbox, use_sandbox
from .zenodo import Community, Record

__all__ = ['Configuration', 'sandbox', 'use_sandbox']
__all__ += ['Community', 'Record']

_COMMUNITY = None
"""
Singleton instance of the *Zenodo* community that holds the datasets
information.

_COMMUNITY : Community
"""


def datasets():
    """
    Singleton factory that returns *Zenodo* community that holds the datasets
    information.

    Returns
    -------
    Community
        Singleton instance of the *Zenodo* community.

    Examples
    --------
    # Doctests skip for Python 2.x compatibility.
    >>> datasets()['3245883'].title  # doctest: +SKIP
    'Camera Spectral Sensitivity Database'
    """

    global _COMMUNITY

    if _COMMUNITY is None:
        _COMMUNITY = Community.from_id(Configuration().community)

    return _COMMUNITY


__all__ += ['datasets']
