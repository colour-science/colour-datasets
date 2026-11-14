"""Define offline regression tests for record archive extraction."""

import gzip
import json
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from colour_datasets.records import Configuration, Record


class TestRecordArchives(unittest.TestCase):
    """Test record extraction without a packaging library or network access."""

    def test_pull_archives(self) -> None:
        """Extract the supported archive formats and preserve record metadata."""

        for archive_format in ("zip", "tar", "gztar", "bztar", "gzip"):
            with (
                self.subTest(archive_format=archive_format),
                tempfile.TemporaryDirectory() as directory,
            ):
                source = os.path.join(directory, "source")
                os.mkdir(source)
                with open(os.path.join(source, "sample.txt"), "w") as sample:
                    sample.write("spectral data")
                if archive_format == "gzip":
                    archive = os.path.join(directory, "sample.gz")
                    with gzip.open(archive, "wb") as compressed:
                        compressed.write(b"spectral data")
                else:
                    archive = shutil.make_archive(
                        os.path.join(directory, "sample"), archive_format, source
                    )
                configuration = Configuration(dict(Configuration()))
                configuration.repository = os.path.join(directory, "records")
                data = {
                    "id": 1,
                    "metadata": {"title": "Archive regression"},
                    "files": [
                        {
                            "key": os.path.basename(archive),
                            "links": {
                                "self": "https://example.com/"
                                + os.path.basename(archive)
                            },
                            "checksum": "md5:unused",
                        }
                    ],
                }
                record = Record(data, configuration)

                def download(
                    _url: str,
                    filename: str,
                    *_args: object,
                    source_archive: str = archive,
                ) -> None:
                    """Copy the generated archive in place of downloading it."""

                    shutil.copyfile(source_archive, filename)

                with patch(
                    "colour_datasets.records.zenodo.url_download", side_effect=download
                ):
                    record.pull(use_urls_txt_file=False)
                extracted = os.path.join(
                    record.repository, "dataset", "sample", "sample.txt"
                )
                if archive_format == "gzip":
                    extracted = os.path.join(
                        record.repository, "dataset", "sample", "sample"
                    )
                with open(extracted) as sample:
                    self.assertEqual(sample.read(), "spectral data")
                with open(os.path.join(record.repository, "record.json")) as metadata:
                    self.assertEqual(json.load(metadata), data)
                self.assertTrue(record.synced())
