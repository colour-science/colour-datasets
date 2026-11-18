"""Apply the package test isolation hooks to release-task regressions."""

from colour_datasets.conftest import pytest_configure, pytest_unconfigure

__all__ = ["pytest_configure", "pytest_unconfigure"]
