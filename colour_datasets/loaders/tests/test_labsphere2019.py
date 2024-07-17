"""
Define the unit tests for the :mod:`colour_datasets.loaders.labsphere2019`
module.
"""


from colour import SpectralShape

from colour_datasets.loaders import (
    DatasetLoader_Labsphere2019,
    build_Labsphere2019,
)

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestDatasetLoader_Labsphere2019",
    "TestBuildLabsphere2019",
]


class TestDatasetLoader_Labsphere2019:
    """
    Define :class:`colour_datasets.loaders.labsphere2019.\
DatasetLoader_Labsphere2019` class unit tests methods.
    """

    def test_required_attributes(self):
        """Test the presence of required attributes."""

        required_attributes = ("ID",)

        for attribute in required_attributes:
            assert attribute in dir(DatasetLoader_Labsphere2019)

    def test_required_methods(self):
        """Test the presence of required methods."""

        required_methods = ("__init__", "load")

        for method in required_methods:
            assert method in dir(DatasetLoader_Labsphere2019)

    def test_load(self):
        """
        Test :func:`colour_datasets.loaders.labsphere2019.\
DatasetLoader_Labsphere2019.load` method.
        """

        dataset = DatasetLoader_Labsphere2019()
        assert sorted(dataset.load().keys()) == ["Labsphere SRS-99-020"]
        assert dataset.content["Labsphere SRS-99-020"].shape == SpectralShape(
            250, 2500, 1
        )


class TestBuildLabsphere2019:
    """
    Define :func:`colour_datasets.loaders.labsphere2019.build_Labsphere2019`
    definition unit tests methods.
    """

    def test_build_Labsphere2019(self):
        """
        Test :func:`colour_datasets.loaders.labsphere2019.build_Labsphere2019`
        definition.
        """

        assert build_Labsphere2019() is build_Labsphere2019()
