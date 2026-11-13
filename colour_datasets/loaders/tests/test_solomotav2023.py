"""Define the unit tests for the :mod:`colour_datasets.loaders.solomotav2023` module."""

import os
import tempfile
import zipfile
from unittest.mock import patch

from colour import SpectralShape

from colour_datasets.loaders import (
    DatasetLoader_Solomotav2023,
    build_Solomotav2023,
)
from colour_datasets.records import Configuration, Record

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

    def test_required_attributes(self) -> None:
        """Test the presence of required attributes."""

        required_attributes = ("ID",)

        for attribute in required_attributes:
            assert attribute in dir(DatasetLoader_Solomotav2023)

    def test_required_methods(self) -> None:
        """Test the presence of required methods."""

        required_methods = ("__init__", "load")

        for method in required_methods:
            assert method in dir(DatasetLoader_Solomotav2023)

    def test_load_portable_archive_names(self) -> None:
        """Retain camera names that cannot be extracted on Windows."""

        with tempfile.TemporaryDirectory() as directory:
            configuration = Configuration(dict(Configuration()))
            configuration.repository = directory
            record = Record({"id": self.__class__.__name__}, configuration)
            downloads = os.path.join(record.repository, "downloads")
            os.makedirs(downloads)
            os.mkdir(os.path.join(record.repository, "dataset"))
            csv_data = "wavelength,R,G,B\n" + "".join(
                f"{wavelength},0.1,0.2,0.3\n" for wavelength in range(400, 701, 10)
            )
            for basename in ("csv", "ground-truths"):
                with zipfile.ZipFile(
                    os.path.join(downloads, f"{basename}.zip"), "w"
                ) as archive:
                    for name in ("Pentax-*istD", "Camera-A", "camera-a"):
                        archive.writestr(f"{basename}/{name}.csv", csv_data)
                    archive.writestr(f"__MACOSX/{basename}/._metadata.csv", "metadata")
            with patch(
                "colour_datasets.loaders.solomotav2023.datasets",
                return_value={DatasetLoader_Solomotav2023.ID: record},
            ):
                dataset = DatasetLoader_Solomotav2023()
            content = dataset.load()
            for group in ("Estimated", "Ground Truth"):
                assert set(content[group]) == {"Pentax *istD", "Camera A", "camera a"}
                assert content[group]["Pentax *istD"].shape == SpectralShape(
                    400, 700, 10
                )

    def test_load(self) -> None:
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

    def test_build_Solomotav2023(self) -> None:
        """
        Test :func:`colour_datasets.loaders.solomotav2023.build_Solomotav2023`
        definition.
        """

        assert isinstance(build_Solomotav2023(), DatasetLoader_Solomotav2023) is True
