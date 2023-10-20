from __future__ import annotations


from .configuration import Configuration, sandbox, use_sandbox
from .zenodo import Community, Record

__all__ = [
    "Configuration",
    "sandbox",
    "use_sandbox",
]
__all__ += [
    "Community",
    "Record",
]

_COMMUNITY: Community | None = None
"""
Singleton instance of the *Zenodo* community that holds the datasets
information.
"""


def datasets() -> Community:
    """
    Singleton factory that returns *Zenodo* community that holds the datasets
    information.

    Returns
    -------
    :class:`colour_datasets.Community`
        Singleton instance of the *Zenodo* community.

    Examples
    --------
    >>> datasets()["3245883"].title
    'Camera Spectral Sensitivity Database - Jiang et al. (2013)'
    """

    global _COMMUNITY  # noqa: PLW0603

    if _COMMUNITY is None:
        _COMMUNITY = Community.from_id(Configuration().community)

    return _COMMUNITY


__all__ += [
    "datasets",
]
