"""
Define the unit tests for the :mod:`colour_datasets.loaders.brendel2020`
module.
"""

from colour import SpectralShape

from colour_datasets.loaders import (
    DatasetLoader_Brendel2020,
    build_Brendel2020,
)

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestDatasetLoader_Brendel2020",
    "TestBuildBrendel2020",
]


class TestDatasetLoader_Brendel2020:
    """
    Define :class:`colour_datasets.loaders.brendel2020.\
DatasetLoader_Brendel2020` class unit tests methods.
    """

    def test_required_attributes(self):
        """Test the presence of required attributes."""

        required_attributes = ("ID",)

        for attribute in required_attributes:
            assert attribute in dir(DatasetLoader_Brendel2020)

    def test_required_methods(self):
        """Test the presence of required methods."""

        required_methods = ("__init__", "load")

        for method in required_methods:
            assert method in dir(DatasetLoader_Brendel2020)

    def test_load(self):
        """
        Test :func:`colour_datasets.loaders.brendel2020.\
DatasetLoader_Brendel2020.load` method.
        """

        dataset = DatasetLoader_Brendel2020()

        assert len(dataset.load()) == 29

        assert dataset.content[
            "556nm - LED 11 - Brendel (2020)"
        ].shape == SpectralShape(350, 700, 2)


class TestBuildBrendel2020:
    """
    Define :func:`colour_datasets.loaders.brendel2020.build_Brendel2020`
    definition unit tests methods.
    """

    def test_build_Brendel2020(self):
        """
        Test :func:`colour_datasets.loaders.brendel2020.build_Brendel2020`
        definition.
        """

        assert build_Brendel2020() is build_Brendel2020()
