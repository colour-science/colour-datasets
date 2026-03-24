"""Define the unit tests for the :mod:`colour_datasets.loaders.wilkie2021` module."""

from colour_datasets.loaders import (
    DatasetLoader_Wilkie2021,
    build_Wilkie2021,
)

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestDatasetLoader_Wilkie2021",
    "TestBuildWilkie2021",
]

try:
    from colour.phenomena.sky.wilkie2021 import SkyDataset_Wilkie2021
except ImportError:
    SkyDataset_Wilkie2021 = None


class TestDatasetLoader_Wilkie2021:
    """
    Define :class:`colour_datasets.loaders.wilkie2021.DatasetLoader_Wilkie2021`
    class unit tests methods.
    """

    def test_required_attributes(self) -> None:
        """Test the presence of required attributes."""

        required_attributes = ("ID",)

        for attribute in required_attributes:
            assert attribute in dir(DatasetLoader_Wilkie2021)

    def test_required_methods(self) -> None:
        """Test the presence of required methods."""

        required_methods = ("__init__", "load")

        for method in required_methods:
            assert method in dir(DatasetLoader_Wilkie2021)

    def test_load(self) -> None:
        """
        Test :func:`colour_datasets.loaders.wilkie2021.\
DatasetLoader_Wilkie2021.load` method.
        """

        dataset = DatasetLoader_Wilkie2021()
        content = dataset.load()

        assert "ground" in content

        if SkyDataset_Wilkie2021 is not None:
            assert content["ground"].channels == 11
        else:
            assert isinstance(content["ground"], str)


class TestBuildWilkie2021:
    """
    Define :func:`colour_datasets.loaders.wilkie2021.build_Wilkie2021`
    definition unit tests methods.
    """

    def test_build_Wilkie2021(self) -> None:
        """
        Test :func:`colour_datasets.loaders.wilkie2021.build_Wilkie2021`
        definition.
        """

        assert isinstance(build_Wilkie2021(), DatasetLoader_Wilkie2021) is True
