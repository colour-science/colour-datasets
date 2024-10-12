"""Define the unit tests for the :mod:`colour_datasets.loaders.xrite2016` module."""


from colour.characterisation import ColourChecker

from colour_datasets.loaders import DatasetLoader_XRite2016, build_XRite2016

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestDatasetLoader_XRite2016",
    "TestBuildXRite2016",
]


class TestDatasetLoader_XRite2016:
    """
    Define :class:`colour_datasets.loaders.xrite2016.DatasetLoader_XRite2016`
    class unit tests methods.
    """

    def test_required_attributes(self):
        """Test the presence of required attributes."""

        required_attributes = ("ID",)

        for attribute in required_attributes:
            assert attribute in dir(DatasetLoader_XRite2016)

    def test_required_methods(self):
        """Test the presence of required methods."""

        required_methods = ("__init__", "load")

        for method in required_methods:
            assert method in dir(DatasetLoader_XRite2016)

    def test_load(self):
        """
        Test :func:`colour_datasets.loaders.xrite2016.\
DatasetLoader_XRite2016.load` method.
        """

        dataset = DatasetLoader_XRite2016()
        assert sorted(dataset.load().keys()) == [
            "ColorChecker24 - After November 2014",
            "ColorChecker24 - Before November 2014",
            "ColorCheckerSG - After November 2014",
            "ColorCheckerSG - Before November 2014",
        ]
        assert (
            isinstance(
                dataset.content["ColorChecker24 - After November 2014"], ColourChecker
            )
            is True
        )


class TestBuildXRite2016:
    """
    Define :func:`colour_datasets.loaders.xrite2016.build_XRite2016`
    definition unit tests methods.
    """

    def test_build_XRite2016(self):
        """
        Test :func:`colour_datasets.loaders.xrite2016.build_XRite2016`
        definition.
        """

        assert build_XRite2016() is build_XRite2016()
