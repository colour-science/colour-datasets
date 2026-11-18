"""Isolate dataset downloads and deletion tests from the user cache."""

from __future__ import annotations

import os
import sys
from tempfile import TemporaryDirectory

import pytest

_REPOSITORY = pytest.StashKey[TemporaryDirectory[str]]()
_PREVIOUS_REPOSITORY = pytest.StashKey[str | None]()
_REPOSITORY_VARIABLE = "COLOUR_SCIENCE__COLOUR_DATASETS__REPOSITORY"


def pytest_configure(config: pytest.Config) -> None:
    """Give every worker its own temporary dataset repository."""
    if _REPOSITORY in config.stash:
        return
    config.stash[_PREVIOUS_REPOSITORY] = os.environ.get(_REPOSITORY_VARIABLE)
    repository = TemporaryDirectory(prefix="colour-datasets-tests-")
    config.stash[_REPOSITORY] = repository
    os.environ[_REPOSITORY_VARIABLE] = repository.name
    configuration = sys.modules.get("colour_datasets.records.configuration")
    if configuration is not None:
        configuration.DEFAULT_CONFIGURATION["repository"] = repository.name


def pytest_unconfigure(config: pytest.Config) -> None:
    """Remove only the test repository and restore the caller's environment."""
    if _REPOSITORY not in config.stash:
        return
    repository = config.stash[_REPOSITORY]
    del config.stash[_REPOSITORY]
    previous = config.stash[_PREVIOUS_REPOSITORY]
    del config.stash[_PREVIOUS_REPOSITORY]
    if previous is None:
        os.environ.pop(_REPOSITORY_VARIABLE, None)
    else:
        os.environ[_REPOSITORY_VARIABLE] = previous
    configuration = sys.modules.get("colour_datasets.records.configuration")
    if configuration is not None:
        configuration.DEFAULT_CONFIGURATION["repository"] = os.environ.get(
            _REPOSITORY_VARIABLE,
            os.path.join(os.path.expanduser("~"), ".colour-science", "colour-datasets"),
        )
    repository.cleanup()
