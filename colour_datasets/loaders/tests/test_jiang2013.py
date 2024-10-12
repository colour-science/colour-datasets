"""Define the unit tests for the :mod:`colour_datasets.loaders.jiang2013` module."""


from colour import SpectralShape

from colour_datasets.loaders import DatasetLoader_Jiang2013, build_Jiang2013

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestDatasetLoader_Jiang2013",
    "TestBuildJiang2013",
]


class TestDatasetLoader_Jiang2013:
    """
    Define :class:`colour_datasets.loaders.jiang2013.DatasetLoader_Jiang2013`
    class unit tests methods.
    """

    def test_required_attributes(self):
        """Test the presence of required attributes."""

        required_attributes = ("ID",)

        for attribute in required_attributes:
            assert attribute in dir(DatasetLoader_Jiang2013)

    def test_required_methods(self):
        """Test the presence of required methods."""

        required_methods = ("__init__", "load")

        for method in required_methods:
            assert method in dir(DatasetLoader_Jiang2013)

    def test_load(self):
        """
        Test :func:`colour_datasets.loaders.jiang2013.\
DatasetLoader_Jiang2013.load` method.
        """

        dataset = DatasetLoader_Jiang2013()
        assert sorted(dataset.load().keys()) == [
            "Canon 1DMarkIII",
            "Canon 20D",
            "Canon 300D",
            "Canon 40D",
            "Canon 500D",
            "Canon 50D",
            "Canon 5DMarkII",
            "Canon 600D",
            "Canon 60D",
            "Hasselblad H2",
            "Nikon D200",
            "Nikon D3",
            "Nikon D300s",
            "Nikon D3X",
            "Nikon D40",
            "Nikon D50",
            "Nikon D5100",
            "Nikon D700",
            "Nikon D80",
            "Nikon D90",
            "Nokia N900",
            "Olympus E-PL2",
            "Pentax K-5",
            "Pentax Q",
            "Phase One",
            "Point Grey Grasshopper 50S5C",
            "Point Grey Grasshopper2 14S5C",
            "SONY NEX-5N",
        ]
        assert dataset.content["Canon 1DMarkIII"].shape == SpectralShape(400, 720, 10)


class TestBuildJiang2013:
    """
    Define :func:`colour_datasets.loaders.jiang2013.build_Jiang2013`
    definition unit tests methods.
    """

    def test_build_Jiang2013(self):
        """
        Test :func:`colour_datasets.loaders.jiang2013.build_Jiang2013`
        definition.
        """

        assert build_Jiang2013() is build_Jiang2013()
