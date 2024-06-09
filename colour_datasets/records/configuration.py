"""
Configuration
=============

Define various objects related to the configuration of *Colour - Datasets*.
"""

from __future__ import annotations

import functools
import os

from colour.hints import Any, Callable, Dict
from colour.utilities import Structure
from colour.utilities.documentation import (
    DocstringDict,
    is_documentation_building,
)

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "DEFAULT_CONFIGURATION",
    "Configuration",
    "use_sandbox",
    "sandbox",
]

DEFAULT_CONFIGURATION: Dict = {
    "repository": os.environ.get(
        "COLOUR_SCIENCE__COLOUR_DATASETS__REPOSITORY",
        os.path.join(
            os.path.expanduser("~"),
            ".colour-science",
            "colour-datasets",
        ),
    ),
    "downloads_directory": "downloads",
    "deflate_directory": "dataset",
    "api_url": "https://zenodo.org/api",
    "community": "colour-science-datasets",
    "urls_txt_file": "urls.txt",
}
if is_documentation_building():  # pragma: no cover
    DEFAULT_CONFIGURATION = DocstringDict(DEFAULT_CONFIGURATION)
    DEFAULT_CONFIGURATION.__doc__ = """
*Colour - Datasets* default configuration.
"""


class Configuration(Structure):
    """
    *Colour - Datasets* configuration factory based on
    :class:`colour.utilities.Structure` class and allowing to access key values
    using dot syntax.

    Parameters
    ----------
    configuration
        Configuration to use instead of the default one.
    """

    def __init__(self, configuration: Dict | None = None) -> None:
        super().__init__(
            DEFAULT_CONFIGURATION if configuration is None else configuration
        )


def use_sandbox(
    state: bool = True,
    api_url: str = "https://sandbox.zenodo.org/api",
    community: str = "colour-science-datasets",
):
    """
    Modify the *Colour - Datasets* configuration to use *Zenodo* sandbox.

    Parameters
    ----------
    state
        Whether to use *Zenodo* sandbox.
    api_url
        *Zenodo* sandbox url.
    community
        *Zenodo* community.
    """

    global DEFAULT_CONFIGURATION  # noqa: PLW0602

    if state:
        DEFAULT_CONFIGURATION["api_url"] = api_url
        DEFAULT_CONFIGURATION["community"] = community
    else:
        DEFAULT_CONFIGURATION["api_url"] = "https://zenodo.org/api"
        DEFAULT_CONFIGURATION["community"] = "colour-science-datasets"


class sandbox:
    """
    A context manager and decorator temporarily setting the configuration to
    the *Zenodo* sandbox.

    Parameters
    ----------
    api_url
        *Zenodo* sandbox url.
    community
        *Zenodo* community.
    """

    def __init__(
        self,
        api_url: str = "https://sandbox.zenodo.org/api",
        community: str = "colour-science-datasets",
    ) -> None:
        self._api_url = api_url
        self._community = community

    def __enter__(self) -> sandbox:
        """
        Set the configuration to the *Zenodo* sandbox upon entering the context
        manager.
        """

        use_sandbox(True, self._api_url, self._community)

        return self

    def __exit__(self, *args: Any):
        """Restore the configuration upon exiting the context manager."""

        use_sandbox(False)

    def __call__(self, function: Callable) -> Callable:
        """Call the wrapped definition."""

        @functools.wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Callable:
            with self:
                return function(*args, **kwargs)

        return wrapper
