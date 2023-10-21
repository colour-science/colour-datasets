"""
Define the unit tests for the :mod:`colour_datasets.utilities.spreadsheet`
module.
"""

import os
import unittest

import xlrd

from colour_datasets.utilities import (
    cell_range_values,
    column_to_index,
    index_to_column,
    index_to_row,
    row_to_index,
)

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestRowToIndex",
    "TestIndexToRow",
    "TestColumnToIndex",
    "TestIndexToColumn",
    "TestCellRangeValues",
]


class TestRowToIndex(unittest.TestCase):
    """
    Define :func:`colour_datasets.utilities.spreadsheet.row_to_index`
    definition unit tests methods.
    """

    def test_row_to_index(self):
        """
        Test :func:`colour_datasets.utilities.spreadsheet.row_to_index`
        definition.
        """

        self.assertEqual(row_to_index(1), 0)

        self.assertEqual(row_to_index(10), 9)

        self.assertEqual(row_to_index("100"), 99)

        self.assertRaises(AssertionError, lambda: row_to_index(0))


class TestIndexToRow(unittest.TestCase):
    """
    Define :func:`colour_datasets.utilities.spreadsheet.index_to_row`
    definition unit tests methods.
    """

    def test_index_to_row(self):
        """
        Test :func:`colour_datasets.utilities.spreadsheet.index_to_row`
        definition.
        """

        self.assertEqual(index_to_row(0), "1")

        self.assertEqual(index_to_row(9), "10")

        self.assertEqual(index_to_row(99), "100")


class TestColumnToIndex(unittest.TestCase):
    """
    Define :func:`colour_datasets.utilities.spreadsheet.column_to_index`
    definition unit tests methods.
    """

    def test_column_to_index(self):
        """
        Test :func:`colour_datasets.utilities.spreadsheet.column_to_index`
        definition.
        """

        self.assertEqual(column_to_index("A"), 0)

        self.assertEqual(column_to_index("J"), 9)

        self.assertEqual(column_to_index("AA"), 26)

        self.assertRaises(KeyError, lambda: column_to_index("AAAA"))


class TestIndexToColumn(unittest.TestCase):
    """
    Define :func:`colour_datasets.utilities.spreadsheet.index_to_column`
    definition unit tests methods.
    """

    def test_index_to_column(self):
        """
        Test :func:`colour_datasets.utilities.spreadsheet.index_to_column`
        definition.
        """

        self.assertEqual(index_to_column(0), "A")

        self.assertEqual(index_to_column(9), "J")

        self.assertEqual(index_to_column(26), "AA")


class TestCellRangeValues(unittest.TestCase):
    """
    Define :func:`colour_datasets.utilities.spreadsheet.cell_range_values`
    definition unit tests methods.
    """

    def test_cell_range_values(self):
        """
        Test :func:`colour_datasets.utilities.spreadsheet.cell_range_values`
        definition.
        """

        workbook_path = os.path.join(
            os.path.dirname(__file__), "resources", "Workbook.xlsx"
        )
        sheet = xlrd.open_workbook(workbook_path).sheet_by_index(0)
        self.assertListEqual(
            cell_range_values(sheet, "A1:E5"),
            [
                [1.0, 2.0, 3.0, 4.0, 5.0],
                [2.0, 3.0, 4.0, 5.0, 6.0],
                [3.0, 4.0, 5.0, 6.0, 7.0],
                [4.0, 5.0, 6.0, 7.0, 8.0],
                [5.0, 6.0, 7.0, 8.0, 9.0],
            ],
        )


if __name__ == "__main__":
    unittest.main()
