# -*- coding: utf-8 -*-
"""
RAW to ACES Utility Data - Dyer et al. (2017)
=============================================

Defines the objects implementing support for
*Dyer, Forsythe, Irons, Mansencal and Zhu (2017)*
*RAW to ACES Utility Data* dataset loading:

-   :class:`colour_datasets.loaders.Dyer2017DatasetLoader`
-   :func:`colour_datasets.loaders.build_Dyer2017`

References
----------
-   :cite:`Dyer2017` : Dyer, S., Forsythe, A., Irons, J., Mansencal, T., & Zhu,
    M. (2017). RAW to ACES Utility Data.
"""

from __future__ import division, unicode_literals

import json
import glob
import os
from collections import OrderedDict

from colour import MultiSpectralDistributions, SpectralDistribution
from colour.continuous import MultiSignals, Signal
from colour.utilities import is_numeric, is_string

from colour_datasets.records import datasets
from colour_datasets.loaders import AbstractDatasetLoader

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = [
    'AMPAS_SpectralDataHeader', 'AMPAS_SpectralDataMixin',
    'SpectralDistribution_AMPAS', 'Dyer2017DatasetLoader', 'build_Dyer2017'
]


class AMPAS_SpectralDataHeader(object):
    """
    Defines the header object for an *A.M.P.A.S* spectral data.

    Parameters
    ----------
    schema_version : unicode, optional
        Version of the *A.M.P.A.S* spectral data schema.
    catalog_number : unicode, optional
        Manufacturer's product catalog number.
    description : unicode, optional
        Description of the spectral data in the spectral data JSON file.
    document_creator : unicode, optional
        Creator of the spectral data JSON file, which may be a
        test lab, a research group, a standard body, a company or an
        individual.
    unique_identifier : unicode, optional
        Description of the equipment used to measure the spectral data.
    measurement_equipment : unicode, optional
        Description of the equipment used to measure the spectral data.
    laboratory : unicode, optional
        Testing laboratory name that performed the spectral data measurements.
    document_creation_date : unicode, optional
        Spectral data JSON file creation date using the
        *JSON DateTime Data Type*, *YYYY-MM-DDThh:mm:ss*.
    comments : unicode, optional
        Additional information relating to the tested and reported data.
    license : unicode, optional
        License under which the data is distributed.

    Attributes
    ----------
    schema_version
    catalog_number
    description
    document_creator
    unique_identifier
    measurement_equipment
    laboratory
    document_creation_date
    comments
    license
    """

    def __init__(self,
                 schema_version=None,
                 catalog_number=None,
                 description=None,
                 document_creator=None,
                 unique_identifier=None,
                 measurement_equipment=None,
                 laboratory=None,
                 document_creation_date=None,
                 comments=None,
                 license=None,
                 **kwargs):

        self._schema_version = None
        self.schema_version = schema_version
        self._catalog_number = None
        self.catalog_number = catalog_number
        self._description = None
        self.description = description
        self._document_creator = None
        self.document_creator = document_creator
        self._unique_identifier = None
        self.unique_identifier = unique_identifier
        self._measurement_equipment = None
        self.measurement_equipment = measurement_equipment
        self._laboratory = None
        self.laboratory = laboratory
        self._document_creation_date = None
        self.document_creation_date = document_creation_date
        self._comments = None
        self.comments = comments
        self._license = None
        self.license = license

        # TODO: Re-instate "manufacturer", "model", "illuminant" and "type"
        # attributes according to outcome of
        # https://github.com/ampas/rawtoaces/issues/114. Those attributes are
        # currently stored in "self._kwargs".
        self._kwargs = kwargs

    @property
    def schema_version(self):
        """
        Getter and setter property for the schema version.

        Parameters
        ----------
        value : unicode
            Value to set the schema version with.

        Returns
        -------
        unicode
            Schema version.
        """

        return self._schema_version

    @schema_version.setter
    def schema_version(self, value):
        """
        Setter for the **self.schema_version** property.
        """

        if value is not None:
            assert is_string(value), (
                '"{0}" attribute: "{1}" is not a "string" like object!'.format(
                    'schema_version', value))
        self._schema_version = value

    @property
    def catalog_number(self):
        """
        Getter and setter property for the catalog number.

        Parameters
        ----------
        value : unicode
            Value to set the catalog number with.

        Returns
        -------
        unicode
            Catalog number.
        """

        return self._catalog_number

    @catalog_number.setter
    def catalog_number(self, value):
        """
        Setter for the **self.catalog_number** property.
        """

        if value is not None:
            assert is_string(value), (
                '"{0}" attribute: "{1}" is not a "string" like object!'.format(
                    'catalog_number', value))
        self._catalog_number = value

    @property
    def description(self):
        """
        Getter and setter property for the description.

        Parameters
        ----------
        value : unicode
            Value to set the description with.

        Returns
        -------
        unicode
            Description.
        """

        return self._description

    @description.setter
    def description(self, value):
        """
        Setter for the **self.description** property.
        """

        if value is not None:
            assert is_string(value), (
                '"{0}" attribute: "{1}" is not a "string" like object!'.format(
                    'description', value))
        self._description = value

    @property
    def document_creator(self):
        """
        Getter and setter property for the document creator.

        Parameters
        ----------
        value : unicode
            Value to set the document creator with.

        Returns
        -------
        unicode
            Document creator.
        """

        return self._document_creator

    @document_creator.setter
    def document_creator(self, value):
        """
        Setter for the **self.document_creator** property.
        """

        if value is not None:
            assert is_string(value), (
                '"{0}" attribute: "{1}" is not a "string" like object!'.format(
                    'document_creator', value))
        self._document_creator = value

    @property
    def unique_identifier(self):
        """
        Getter and setter property for the unique identifier.

        Parameters
        ----------
        value : unicode
            Value to set the unique identifier with.

        Returns
        -------
        unicode
            Unique identifier.
        """

        return self._unique_identifier

    @unique_identifier.setter
    def unique_identifier(self, value):
        """
        Setter for the **self.unique_identifier** property.
        """

        if value is not None:
            assert is_string(value), (
                '"{0}" attribute: "{1}" is not a "string" like object!'.format(
                    'unique_identifier', value))
        self._unique_identifier = value

    @property
    def measurement_equipment(self):
        """
        Getter and setter property for the measurement equipment.

        Parameters
        ----------
        value : unicode
            Value to set the measurement equipment with.

        Returns
        -------
        unicode
            Measurement equipment.
        """

        return self._measurement_equipment

    @measurement_equipment.setter
    def measurement_equipment(self, value):
        """
        Setter for the **self.measurement_equipment** property.
        """

        if value is not None:
            assert is_string(value), (
                '"{0}" attribute: "{1}" is not a "string" like object!'.format(
                    'measurement_equipment', value))
        self._measurement_equipment = value

    @property
    def laboratory(self):
        """
        Getter and setter property for the laboratory.

        Parameters
        ----------
        value : unicode
            Value to set the laboratory with.

        Returns
        -------
        unicode
            Laboratory.
        """

        return self._laboratory

    @laboratory.setter
    def laboratory(self, value):
        """
        Setter for the **self.measurement_equipment** property.
        """

        if value is not None:
            assert is_string(value), (
                '"{0}" attribute: "{1}" is not a "string" like object!'.format(
                    'laboratory', value))
        self._laboratory = value

    @property
    def document_creation_date(self):
        """
        Getter and setter property for the document creation date.

        Parameters
        ----------
        value : unicode
            Value to set the document creation date with.

        Returns
        -------
        unicode
            Document creation date.
        """

        return self._document_creation_date

    @document_creation_date.setter
    def document_creation_date(self, value):
        """
        Setter for the **self.document_creation_date** property.
        """

        if value is not None:
            assert is_string(value), (
                '"{0}" attribute: "{1}" is not a "string" like object!'.format(
                    'document_creation_date', value))
        self._document_creation_date = value

    @property
    def comments(self):
        """
        Getter and setter property for the comments.

        Parameters
        ----------
        value : unicode
            Value to set the comments with.

        Returns
        -------
        unicode
            Comments.
        """

        return self._comments

    @comments.setter
    def comments(self, value):
        """
        Setter for the **self.comments** property.
        """

        if value is not None:
            assert is_string(value), (
                '"{0}" attribute: "{1}" is not a "string" like object!'.format(
                    'comments', value))
        self._comments = value

    @property
    def license(self):
        """
        Getter and setter property for the license.

        Parameters
        ----------
        value : unicode
            Value to set the license with.

        Returns
        -------
        unicode
            Comments.
        """

        return self._license

    @license.setter
    def license(self, value):
        """
        Setter for the **self.license** property.
        """

        if value is not None:
            assert is_string(value), (
                '"{0}" attribute: "{1}" is not a "string" like object!'.format(
                    'license', value))
        self._license = value


class AMPAS_SpectralDataMixin(object):
    """
    Defines a mixin for *A.M.P.A.S* spectral data.

    Parameters
    ----------
    path : unicode, optional
        Spectral data JSON file path.
    header : AMPAS_SpectralDataHeader, optional
        *A.M.P.A.S.* spectral distribution header.
    units : unicode, optional
        **{'flux', 'absorptance', 'transmittance', 'reflectance', 'intensity',
        'irradiance', 'radiance', 'exitance', 'R-Factor', 'T-Factor',
        'relative', 'other'}**,
        Quantity of measurement for each element of the spectral data.
    reflection_geometry : unicode, optional
        **{'di:8', 'de:8', '8:di', '8:de', 'd:d', 'd:0', '45a:0', '45c:0',
        '0:45a', '45x:0', '0:45x', 'other'}**,
        Spectral reflectance factors geometric conditions.
    transmission_geometry : unicode, optional
        **{'0:0', 'di:0', 'de:0', '0:di', '0:de', 'd:d', 'other'}**,
        Spectral transmittance factors geometric conditions.
    bandwidth_FWHM : numeric, optional
        Spectroradiometer full-width half-maximum bandwidth in nanometers.
    bandwidth_corrected : bool, optional
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
    path
    header
    units
    reflection_geometry
    transmission_geometry
    bandwidth_FWHM
    bandwidth_corrected

    Methods
    -------
    read

    References
    ----------
    :cite:`IESComputerCommittee2014a`
    """

    def __init__(self,
                 path=None,
                 header=None,
                 units=None,
                 reflection_geometry=None,
                 transmission_geometry=None,
                 bandwidth_FWHM=None,
                 bandwidth_corrected=None):
        super(AMPAS_SpectralDataMixin, self).__init__()

        self._path = None
        self.path = path
        self._header = None
        self.header = (header
                       if header is not None else AMPAS_SpectralDataHeader())
        self._units = None
        self.units = units
        self._reflection_geometry = None
        self.reflection_geometry = reflection_geometry
        self._transmission_geometry = None
        self.transmission_geometry = transmission_geometry
        self._bandwidth_FWHM = None
        self.bandwidth_FWHM = bandwidth_FWHM
        self._bandwidth_corrected = None
        self.bandwidth_corrected = bandwidth_corrected

    @property
    def path(self):
        """
        Getter and setter property for the path.

        Parameters
        ----------
        value : unicode
            Value to set the path with.

        Returns
        -------
        unicode
            Path.
        """

        return self._path

    @path.setter
    def path(self, value):
        """
        Setter for the **self.path** property.
        """

        if value is not None:
            assert is_string(value), (
                '"{0}" attribute: "{1}" is not a "string" like object!'.format(
                    'path', value))
        self._path = value

    @property
    def header(self):
        """
        Getter and setter property for the header.

        Parameters
        ----------
        value : AMPAS_SpectralDataHeader
            Value to set the header with.

        Returns
        -------
        AMPAS_SpectralDataHeader
            Header.
        """

        return self._header

    @header.setter
    def header(self, value):
        """
        Setter for the **self.header** property.
        """

        if value is not None:
            assert isinstance(value, AMPAS_SpectralDataHeader), (
                '"{0}" attribute: "{1}" is not a "AMPAS_SpectralDataHeader" '
                'instance!'.format('header', value))
        self._header = value

    @property
    def units(self):
        """
        Getter and setter property for the units.

        Parameters
        ----------
        value : unicode
            Value to set the units with.

        Returns
        -------
        unicode
            Spectral quantity.
        """

        return self._units

    @units.setter
    def units(self, value):
        """
        Setter for the **self.units** property.
        """

        if value is not None:
            assert is_string(value), (
                '"{0}" attribute: "{1}" is not a "string" like object!'.format(
                    'units', value))
        self._units = value

    @property
    def reflection_geometry(self):
        """
        Getter and setter property for the reflection geometry.

        Parameters
        ----------
        value : unicode
            Value to set the reflection geometry with.

        Returns
        -------
        unicode
            Reflection geometry.
        """

        return self._reflection_geometry

    @reflection_geometry.setter
    def reflection_geometry(self, value):
        """
        Setter for the **self.reflection_geometry** property.
        """

        if value is not None:
            assert is_string(value), (
                '"{0}" attribute: "{1}" is not a "string" like object!'.format(
                    'reflection_geometry', value))
        self._reflection_geometry = value

    @property
    def transmission_geometry(self):
        """
        Getter and setter property for the transmission geometry.

        Parameters
        ----------
        value : unicode
            Value to set the transmission geometry with.

        Returns
        -------
        unicode
            Transmission geometry.
        """

        return self._transmission_geometry

    @transmission_geometry.setter
    def transmission_geometry(self, value):
        """
        Setter for the **self.transmission_geometry** property.
        """

        if value is not None:
            assert is_string(value), (
                '"{0}" attribute: "{1}" is not a "string" like object!'.format(
                    'transmission_geometry', value))
        self._transmission_geometry = value

    @property
    def bandwidth_FWHM(self):
        """
        Getter and setter property for the full-width half-maximum bandwidth.

        Parameters
        ----------
        value : numeric
            Value to set the full-width half-maximum bandwidth with.

        Returns
        -------
        numeric
            Full-width half-maximum bandwidth.
        """

        return self._bandwidth_FWHM

    @bandwidth_FWHM.setter
    def bandwidth_FWHM(self, value):
        """
        Setter for the **self.bandwidth_FWHM** property.
        """

        if value is not None:
            assert is_numeric(value), (
                '"{0}" attribute: "{1}" is not a "numeric"!'.format(
                    'bandwidth_FWHM', value))

        self._bandwidth_FWHM = value

    @property
    def bandwidth_corrected(self):
        """
        Getter and setter property for whether bandwidth correction has been
        applied to the measured data.

        Parameters
        ----------
        value : bool
            Whether bandwidth correction has been applied to the measured data.

        Returns
        -------
        bool
            Whether bandwidth correction has been applied to the measured data.
        """

        return self._bandwidth_corrected

    @bandwidth_corrected.setter
    def bandwidth_corrected(self, value):
        """
        Setter for the **self.bandwidth_corrected** property.
        """

        if value is not None:
            assert isinstance(value, bool), (
                '"{0}" attribute: "{1}" is not a "bool" instance!'.format(
                    'bandwidth_corrected', value))

        self._bandwidth_corrected = value

    def read(self):
        """
        Reads and parses the spectral data JSON file path.

        Returns
        -------
        bool
            Definition success.
        """

        with open(self._path, 'r') as json_file:
            content = json.load(json_file)

        self._header = AMPAS_SpectralDataHeader(**content['header'])
        for attribute in ('units', 'reflection_geometry',
                          'transmission_geometry', 'bandwidth_FWHM',
                          'bandwidth_corrected'):
            setattr(self, '_{0}'.format(attribute),
                    content['spectral_data'][attribute])

        index = content['spectral_data']['index']['main']
        data = content['spectral_data']['data']['main']

        if len(index) == 1:
            self.domain, self.range = Signal.signal_unpack_data(
                {k: v[0]
                 for k, v in data.items()})
        else:
            self.signals = MultiSignals.multi_signals_unpack_data(
                data, labels=index)

        # TODO: Re-instate "manufacturer", "model", "illuminant" and "type"
        # attributes according to outcome of
        # https://github.com/ampas/rawtoaces/issues/114.
        if ('manufacturer' in self._header._kwargs and
                'model' in self._header._kwargs):
            self.name = '{0} {1}'.format(self._header._kwargs['manufacturer'],
                                         self._header._kwargs['model'])
        elif 'illuminant' in self._header._kwargs:
            self.name = self._header._kwargs['illuminant']
        elif 'type' in self._header._kwargs:
            self.name = self._header._kwargs['type']

        return self


class SpectralDistribution_AMPAS(AMPAS_SpectralDataMixin,
                                 SpectralDistribution):
    """
    Defines an *A.M.P.A.S* spectral distribution.

    This class can read *A.M.P.A.S* spectral data JSON files.

    Parameters
    ----------
    path : unicode, optional
        Spectral data JSON file path.
    header : AMPAS_SpectralDataHeader, optional
        *A.M.P.A.S.* spectral distribution header.
    units : unicode, optional
        **{'flux', 'absorptance', 'transmittance', 'reflectance', 'intensity',
        'irradiance', 'radiance', 'exitance', 'R-Factor', 'T-Factor',
        'relative', 'other'}**,
        Quantity of measurement for each element of the spectral data.
    reflection_geometry : unicode, optional
        **{'di:8', 'de:8', '8:di', '8:de', 'd:d', 'd:0', '45a:0', '45c:0',
        '0:45a', '45x:0', '0:45x', 'other'}**,
        Spectral reflectance factors geometric conditions.
    transmission_geometry : unicode, optional
        **{'0:0', 'di:0', 'de:0', '0:di', '0:de', 'd:d', 'other'}**,
        Spectral transmittance factors geometric conditions.
    bandwidth_FWHM : numeric, optional
        Spectroradiometer full-width half-maximum bandwidth in nanometers.
    bandwidth_corrected : bool, optional
        Specifies if bandwidth correction has been applied to the measured
        data.

    References
    ----------
    :cite:`IESComputerCommittee2014a`
    """

    def __init__(self,
                 path=None,
                 header=None,
                 units=None,
                 reflection_geometry=None,
                 transmission_geometry=None,
                 bandwidth_FWHM=None,
                 bandwidth_corrected=None):
        super(SpectralDistribution_AMPAS, self).__init__(
            path, header, units, reflection_geometry, transmission_geometry,
            bandwidth_FWHM, bandwidth_corrected)


class MultiSpectralDistributions_AMPAS(AMPAS_SpectralDataMixin,
                                       MultiSpectralDistributions):
    """
    Defines the *A.M.P.A.S* multi-spectral distributions.

    This class can read *A.M.P.A.S* spectral data JSON files.

    Parameters
    ----------
    path : unicode, optional
        Spectral data JSON file path.
    header : AMPAS_SpectralDataHeader, optional
        *A.M.P.A.S.* spectral distribution header.
    units : unicode, optional
        **{'flux', 'absorptance', 'transmittance', 'reflectance', 'intensity',
        'irradiance', 'radiance', 'exitance', 'R-Factor', 'T-Factor',
        'relative', 'other'}**,
        Quantity of measurement for each element of the spectral data.
    reflection_geometry : unicode, optional
        **{'di:8', 'de:8', '8:di', '8:de', 'd:d', 'd:0', '45a:0', '45c:0',
        '0:45a', '45x:0', '0:45x', 'other'}**,
        Spectral reflectance factors geometric conditions.
    transmission_geometry : unicode, optional
        **{'0:0', 'di:0', 'de:0', '0:di', '0:de', 'd:d', 'other'}**,
        Spectral transmittance factors geometric conditions.
    bandwidth_FWHM : numeric, optional
        Spectroradiometer full-width half-maximum bandwidth in nanometers.
    bandwidth_corrected : bool, optional
        Specifies if bandwidth correction has been applied to the measured
        data.

    References
    ----------
    :cite:`IESComputerCommittee2014a`
    """

    def __init__(self,
                 path=None,
                 header=None,
                 units=None,
                 reflection_geometry=None,
                 transmission_geometry=None,
                 bandwidth_FWHM=None,
                 bandwidth_corrected=None):
        super(MultiSpectralDistributions_AMPAS, self).__init__(
            path, header, units, reflection_geometry, transmission_geometry,
            bandwidth_FWHM, bandwidth_corrected)


class Dyer2017DatasetLoader(AbstractDatasetLoader):
    """
    Defines the *Dyer et al. (2017)* *RAW to ACES Utility Data* dataset
    loader.

    Attributes
    ----------
    ID

    Methods
    -------
    load

    References
    ----------
    :cite:`Dyer2017`
    """

    ID = '3372171'
    """
    Dataset record id, i.e. the *Zenodo* record number.

    ID : unicode
    """

    def __init__(self):
        super(Dyer2017DatasetLoader,
              self).__init__(datasets()[Dyer2017DatasetLoader.ID])

    def load(self):
        """
        Syncs, parses, converts and returns the *Dyer et al. (2017)*
        *RAW to ACES Utility Data* dataset content.

        Returns
        -------
        OrderedDict
            *Dyer et al. (2017)* *RAW to ACES Utility Data* dataset content.

        Examples
        --------
        >>> from colour_datasets.utilities import suppress_stdout
        >>> dataset = Dyer2017DatasetLoader()
        >>> with suppress_stdout():
        ...     dataset.load()
        >>> len(dataset.content.keys())
        4
        """

        super(Dyer2017DatasetLoader, self).sync()

        self._content = OrderedDict()

        for directory in ('camera', 'cmf', 'illuminant', 'training'):
            self._content[directory] = OrderedDict()
            factory = (SpectralDistribution_AMPAS if directory == 'illuminant'
                       else MultiSpectralDistributions_AMPAS)
            glob_pattern = os.path.join(self.record.repository, 'dataset',
                                        'data', directory, '*.json')
            for path in glob.glob(glob_pattern):
                msds = factory(path).read()
                self._content[directory][msds.name] = msds

        return self._content


_DYER2017_DATASET_LOADER = None
"""
Singleton instance of the *Dyer et al. (2017)* *RAW to ACES Utility Data*
dataset loader.

_DYER2017_DATASET_LOADER : Dyer2017DatasetLoader
"""


def build_Dyer2017(load=True):
    """
    Singleton factory that builds the *Dyer et al. (2017)*
    *RAW to ACES Utility Data* dataset loader.

    Parameters
    ----------
    load : bool, optional
        Whether to load the dataset upon instantiation.

    Returns
    -------
    Dyer2017DatasetLoader
        Singleton instance of the *Dyer et al. (2017)*
        *RAW to ACES Utility Data* dataset loader.

    References
    ----------
    :cite:`Dyer2017`
    """

    global _DYER2017_DATASET_LOADER

    if _DYER2017_DATASET_LOADER is None:
        _DYER2017_DATASET_LOADER = Dyer2017DatasetLoader()
        if load:
            _DYER2017_DATASET_LOADER.load()

    return _DYER2017_DATASET_LOADER
