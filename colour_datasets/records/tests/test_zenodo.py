"""
Define the unit tests for the :mod:`colour_datasets.records.configuration`
module.
"""

import os
import textwrap
import unittest

from colour_datasets.records import Community, Configuration, Record
from colour_datasets.utilities import json_open

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestRecord",
    "TestCommunity",
]


class TestRecord(unittest.TestCase):
    """
    Define :class:`colour_datasets.records.zenodo.Record` class unit tests
    methods.
    """

    def setUp(self):
        """Initialise the common tests attributes."""

        self._data = json_open("https://zenodo.org/api/records/3245883")
        self._configuration = Configuration()

        self._record = Record(self._data, self._configuration)

    def test_required_attributes(self):
        """Test the presence of required attributes."""

        required_attributes = (
            "data",
            "configuration",
            "repository",
            "id",
            "title",
        )

        for attribute in required_attributes:
            self.assertIn(attribute, dir(Record))

    def test_required_methods(self):
        """Test the presence of required methods."""

        required_methods = (
            "__init__",
            "__str__",
            "__repr__",
            "from_id",
            "synced",
            "pull",
            "remove",
        )

        for method in required_methods:
            self.assertIn(method, dir(Record))

    def test_configuration(self):
        """
        Test :func:colour_datasets.records.zenodo.Record.configuration`
        property.
        """

        self.assertEqual(self._record.configuration, self._configuration)

    def test_data(self):
        """Test :func:colour_datasets.records.zenodo.Record.data` property."""

        self.assertEqual(self._record.data, self._data)

    def test_repository(self):
        """
        Test :func:colour_datasets.records.zenodo.Record.repository`
        property.
        """

        self.assertEqual(
            self._record.repository,
            os.path.join(self._configuration.repository, "3245883"),
        )

    def test_id(self):
        """Test :func:colour_datasets.records.zenodo.Record.id` property."""

        self.assertEqual(self._record.id, "3245883")

    def test_title(self):
        """
        Test :func:colour_datasets.records.zenodo.Record.title`
        property.
        """

        self.assertEqual(
            self._record.title,
            "Camera Spectral Sensitivity Database - Jiang et al. (2013)",
        )

    def test__init__(self):
        """
        Test :func:`colour_datasets.records.zenodo.Record.__init__` method.
        """

        record = Record(self._data, self._configuration)

        self.assertEqual(
            record.title,
            "Camera Spectral Sensitivity Database - Jiang et al. (2013)",
        )

    def test__str__(self):
        """
        Test :func:`colour_datasets.records.zenodo.Record.__str__` method.
        """

        self.assertEqual(
            str(self._record),
            textwrap.dedent(
                """
Camera Spectral Sensitivity Database - Jiang et al. (2013) - 1.0.0
==================================================================

Record ID        : 3245883
Authors          : Jiang, Jun; Liu, Dengyu; Gu, Jinwei; Süsstrunk, Sabine
License          : cc-by-nc-sa-4.0
DOI              : 10.5281/zenodo.3245883
Publication Date : 2019-06-14
URL              : https://zenodo.org/records/3245883

Description
-----------

Source URL: http://www.gujinwei.org/research/camspec/db.html Source DOI:
10.1109/WACV.2013.6475015 Camera spectral sensitivity functions relate scene
radiance with captured RGB triplets. They are important for many computer
vision tasks that use color information, such as multispectral imaging, and
color constancy. We create a database of 28 cameras covering a variety of
types. The database contains the spectral sensitivity functions for 28 cameras,
including professional DSLRs, point-and-shoot, industrial and mobile phone
camera. We use a spectrometer PR655 from Photo Research Inc., a light source
and monochrometer combined with an integrating sphere to do the measurement.
Each measurement starts from wavelength 400nm to 720nm in an interval of 10nm.
Measured Sensitivities are normalized to 1 for RGB channels seperately. The
database is in the form of a text file. Each entry starts with camera name and
follows by measured spectral sensitivities in red, green and blue channel.

Files
-----

- camlist&equipment.txt : https://zenodo.org/api/records/3245883/files/\
camlist&equipment.txt
- camspec_database.txt : https://zenodo.org/api/records/3245883/files/\
camspec_database.txt
- urls.txt : https://zenodo.org/api/records/3245883/files/urls.txt"""
            )[1:],
        )

    def test__repr__(self):
        """
        Test :func:`colour_datasets.records.zenodo.Record.__repr__` method.
        """

        self.assertIsInstance(
            eval(  # noqa: PGH001, S307
                repr(self._record),
                {},
                {"Record": Record, "Configuration": Configuration},
            ),
            Record,
        )

    def test_from_id(self):
        """Test :func:`colour_datasets.records.zenodo.Record.from_id` method."""

        record = Record.from_id("3245883")

        self.assertIsInstance(record, Record)
        self.assertEqual(
            record.title,
            "Camera Spectral Sensitivity Database - Jiang et al. (2013)",
        )

    def test_synced(self):
        """Test :func:`colour_datasets.records.zenodo.Record.synced` method."""

        self._record.pull()
        self.assertTrue(self._record.synced())
        self._record.remove()
        self.assertFalse(self._record.synced())

    def test_pull(self):
        """Test :func:`colour_datasets.records.zenodo.Record.pull` method."""

        self._record.remove()
        self._record.pull()
        self.assertTrue(self._record.synced())

    def test_remove(self):
        """Test :func:`colour_datasets.records.zenodo.Record.remove` method."""

        self._record.pull()
        self._record.remove()
        self.assertFalse(self._record.synced())


class TestCommunity(unittest.TestCase):
    """
    Define :class:`colour_datasets.records.zenodo.Community` class unit tests
    methods.
    """

    def setUp(self):
        """Initialise the common tests attributes."""

        community_data = json_open(
            "https://zenodo.org/api/communities/colour-science-datasets-tests"
        )
        records_data = json_open(community_data["links"]["records"])

        self._data = {
            "community": community_data,
            "records": records_data,
        }
        self._configuration = Configuration()

        self._community = Community(self._data, self._configuration)

    def test_required_attributes(self):
        """Test the presence of required attributes."""

        required_attributes = (
            "data",
            "configuration",
            "repository",
            "records",
        )

        for attribute in required_attributes:
            self.assertIn(attribute, dir(Community))

    def test_required_methods(self):
        """Test the presence of required methods."""

        required_methods = (
            "__init__",
            "__str__",
            "__repr__",
            "__getitem__",
            "__iter__",
            "__len__",
            "from_id",
            "synced",
            "pull",
            "remove",
        )

        for method in required_methods:
            self.assertIn(method, dir(Community))

    def test_configuration(self):
        """
        Test :func:colour_datasets.records.zenodo.Community.configuration`
        property.
        """

        self.assertEqual(self._community.configuration, self._configuration)

    def test_data(self):
        """
        Test :func:colour_datasets.records.zenodo.Community.data` property.
        """

        self.assertEqual(self._community.data, self._data)

    def test_repository(self):
        """
        Test :func:colour_datasets.records.zenodo.Community.repository`
        property.
        """

        self.assertEqual(
            self._community.repository, self._configuration.repository
        )

    def test_records(self):
        """
        Test :func:colour_datasets.records.zenodo.Community.records` property.
        """

        self.assertIn("3245883", list(self._community.records))

    def test__init__(self):
        """
        Test :func:`colour_datasets.records.zenodo.Community.__init__` method.
        """

        community = Community(self._data, self._configuration)

        self.assertEqual(
            community["3245883"].title,
            "Camera Spectral Sensitivity Database - Jiang et al. (2013)",
        )

    def test__str__(self):
        """
        Test :func:`colour_datasets.records.zenodo.Community.__str__` method.
        """

        self._community.remove()

        self.assertEqual(
            str(self._community),
            textwrap.dedent(
                """
colour-science-datasets
=======================

Datasets : 4
Synced   : 0
URL      : https://zenodo.org/communities/colour-science-datasets-tests

Datasets
--------

[ ] 3245883 : Camera Spectral Sensitivity Database - Jiang et al. (2013)
[ ] 3245875 : Labsphere SRS-99-020 - Labsphere (2019)
[ ] 3245895 : New Color Specifications for ColorChecker SG and Classic Charts \
- X-Rite (2016)
[ ] 3252742 : Observer Function Database - Asano (2015)"""
            )[1:],
        )

    def test__repr__(self):
        """
        Test :func:`colour_datasets.records.zenodo.Community.__repr__` method.
        """

        self.assertIsInstance(
            eval(  # noqa: PGH001, S307
                repr(self._community),
                {},
                {"Community": Community, "Configuration": Configuration},
            ),
            Community,
        )

    def test__getitem__(self):
        """
        Test :func:`colour_datasets.records.zenodo.Community.__getitem__`
        method.
        """

        self.assertIs(
            self._community["3245883"], self._community.records["3245883"]
        )

    def test__iter__(self):
        """
        Test :func:`colour_datasets.records.zenodo.Community.__iter__`
        method.
        """

        self.assertListEqual(
            list(self._community), list(self._community.records)
        )

    def test__len__(self):
        """
        Test :func:`colour_datasets.records.zenodo.Community.__getitem__`
        method.
        """

        self.assertEqual(len(self._community), len(self._community.records))

    def test_from_id(self):
        """
        Test :func:`colour_datasets.records.zenodo.Community.from_id` method.
        """

        community = Community.from_id("colour-science-datasets")

        self.assertIsInstance(community, Community)
        self.assertEqual(
            community["3245883"].title,
            "Camera Spectral Sensitivity Database - Jiang et al. (2013)",
        )

    def test_synced(self):
        """
        Test :func:`colour_datasets.records.zenodo.Community.synced` method.
        """

        self._community.pull()
        self.assertTrue(self._community.synced())
        self._community.remove()
        self.assertFalse(self._community.synced())

    def test_pull(self):
        """
        Test :func:`colour_datasets.records.zenodo.Community.pull` method.
        """

        self._community.remove()
        self._community.pull()
        self.assertTrue(self._community.synced())

    def test_remove(self):
        """
        Test :func:`colour_datasets.records.zenodo.Community.remove` method.
        """

        self._community.pull()
        self._community.remove()
        self.assertFalse(self._community.synced())


if __name__ == "__main__":
    unittest.main()
