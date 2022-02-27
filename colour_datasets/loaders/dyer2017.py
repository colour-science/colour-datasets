"""
RAW to ACES Utility Data - Dyer et al. (2017)
=============================================

Defines the objects implementing support for *Dyer, Forsythe, Irons, Mansencal
and Zhu (2017)* *RAW to ACES Utility Data* dataset loading:

-   :class:`colour_datasets.loaders.DatasetLoader_Dyer2017`
-   :func:`colour_datasets.loaders.build_Dyer2017`

References
----------
-   :cite:`Dyer2017` : Dyer, S., Forsythe, A., Irons, J., Mansencal, T., & Zhu,
    M. (2017). RAW to ACES Utility Data.
"""

from __future__ import annotations

import json
import glob
import os

from colour import MultiSpectralDistributions, SpectralDistribution
from colour.continuous import MultiSignals, Signal
from colour.hints import (
    Any,
    Boolean,
    Dict,
    Floating,
    Literal,
    Optional,
    Type,
    Union,
    cast,
)
from colour.utilities import attest, is_numeric, is_string, optional

from colour_datasets.loaders import AbstractDatasetLoader
from colour_datasets.records import datasets

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "New BSD License - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "SpectralDataHeader_AMPAS",
    "SpectralDistribution_AMPAS",
    "MultiSpectralDistributions_AMPAS",
    "DatasetLoader_Dyer2017",
    "build_Dyer2017",
]


class SpectralDataHeader_AMPAS:
    """
    Define the header object for an *A.M.P.A.S* spectral data.

    Parameters
    ----------
    schema_version
        Version of the *A.M.P.A.S* spectral data schema.
    catalog_number
        Manufacturer's product catalog number.
    description
        Description of the spectral data in the spectral data JSON file.
    document_creator
        Creator of the spectral data JSON file, which may be a
        test lab, a research group, a standard body, a company or an
        individual.
    unique_identifier
        Description of the equipment used to measure the spectral data.
    measurement_equipment
        Description of the equipment used to measure the spectral data.
    laboratory
        Testing laboratory name that performed the spectral data measurements.
    document_creation_date
        Spectral data JSON file creation date using the
        *JSON DateTime Data Type*, *YYYY-MM-DDThh:mm:ss*.
    comments
        Additional information relating to the tested and reported data.
    license
        License under which the data is distributed.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.dyer2017.SpectralDataHeader_AMPAS.\
schema_version
    -   :attr:`colour_datasets.loaders.dyer2017.SpectralDataHeader_AMPAS.\
catalog_number
    -   :attr:`colour_datasets.loaders.dyer2017.SpectralDataHeader_AMPAS.\
description
    -   :attr:`colour_datasets.loaders.dyer2017.SpectralDataHeader_AMPAS.\
document_creator
    -   :attr:`colour_datasets.loaders.dyer2017.SpectralDataHeader_AMPAS.\
unique_identifier
    -   :attr:`colour_datasets.loaders.dyer2017.SpectralDataHeader_AMPAS.\
measurement_equipment
    -   :attr:`colour_datasets.loaders.dyer2017.SpectralDataHeader_AMPAS.\
laboratory
    -   :attr:`colour_datasets.loaders.dyer2017.SpectralDataHeader_AMPAS.\
document_creation_date
    -   :attr:`colour_datasets.loaders.dyer2017.SpectralDataHeader_AMPAS.\
comments
    -   :attr:`colour_datasets.loaders.dyer2017.SpectralDataHeader_AMPAS.\
license

    Methods
    -------
    -   :meth:`colour_datasets.loaders.dyer2017.SpectralDataHeader_AMPAS.\
__init__`
    """

    def __init__(
        self,
        schema_version: Optional[str] = None,
        catalog_number: Optional[str] = None,
        description: Optional[str] = None,
        document_creator: Optional[str] = None,
        unique_identifier: Optional[str] = None,
        measurement_equipment: Optional[str] = None,
        laboratory: Optional[str] = None,
        document_creation_date: Optional[str] = None,
        comments: Optional[str] = None,
        license: Optional[str] = None,
        **kwargs: Any,
    ):

        self._schema_version: Optional[str] = None
        self.schema_version = schema_version
        self._catalog_number: Optional[str] = None
        self.catalog_number = catalog_number
        self._description: Optional[str] = None
        self.description = description
        self._document_creator: Optional[str] = None
        self.document_creator = document_creator
        self._unique_identifier: Optional[str] = None
        self.unique_identifier = unique_identifier
        self._measurement_equipment: Optional[str] = None
        self.measurement_equipment = measurement_equipment
        self._laboratory: Optional[str] = None
        self.laboratory = laboratory
        self._document_creation_date: Optional[str] = None
        self.document_creation_date = document_creation_date
        self._comments: Optional[str] = None
        self.comments = comments
        self._license: Optional[str] = None
        self.license = license

        # TODO: Re-instate "manufacturer", "model", "illuminant" and "type"
        # attributes according to outcome of
        # https://github.com/ampas/rawtoaces/issues/114. Those attributes are
        # currently stored in "self._kwargs".
        self._kwargs: Any = kwargs

    @property
    def schema_version(self) -> Optional[str]:
        """
        Getter and setter property for the schema version.

        Parameters
        ----------
        value
            Value to set the schema version with.

        Returns
        -------
        :py:data:`None` or :class:`str`
            Schema version.
        """

        return self._schema_version

    @schema_version.setter
    def schema_version(self, value: Optional[str]):
        """Setter for the **self.schema_version** property."""

        if value is not None:
            attest(
                is_string(value),
                f'"schema_version" property: "{value}" type is not "str"!',
            )

        self._schema_version = value

    @property
    def catalog_number(self) -> Optional[str]:
        """
        Getter and setter property for the catalog number.

        Parameters
        ----------
        value
            Value to set the catalog number with.

        Returns
        -------
        :py:data:`None` or :class:`str`
            Catalog number.
        """

        return self._catalog_number

    @catalog_number.setter
    def catalog_number(self, value: Optional[str]):
        """Setter for the **self.catalog_number** property."""

        if value is not None:
            attest(
                is_string(value),
                f'"catalog_number" property: "{value}" type is not "str"!',
            )

        self._catalog_number = value

    @property
    def description(self) -> Optional[str]:
        """
        Getter and setter property for the description.

        Parameters
        ----------
        value
            Value to set the description with.

        Returns
        -------
        :py:data:`None` or :class:`str`
            Description.
        """

        return self._description

    @description.setter
    def description(self, value: Optional[str]):
        """Setter for the **self.description** property."""

        if value is not None:
            attest(
                is_string(value),
                f'"description" property: "{value}" type is not "str"!',
            )

        self._description = value

    @property
    def document_creator(self) -> Optional[str]:
        """
        Getter and setter property for the document creator.

        Parameters
        ----------
        value
            Value to set the document creator with.

        Returns
        -------
        :py:data:`None` or :class:`str`
            Document creator.
        """

        return self._document_creator

    @document_creator.setter
    def document_creator(self, value: Optional[str]):
        """Setter for the **self.document_creator** property."""

        if value is not None:
            attest(
                is_string(value),
                f'"document_creator" property: "{value}" type is not "str"!',
            )

        self._document_creator = value

    @property
    def unique_identifier(self) -> Optional[str]:
        """
        Getter and setter property for the unique identifier.

        Parameters
        ----------
        value
            Value to set the unique identifier with.

        Returns
        -------
        :py:data:`None` or :class:`str`
            Unique identifier.
        """

        return self._unique_identifier

    @unique_identifier.setter
    def unique_identifier(self, value: Optional[str]):
        """Setter for the **self.unique_identifier** property."""

        if value is not None:
            attest(
                is_string(value),
                f'"unique_identifier" property: "{value}" type is not "str"!',
            )

        self._unique_identifier = value

    @property
    def measurement_equipment(self) -> Optional[str]:
        """
        Getter and setter property for the measurement equipment.

        Parameters
        ----------
        value
            Value to set the measurement equipment with.

        Returns
        -------
        :py:data:`None` or :class:`str`
            Measurement equipment.
        """

        return self._measurement_equipment

    @measurement_equipment.setter
    def measurement_equipment(self, value: Optional[str]):
        """Setter for the **self.measurement_equipment** property."""

        if value is not None:
            attest(
                is_string(value),
                f'"measurement_equipment" property: "{value}" type is not '
                f'"str"!',
            )

        self._measurement_equipment = value

    @property
    def laboratory(self) -> Optional[str]:
        """
        Getter and setter property for the laboratory.

        Parameters
        ----------
        value
            Value to set the laboratory with.

        Returns
        -------
        :py:data:`None` or :class:`str`
            Laboratory.
        """

        return self._laboratory

    @laboratory.setter
    def laboratory(self, value: Optional[str]):
        """Setter for the **self.measurement_equipment** property."""

        if value is not None:
            attest(
                is_string(value),
                f'"laboratory" property: "{value}" type is not "str"!',
            )

        self._laboratory = value

    @property
    def document_creation_date(self) -> Optional[str]:
        """
        Getter and setter property for the document creation date.

        Parameters
        ----------
        value
            Value to set the document creation date with.

        Returns
        -------
        :py:data:`None` or :class:`str`
            Document creation date.
        """

        return self._document_creation_date

    @document_creation_date.setter
    def document_creation_date(self, value: Optional[str]):
        """Setter for the **self.document_creation_date** property."""

        if value is not None:
            attest(
                is_string(value),
                f'"document_creation_date" property: "{value}" type is not '
                f'"str"!',
            )

        self._document_creation_date = value

    @property
    def comments(self) -> Optional[str]:
        """
        Getter and setter property for the comments.

        Parameters
        ----------
        value
            Value to set the comments with.

        Returns
        -------
        :py:data:`None` or :class:`str`
            Comments.
        """

        return self._comments

    @comments.setter
    def comments(self, value: Optional[str]):
        """Setter for the **self.comments** property."""

        if value is not None:
            attest(
                is_string(value),
                f'"comments" property: "{value}" type is not "str"!',
            )

        self._comments = value

    @property
    def license(self) -> Optional[str]:
        """
        Getter and setter property for the license.

        Parameters
        ----------
        value
            Value to set the license with.

        Returns
        -------
        :py:data:`None` or :class:`str`
            Comments.
        """

        return self._license

    @license.setter
    def license(self, value: Optional[str]):
        """Setter for the **self.license** property."""

        if value is not None:
            attest(
                is_string(value),
                f'"license" property: "{value}" type is not "str"!',
            )

        self._license = value


class SpectralDistribution_AMPAS(SpectralDistribution):
    """
    Define an *A.M.P.A.S* spectral distribution.

    This class can read *A.M.P.A.S* spectral data JSON files.

    Parameters
    ----------
    path
        Spectral data JSON file path.
    header
        *A.M.P.A.S.* spectral distribution header.
    units
        Quantity of measurement for each element of the spectral data.
    reflection_geometry
        Spectral reflectance factors geometric conditions.
    transmission_geometry
        Spectral transmittance factors geometric conditions.
    bandwidth_FWHM
        Spectroradiometer full-width half-maximum bandwidth in nanometers.
    bandwidth_corrected
        Specifies if bandwidth correction has been applied to the measured
        data.

    Notes
    -----
    *Reflection Geometry*

    -   di:8: Diffuse / eight-degree, specular component included.
    -   de:8: Diffuse / eight-degree, specular component excluded.
    -   8:di: Eight-degree / diffuse, specular component included.
    -   8:de: Eight-degree / diffuse, specular component excluded.
    -   d:d: Diffuse / diffuse.
    -   d:0: Alternative diffuse.
    -   45a:0: Forty-five degree annular / normal.
    -   45c:0: Forty-five degree circumferential / normal.
    -   0:45a: Normal / forty-five degree annular.
    -   45x:0: Forty-five degree directional / normal.
    -   0:45x: Normal / forty-five degree directional.
    -   other: User-specified in comments.

    *Transmission Geometry*

    -   0:0: Normal / normal.
    -   di:0: Diffuse / normal, regular component included.
    -   de:0: Diffuse / normal, regular component excluded.
    -   0:di: Normal / diffuse, regular component included.
    -   0:de: Normal / diffuse, regular component excluded.
    -   d:d: Diffuse / diffuse.
    -   other: User-specified in comments.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.dyer2017.SpectralDistribution_AMPAS.path`
    -   :attr:`colour_datasets.loaders.dyer2017.SpectralDistribution_AMPAS.header`
    -   :attr:`colour_datasets.loaders.dyer2017.SpectralDistribution_AMPAS.units`
    -   :attr:`colour_datasets.loaders.dyer2017.SpectralDistribution_AMPAS.\
reflection_geometry`
    -   :attr:`colour_datasets.loaders.dyer2017.SpectralDistribution_AMPAS.\
transmission_geometry`
    -   :attr:`colour_datasets.loaders.dyer2017.SpectralDistribution_AMPAS.\
bandwidth_FWHM`
    -   :attr:`colour_datasets.loaders.dyer2017.SpectralDistribution_AMPAS.\
bandwidth_corrected`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.dyer2017.SpectralDistribution_AMPAS.\
__init__`
    -   :meth:`colour_datasets.loaders.dyer2017.SpectralDistribution_AMPAS.read`
    """

    def __init__(
        self,
        path: Optional[str] = None,
        header: Optional[SpectralDataHeader_AMPAS] = None,
        units: Optional[
            Literal[
                "absorptance",
                "exitance",
                "flux",
                "intensity",
                "irradiance",
                "radiance",
                "reflectance",
                "relative",
                "transmittance",
                "R-Factor",
                "T-Factor",
                "other",
            ]
        ] = None,
        reflection_geometry: Optional[
            Literal[
                "di:8",
                "de:8",
                "8:di",
                "8:de",
                "d:d",
                "d:0",
                "45a:0",
                "45c:0",
                "0:45a",
                "45x:0",
                "0:45x",
                "other",
            ]
        ] = None,
        transmission_geometry: Optional[
            Literal["0:0", "di:0", "de:0", "0:di", "0:de", "d:d", "other"]
        ] = None,
        bandwidth_FWHM: Optional[Floating] = None,
        bandwidth_corrected: Optional[Boolean] = None,
    ):
        super().__init__()

        self._path: Optional[str] = None
        self.path = path
        self._header: SpectralDataHeader_AMPAS = SpectralDataHeader_AMPAS()
        self.header = optional(header, self._header)
        self._units: Optional[
            Literal[
                "absorptance",
                "exitance",
                "flux",
                "intensity",
                "irradiance",
                "radiance",
                "reflectance",
                "relative",
                "transmittance",
                "R-Factor",
                "T-Factor",
                "other",
            ]
        ] = None
        self.units = units
        self._reflection_geometry: Optional[
            Literal[
                "di:8",
                "de:8",
                "8:di",
                "8:de",
                "d:d",
                "d:0",
                "45a:0",
                "45c:0",
                "0:45a",
                "45x:0",
                "0:45x",
                "other",
            ]
        ] = None
        self.reflection_geometry = reflection_geometry
        self._transmission_geometry: Optional[
            Literal["0:0", "di:0", "de:0", "0:di", "0:de", "d:d", "other"]
        ] = None
        self.transmission_geometry = transmission_geometry
        self._bandwidth_FWHM: Optional[Floating] = None
        self.bandwidth_FWHM = bandwidth_FWHM
        self._bandwidth_corrected: Optional[Boolean] = None
        self.bandwidth_corrected = bandwidth_corrected

    @property
    def path(self) -> Optional[str]:
        """
        Getter and setter property for the path.

        Parameters
        ----------
        value
            Value to set the path with.

        Returns
        -------
        :py:data:`None` or :class:`str`
            Path.
        """

        return self._path

    @path.setter
    def path(self, value: Optional[str]):
        """Setter for the **self.path** property."""

        if value is not None:
            attest(
                is_string(value),
                f'"path" property: "{value}" type is not "str"!',
            )
        self._path = value

    @property
    def header(self) -> SpectralDataHeader_AMPAS:
        """
        Getter and setter property for the header.

        Parameters
        ----------
        value
            Value to set the header with.

        Returns
        -------
        :class:`colour_datasets.loaders.dyer2017.SpectralDataHeader_AMPAS`
            Header.
        """

        return self._header

    @header.setter
    def header(self, value: SpectralDataHeader_AMPAS):
        """Setter for the **self.header** property."""

        attest(
            isinstance(value, SpectralDataHeader_AMPAS),
            f'"header" property: "{value}" type is not "SpectralDataHeader_AMPAS"!',
        )
        self._header = value

    @property
    def units(
        self,
    ) -> Optional[
        Literal[
            "absorptance",
            "exitance",
            "flux",
            "intensity",
            "irradiance",
            "radiance",
            "reflectance",
            "relative",
            "transmittance",
            "R-Factor",
            "T-Factor",
            "other",
        ]
    ]:
        """
        Getter and setter property for the units.

        Parameters
        ----------
        value
            Value to set the units with.

        Returns
        -------
        :py:data:`None` or :class:`str`
            Spectral units.
        """

        return self._units

    @units.setter
    def units(
        self,
        value: Optional[
            Literal[
                "absorptance",
                "exitance",
                "flux",
                "intensity",
                "irradiance",
                "radiance",
                "reflectance",
                "relative",
                "transmittance",
                "R-Factor",
                "T-Factor",
                "other",
            ]
        ],
    ):
        """Setter for the **self.units** property."""

        if value is not None:
            attest(
                is_string(value),
                f'"units" property: "{value}" type is not "str"!',
            )

        self._units = value

    @property
    def reflection_geometry(
        self,
    ) -> Optional[
        Literal[
            "di:8",
            "de:8",
            "8:di",
            "8:de",
            "d:d",
            "d:0",
            "45a:0",
            "45c:0",
            "0:45a",
            "45x:0",
            "0:45x",
            "other",
        ]
    ]:
        """
        Getter and setter property for the reflection geometry.

        Parameters
        ----------
        value
            Value to set the reflection geometry with.

        Returns
        -------
        :py:data:`None` or :class:`str`
            Reflection geometry.
        """

        return self._reflection_geometry

    @reflection_geometry.setter
    def reflection_geometry(
        self,
        value: Optional[
            Literal[
                "di:8",
                "de:8",
                "8:di",
                "8:de",
                "d:d",
                "d:0",
                "45a:0",
                "45c:0",
                "0:45a",
                "45x:0",
                "0:45x",
                "other",
            ]
        ],
    ):
        """Setter for the **self.reflection_geometry** property."""

        if value is not None:
            attest(
                is_string(value),
                f'"reflection_geometry" property: "{value}" type is not "str"!',
            )

        self._reflection_geometry = value

    @property
    def transmission_geometry(
        self,
    ) -> Optional[
        Literal["0:0", "di:0", "de:0", "0:di", "0:de", "d:d", "other"]
    ]:
        """
        Getter and setter property for the transmission geometry.

        Parameters
        ----------
        value
            Value to set the transmission geometry with.

        Returns
        -------
        :py:data:`None` or :class:`str`
            Transmission geometry.
        """

        return self._transmission_geometry

    @transmission_geometry.setter
    def transmission_geometry(
        self,
        value: Optional[
            Literal["0:0", "di:0", "de:0", "0:di", "0:de", "d:d", "other"]
        ],
    ):
        """Setter for the **self.transmission_geometry** property."""

        if value is not None:
            assert is_string(value), (
                f'"transmission_geometry" property: "{value}" type is not "str"!',
            )

        self._transmission_geometry = value

    @property
    def bandwidth_FWHM(self) -> Optional[Floating]:
        """
        Getter and setter property for the full-width half-maximum bandwidth.

        Parameters
        ----------
        value
            Value to set the full-width half-maximum bandwidth with.

        Returns
        -------
        :py:data:`None` or :class:`numpy.floating`
            Full-width half-maximum bandwidth.
        """

        return self._bandwidth_FWHM

    @bandwidth_FWHM.setter
    def bandwidth_FWHM(self, value: Optional[Floating]):
        """Setter for the **self.bandwidth_FWHM** property."""

        if value is not None:
            attest(
                is_numeric(value),
                f'"bandwidth_FWHM" property: "{value}" is not a "number"!',
            )

        self._bandwidth_FWHM = value

    @property
    def bandwidth_corrected(self) -> Optional[Boolean]:
        """
        Getter and setter property for whether bandwidth correction has been
        applied to the measured data.

        Parameters
        ----------
        value
            Whether bandwidth correction has been applied to the measured data.

        Returns
        -------
        :py:data:`None` or :class:`bool`
            Whether bandwidth correction has been applied to the measured data.
        """

        return self._bandwidth_corrected

    @bandwidth_corrected.setter
    def bandwidth_corrected(self, value: Optional[Boolean]):
        """Setter for the **self.bandwidth_corrected** property."""

        if value is not None:
            attest(
                isinstance(value, bool),
                f'"bandwidth_corrected" property: "{value}" type is not "bool"!',
            )

        self._bandwidth_corrected = value

    def read(self) -> SpectralDistribution:
        """
        Read and parses the spectral data JSON file path.

        Returns
        -------
        :class:`colour.SpectralDistribution`

        Raises
        ------
        ValueError
            If the spectral distribution path is undefined.
        """

        if self._path is not None:
            with open(self._path) as json_file:
                content = json.load(json_file)

            self._header = SpectralDataHeader_AMPAS(**content["header"])
            for attribute in (
                "units",
                "reflection_geometry",
                "transmission_geometry",
                "bandwidth_FWHM",
                "bandwidth_corrected",
            ):
                setattr(
                    self, f"_{attribute}", content["spectral_data"][attribute]
                )

            data = content["spectral_data"]["data"]["main"]

            self.domain, self.range = Signal.signal_unpack_data(
                {k: v[0] for k, v in data.items()}
            )

            # TODO: Re-instate "manufacturer", "model", "illuminant" and "type"
            # attributes according to outcome of
            # https://github.com/ampas/rawtoaces/issues/114.
            if (
                "manufacturer" in self._header._kwargs
                and "model" in self._header._kwargs
            ):
                self.name = (
                    f"{self._header._kwargs['manufacturer']} "
                    f"{self._header._kwargs['model']}"
                )
            elif "illuminant" in self._header._kwargs:
                self.name = self._header._kwargs["illuminant"]
            elif "type" in self._header._kwargs:
                self.name = self._header._kwargs["type"]

            return self
        else:
            raise ValueError("The spectral distribution path is undefined!")


class MultiSpectralDistributions_AMPAS(MultiSpectralDistributions):
    """
    Define the *A.M.P.A.S* multi-spectral distributions.

    This class can read *A.M.P.A.S* spectral data JSON files.

    Parameters
    ----------
    path
        Spectral data JSON file path.
    header
        *A.M.P.A.S.* spectral distribution header.
    units
        Quantity of measurement for each element of the spectral data.
    reflection_geometry
        Spectral reflectance factors geometric conditions.
    transmission_geometry
        Spectral transmittance factors geometric conditions.
    bandwidth_FWHM
        Spectroradiometer full-width half-maximum bandwidth in nanometers.
    bandwidth_corrected
        Specifies if bandwidth correction has been applied to the measured
        data.

    Notes
    -----
    *Reflection Geometry*

    -   di:8: Diffuse / eight-degree, specular component included.
    -   de:8: Diffuse / eight-degree, specular component excluded.
    -   8:di: Eight-degree / diffuse, specular component included.
    -   8:de: Eight-degree / diffuse, specular component excluded.
    -   d:d: Diffuse / diffuse.
    -   d:0: Alternative diffuse.
    -   45a:0: Forty-five degree annular / normal.
    -   45c:0: Forty-five degree circumferential / normal.
    -   0:45a: Normal / forty-five degree annular.
    -   45x:0: Forty-five degree directional / normal.
    -   0:45x: Normal / forty-five degree directional.
    -   other: User-specified in comments.

    *Transmission Geometry*

    -   0:0: Normal / normal.
    -   di:0: Diffuse / normal, regular component included.
    -   de:0: Diffuse / normal, regular component excluded.
    -   0:di: Normal / diffuse, regular component included.
    -   0:de: Normal / diffuse, regular component excluded.
    -   d:d: Diffuse / diffuse.
    -   other: User-specified in comments.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.dyer2017.MultiSpectralDistributions_AMPAS.path`
    -   :attr:`colour_datasets.loaders.dyer2017.MultiSpectralDistributions_AMPAS.header`
    -   :attr:`colour_datasets.loaders.dyer2017.MultiSpectralDistributions_AMPAS.units`
    -   :attr:`colour_datasets.loaders.dyer2017.MultiSpectralDistributions_AMPAS.\
reflection_geometry`
    -   :attr:`colour_datasets.loaders.dyer2017.MultiSpectralDistributions_AMPAS.\
transmission_geometry`
    -   :attr:`colour_datasets.loaders.dyer2017.MultiSpectralDistributions_AMPAS.\
bandwidth_FWHM`
    -   :attr:`colour_datasets.loaders.dyer2017.MultiSpectralDistributions_AMPAS.\
bandwidth_corrected`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.dyer2017.MultiSpectralDistributions_AMPAS.\
__init__`
    -   :meth:`colour_datasets.loaders.dyer2017.MultiSpectralDistributions_AMPAS.read`
    """

    def __init__(
        self,
        path: Optional[str] = None,
        header: Optional[SpectralDataHeader_AMPAS] = None,
        units: Optional[
            Literal[
                "absorptance",
                "exitance",
                "flux",
                "intensity",
                "irradiance",
                "radiance",
                "reflectance",
                "relative",
                "transmittance",
                "R-Factor",
                "T-Factor",
                "other",
            ]
        ] = None,
        reflection_geometry: Optional[
            Literal[
                "di:8",
                "de:8",
                "8:di",
                "8:de",
                "d:d",
                "d:0",
                "45a:0",
                "45c:0",
                "0:45a",
                "45x:0",
                "0:45x",
                "other",
            ]
        ] = None,
        transmission_geometry: Optional[
            Literal["0:0", "di:0", "de:0", "0:di", "0:de", "d:d", "other"]
        ] = None,
        bandwidth_FWHM: Optional[Floating] = None,
        bandwidth_corrected: Optional[Boolean] = None,
    ):
        super().__init__()

        self._path: Optional[str] = None
        self.path = path
        self._header: SpectralDataHeader_AMPAS = SpectralDataHeader_AMPAS()
        self.header = optional(header, self._header)
        self._units: Optional[
            Literal[
                "absorptance",
                "exitance",
                "flux",
                "intensity",
                "irradiance",
                "radiance",
                "reflectance",
                "relative",
                "transmittance",
                "R-Factor",
                "T-Factor",
                "other",
            ]
        ] = None
        self.units = units
        self._reflection_geometry: Optional[
            Literal[
                "di:8",
                "de:8",
                "8:di",
                "8:de",
                "d:d",
                "d:0",
                "45a:0",
                "45c:0",
                "0:45a",
                "45x:0",
                "0:45x",
                "other",
            ]
        ] = None
        self.reflection_geometry = reflection_geometry
        self._transmission_geometry: Optional[
            Literal["0:0", "di:0", "de:0", "0:di", "0:de", "d:d", "other"]
        ] = None
        self.transmission_geometry = transmission_geometry
        self._bandwidth_FWHM: Optional[Floating] = None
        self.bandwidth_FWHM = bandwidth_FWHM
        self._bandwidth_corrected: Optional[Boolean] = None
        self.bandwidth_corrected = bandwidth_corrected

    @property
    def path(self) -> Optional[str]:
        """
        Getter and setter property for the path.

        Parameters
        ----------
        value
            Value to set the path with.

        Returns
        -------
        :py:data:`None` or :class:`str`
            Path.
        """

        return self._path

    @path.setter
    def path(self, value: Optional[str]):
        """Setter for the **self.path** property."""

        if value is not None:
            attest(
                is_string(value),
                f'"path" property: "{value}" type is not "str"!',
            )
        self._path = value

    @property
    def header(self) -> SpectralDataHeader_AMPAS:
        """
        Getter and setter property for the header.

        Parameters
        ----------
        value
            Value to set the header with.

        Returns
        -------
        :class:`colour_datasets.loaders.dyer2017.SpectralDataHeader_AMPAS`
            Header.
        """

        return self._header

    @header.setter
    def header(self, value: SpectralDataHeader_AMPAS):
        """Setter for the **self.header** property."""

        attest(
            isinstance(value, SpectralDataHeader_AMPAS),
            f'"header" property: "{value}" type is not "SpectralDataHeader_AMPAS"!',
        )
        self._header = value

    @property
    def units(
        self,
    ) -> Optional[
        Literal[
            "absorptance",
            "exitance",
            "flux",
            "intensity",
            "irradiance",
            "radiance",
            "reflectance",
            "relative",
            "transmittance",
            "R-Factor",
            "T-Factor",
            "other",
        ]
    ]:
        """
        Getter and setter property for the units.

        Parameters
        ----------
        value
            Value to set the units with.

        Returns
        -------
        :py:data:`None` or :class:`str`
            Spectral units.
        """

        return self._units

    @units.setter
    def units(
        self,
        value: Optional[
            Literal[
                "absorptance",
                "exitance",
                "flux",
                "intensity",
                "irradiance",
                "radiance",
                "reflectance",
                "relative",
                "transmittance",
                "R-Factor",
                "T-Factor",
                "other",
            ]
        ],
    ):
        """Setter for the **self.units** property."""

        if value is not None:
            attest(
                is_string(value),
                f'"units" property: "{value}" type is not "str"!',
            )

        self._units = value

    @property
    def reflection_geometry(
        self,
    ) -> Optional[
        Literal[
            "di:8",
            "de:8",
            "8:di",
            "8:de",
            "d:d",
            "d:0",
            "45a:0",
            "45c:0",
            "0:45a",
            "45x:0",
            "0:45x",
            "other",
        ]
    ]:
        """
        Getter and setter property for the reflection geometry.

        Parameters
        ----------
        value
            Value to set the reflection geometry with.

        Returns
        -------
        :py:data:`None` or :class:`str`
            Reflection geometry.
        """

        return self._reflection_geometry

    @reflection_geometry.setter
    def reflection_geometry(
        self,
        value: Optional[
            Literal[
                "di:8",
                "de:8",
                "8:di",
                "8:de",
                "d:d",
                "d:0",
                "45a:0",
                "45c:0",
                "0:45a",
                "45x:0",
                "0:45x",
                "other",
            ]
        ],
    ):
        """Setter for the **self.reflection_geometry** property."""

        if value is not None:
            attest(
                is_string(value),
                f'"reflection_geometry" property: "{value}" type is not "str"!',
            )

        self._reflection_geometry = value

    @property
    def transmission_geometry(
        self,
    ) -> Optional[
        Literal["0:0", "di:0", "de:0", "0:di", "0:de", "d:d", "other"]
    ]:
        """
        Getter and setter property for the transmission geometry.

        Parameters
        ----------
        value
            Value to set the transmission geometry with.

        Returns
        -------
        :py:data:`None` or :class:`str`
            Transmission geometry.
        """

        return self._transmission_geometry

    @transmission_geometry.setter
    def transmission_geometry(
        self,
        value: Optional[
            Literal["0:0", "di:0", "de:0", "0:di", "0:de", "d:d", "other"]
        ],
    ):
        """Setter for the **self.transmission_geometry** property."""

        if value is not None:
            assert is_string(value), (
                f'"transmission_geometry" property: "{value}" type is not "str"!',
            )

        self._transmission_geometry = value

    @property
    def bandwidth_FWHM(self) -> Optional[Floating]:
        """
        Getter and setter property for the full-width half-maximum bandwidth.

        Parameters
        ----------
        value
            Value to set the full-width half-maximum bandwidth with.

        Returns
        -------
        :py:data:`None` or :class:`numpy.floating`
            Full-width half-maximum bandwidth.
        """

        return self._bandwidth_FWHM

    @bandwidth_FWHM.setter
    def bandwidth_FWHM(self, value: Optional[Floating]):
        """Setter for the **self.bandwidth_FWHM** property."""

        if value is not None:
            attest(
                is_numeric(value),
                f'"bandwidth_FWHM" property: "{value}" is not a "number"!',
            )

        self._bandwidth_FWHM = value

    @property
    def bandwidth_corrected(self) -> Optional[Boolean]:
        """
        Getter and setter property for whether bandwidth correction has been
        applied to the measured data.

        Parameters
        ----------
        value
            Whether bandwidth correction has been applied to the measured data.

        Returns
        -------
        :py:data:`None` or :class:`bool`
            Whether bandwidth correction has been applied to the measured data.
        """

        return self._bandwidth_corrected

    @bandwidth_corrected.setter
    def bandwidth_corrected(self, value: Optional[Boolean]):
        """Setter for the **self.bandwidth_corrected** property."""

        if value is not None:
            attest(
                isinstance(value, bool),
                f'"bandwidth_corrected" property: "{value}" type is not "bool"!',
            )

        self._bandwidth_corrected = value

    def read(self) -> MultiSpectralDistributions:
        """
        Read and parses the spectral data JSON file path.

        Returns
        -------
        :class:`colour.MultiSpectralDistributions`

        Raises
        ------
        ValueError
            If the multi-spectral distributions path is undefined.
        """

        if self._path is not None:
            with open(self._path) as json_file:
                content = json.load(json_file)

            self._header = SpectralDataHeader_AMPAS(**content["header"])
            for attribute in (
                "units",
                "reflection_geometry",
                "transmission_geometry",
                "bandwidth_FWHM",
                "bandwidth_corrected",
            ):
                setattr(
                    self, f"_{attribute}", content["spectral_data"][attribute]
                )

            index = content["spectral_data"]["index"]["main"]
            data = content["spectral_data"]["data"]["main"]

            self.signals = MultiSignals.multi_signals_unpack_data(
                data, labels=index
            )

            # TODO: Re-instate "manufacturer", "model", "illuminant" and "type"
            # attributes according to outcome of
            # https://github.com/ampas/rawtoaces/issues/114.
            if (
                "manufacturer" in self._header._kwargs
                and "model" in self._header._kwargs
            ):
                self.name = (
                    f"{self._header._kwargs['manufacturer']} "
                    f"{self._header._kwargs['model']}"
                )
            elif "illuminant" in self._header._kwargs:
                self.name = self._header._kwargs["illuminant"]
            elif "type" in self._header._kwargs:
                self.name = self._header._kwargs["type"]

            return self
        else:
            raise ValueError(
                "The multi=spectral distributions path is undefined!"
            )


class DatasetLoader_Dyer2017(AbstractDatasetLoader):
    """
    Define the *Dyer et al. (2017)* *RAW to ACES Utility Data* dataset
    loader.

    Attributes
    ----------
    -   :attr:`colour_datasets.loaders.DatasetLoader_Dyer2017.ID`

    Methods
    -------
    -   :meth:`colour_datasets.loaders.DatasetLoader_Dyer2017.__init__`
    -   :meth:`colour_datasets.loaders.DatasetLoader_Dyer2017.load`

    References
    ----------
    :cite:`Dyer2017`
    """

    ID: str = "3372171"
    """Dataset record id, i.e. the *Zenodo* record number."""

    def __init__(self):
        super().__init__(datasets()[DatasetLoader_Dyer2017.ID])

    def load(
        self,
    ) -> Dict[
        str,
        Dict[
            str,
            Union[
                SpectralDistribution_AMPAS, MultiSpectralDistributions_AMPAS
            ],
        ],
    ]:
        """
        Sync, parse, convert and return the *Dyer et al. (2017)*
        *RAW to ACES Utility Data* dataset content.

        Returns
        -------
        :class:`dict`
            *Dyer et al. (2017)* *RAW to ACES Utility Data* dataset content.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = DatasetLoader_Dyer2017()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.content.keys())
        4
        """

        super().sync()

        self._content = dict()

        for directory in ("camera", "cmf", "illuminant", "training"):
            self._content[directory] = dict()
            factory = cast(
                Union[
                    Type[SpectralDistribution_AMPAS],
                    Type[MultiSpectralDistributions_AMPAS],
                ],
                SpectralDistribution_AMPAS
                if directory == "illuminant"
                else MultiSpectralDistributions_AMPAS,
            )
            glob_pattern = os.path.join(
                self.record.repository, "dataset", "data", directory, "*.json"
            )
            for path in glob.glob(glob_pattern):
                msds = factory(path).read()
                self._content[directory][msds.name] = msds

        return self._content


_DATASET_LOADER_DYER2017: Optional[DatasetLoader_Dyer2017] = None
"""
Singleton instance of the *Dyer et al. (2017)* *RAW to ACES Utility Data*
dataset loader.
"""


def build_Dyer2017(load: Boolean = True) -> DatasetLoader_Dyer2017:
    """
    Singleton factory that builds the *Dyer et al. (2017)*
    *RAW to ACES Utility Data* dataset loader.

    Parameters
    ----------
    load
        Whether to load the dataset upon instantiation.

    Returns
    -------
     :class:`colour_datasets.loaders.DatasetLoader_Dyer2017`
        Singleton instance of the *Dyer et al. (2017)*
        *RAW to ACES Utility Data* dataset loader.

    References
    ----------
    :cite:`Dyer2017`
    """

    global _DATASET_LOADER_DYER2017

    if _DATASET_LOADER_DYER2017 is None:
        _DATASET_LOADER_DYER2017 = DatasetLoader_Dyer2017()
        if load:
            _DATASET_LOADER_DYER2017.load()

    return _DATASET_LOADER_DYER2017
