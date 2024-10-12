"""Define the unit tests for the :mod:`colour_datasets.loaders.solomotav2023` module."""


from colour import SpectralShape

from colour_datasets.loaders import (
    DatasetLoader_Solomotav2023,
    build_Solomotav2023,
)

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestDatasetLoader_Solomotav2023",
    "TestBuildSolomotav2023",
]


class TestDatasetLoader_Solomotav2023:
    """
    Define :class:`colour_datasets.loaders.solomotav2023.DatasetLoader_Solomotav2023`
    class unit tests methods.
    """

    def test_required_attributes(self):
        """Test the presence of required attributes."""

        required_attributes = ("ID",)

        for attribute in required_attributes:
            assert attribute in dir(DatasetLoader_Solomotav2023)

    def test_required_methods(self):
        """Test the presence of required methods."""

        required_methods = ("__init__", "load")

        for method in required_methods:
            assert method in dir(DatasetLoader_Solomotav2023)

    def test_load(self):
        """
        Test :func:`colour_datasets.loaders.solomotav2023.\
DatasetLoader_Solomotav2023.load` method.
        """

        dataset = DatasetLoader_Solomotav2023()
        assert list(dataset.load().keys()) == ["Estimated", "Ground Truth"]

        assert dataset.content["Estimated"]["Canon EOS 1D C"].shape == SpectralShape(
            400, 700, 10
        )


class TestBuildSolomotav2023:
    """
    Define :func:`colour_datasets.loaders.solomotav2023.build_Solomotav2023`
    definition unit tests methods.
    """

    def test_build_Solomotav2023(self):
        """
        Test :func:`colour_datasets.loaders.solomotav2023.build_Solomotav2023`
        definition.
        """

        assert build_Solomotav2023() is build_Solomotav2023()
