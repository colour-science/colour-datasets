"""Define the unit tests for the :mod:`colour_datasets.loaders.jakob2019` module."""


from colour_datasets.loaders import DatasetLoader_Jakob2019, build_Jakob2019

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestDatasetLoader_Jakob2019",
    "TestBuildJakob2019",
]


class TestDatasetLoader_Jakob2019:
    """
    Define :class:`colour_datasets.loaders.jakob2019.DatasetLoader_Jakob2019`
    class unit tests methods.
    """

    def test_required_attributes(self):
        """Test the presence of required attributes."""

        required_attributes = ("ID",)

        for attribute in required_attributes:
            assert attribute in dir(DatasetLoader_Jakob2019)

    def test_required_methods(self):
        """Test the presence of required methods."""

        required_methods = ("__init__", "load")

        for method in required_methods:
            assert method in dir(DatasetLoader_Jakob2019)

    def test_load(self):
        """
        Test :func:`colour_datasets.loaders.jakob2019.\
DatasetLoader_Jakob2019.load` method.
        """

        dataset = DatasetLoader_Jakob2019()
        assert sorted(dataset.load().keys()) == [
            "ACES2065-1",
            "ITU-R BT.2020",
            "ProPhoto RGB",
            "sRGB",
        ]


class TestBuildJakob2019:
    """
    Define :func:`colour_datasets.loaders.jakob2019.build_Jakob2019`
    definition unit tests methods.
    """

    def test_build_Jakob2019(self):
        """
        Test :func:`colour_datasets.loaders.jakob2019.build_Jakob2019`
        definition.
        """

        assert build_Jakob2019() is build_Jakob2019()
