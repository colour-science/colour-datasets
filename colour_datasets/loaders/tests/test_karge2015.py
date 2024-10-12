"""Define the unit tests for the :mod:`colour_datasets.loaders.karge2015` module."""


from colour import SpectralShape

from colour_datasets.loaders import DatasetLoader_Karge2015, build_Karge2015

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestDatasetLoader_Karge2015",
    "TestBuildKarge2015",
]


class TestDatasetLoader_Karge2015:
    """
    Define :class:`colour_datasets.loaders.karge2015.DatasetLoader_Karge2015`
    class unit tests methods.
    """

    def test_required_attributes(self):
        """Test the presence of required attributes."""

        required_attributes = ("ID",)

        for attribute in required_attributes:
            assert attribute in dir(DatasetLoader_Karge2015)

    def test_required_methods(self):
        """Test the presence of required methods."""

        required_methods = ("__init__", "load")

        for method in required_methods:
            assert method in dir(DatasetLoader_Karge2015)

    def test_load(self):
        """
        Test :func:`colour_datasets.loaders.karge2015.\
DatasetLoader_Karge2015.load` method.
        """

        dataset = DatasetLoader_Karge2015()
        assert sorted(dataset.load().keys()) == [
            "Arri HMI",
            "Arri LED",
            "Arri TU",
            "Bron Kobold FL",
            "Bron Kobold HMI",
            "CMT Kinoflo FL",
            "Dedolight TU",
        ]
        assert dataset.content["Arri HMI"]["Raw"][
            "Arri_Compact125W_HMI_Spot"
        ].shape == SpectralShape(380, 780, 4)


class TestBuildKarge2015:
    """
    Define :func:`colour_datasets.loaders.karge2015.build_Karge2015`
    definition unit tests methods.
    """

    def test_build_Karge2015(self):
        """
        Test :func:`colour_datasets.loaders.karge2015.build_Karge2015`
        definition.
        """

        assert build_Karge2015() is build_Karge2015()
