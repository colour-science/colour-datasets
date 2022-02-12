"""
Spreadsheet Utilities
=====================

Defines various spreadsheet related utilities.

References
----------
-   :cite:`OpenpyxlDevelopers2019` : Openpyxl Developers. (2019). openpyxl.
    https://bitbucket.org/openpyxl/openpyxl/
"""

from __future__ import annotations

import re
import xlrd

from colour.hints import Dict, Integer, List, Union
from colour.utilities import CaseInsensitiveMapping

__author__ = "Colour Developers, Openpyxl Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__copyright__ += ", "
__copyright__ = "Copyright (C) 2010 openpyxl"
__license__ = "New BSD License - https://opensource.org/licenses/BSD-3-Clause"
__license__ += ", "
__license__ += "MIT Licence - https://opensource.org/licenses/MIT"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "column_to_index",
    "row_to_index",
    "index_to_column",
    "index_to_row",
    "cell_range_values",
]


def _column_number_to_letters(number: Integer) -> str:
    """
    Convert given column number into a column letters.

    Right shifts the column index by 26 to find column letters in reverse
    order. These numbers are 1-based, and can be converted to ASCII
    ordinals by adding 64.

    Parameters
    ----------
    number
        Column number to convert to column letters.

    Returns
    -------
    :class:`str`
        Column letters.

    References
    ----------
    :cite:`OpenpyxlDevelopers2019`

    Examples
    --------
    # Doctests skip for Python 2.x compatibility.
    >>> _column_number_to_letters(128)  # doctest: +SKIP
    'DX'
    """

    assert (
        1 <= number <= 18278
    ), f"Column number {number} must be in range [1, 18278]!"

    letters = []
    while number > 0:
        number, remainder = divmod(number, 26)
        if remainder == 0:
            remainder = 26
            number -= 1
        letters.append(chr(remainder + 64))

    return "".join(reversed(letters))


_LETTERS_TO_NUMBER_CACHE: CaseInsensitiveMapping = CaseInsensitiveMapping()
"""Letters, e.g. *Microsoft Excel* column letters to numbers cache."""

_NUMBER_TO_LETTERS_CACHE: Dict = {}
"""Numbers to letters, e.g. *Microsoft Excel* column letters cache."""

for i in range(1, 18279):
    letter = _column_number_to_letters(i)
    _NUMBER_TO_LETTERS_CACHE[i] = letter
    _LETTERS_TO_NUMBER_CACHE[letter] = i


def row_to_index(row: Union[Integer, str]) -> Integer:
    """
    Return the 0-based index of given row name.

    Parameters
    ----------
    row
        Row name.

    Returns
    -------
    :class`int` or :class:`str`
        0-based row index.

    Examples
    --------
    >>> row_to_index('1')
    0
    """

    row = int(row)

    assert row > 0, "Row must be greater than 0!"

    return row - 1


def index_to_row(index: Integer) -> str:
    """
    Return the row name of given 0-based index.

    Parameters
    ----------
    index
        0-based row index.

    Returns
    -------
    :class:`str
        Row name.

    Examples
    --------
    # Doctests skip for Python 2.x compatibility.
    >>> index_to_row(0)  # doctest: +SKIP
    '1'
    """

    return str(index + 1)


def column_to_index(column: str) -> Integer:
    """
    Return the 0-based index of given column letters.

    Parameters
    ----------
    column
        Column letters

    Returns
    -------
    :class:`int`
        0-based column index.

    Examples
    --------
    >>> column_to_index('A')
    0
    """

    return _LETTERS_TO_NUMBER_CACHE[column] - 1


def index_to_column(index: Integer) -> str:
    """
    Return the column letters of given 0-based index.

    Parameters
    ----------
    index
        0-based column index.

    Returns
    -------
    :class:`str`
        Column letters

    Examples
    --------
    # Doctests skip for Python 2.x compatibility.
    >>> index_to_column(0)  # doctest: +SKIP
    'A'
    """

    return _NUMBER_TO_LETTERS_CACHE[index + 1]


_CELL_RANGE_REGEX: re.Pattern = re.compile(
    r"^[$]?(?P<column_in>[A-Za-z]{1,3})?[$]?(?P<row_in>\d+)?"
    r"(:[$]?(?P<column_out>[A-Za-z]{1,3})?[$]?(?P<row_out>\d+)?)?$"
)
"""Regular expression to match a cell range, e.g. "A1:C3"."""


def cell_range_values(sheet: xlrd.sheet.Sheet, cell_range: str) -> List[str]:
    """
    Return given workbook sheet cell range values, i.e. the values of the
    rows and columns for given cell range.

    Parameters
    ----------
    sheet : Sheet
        Workbook sheet.
    cell_range
        Cell range values, e.g. "A1:C3".

    Returns
    -------
    :class:`list`
        List of row values.
    """

    table: List[str] = []

    match = re.match(_CELL_RANGE_REGEX, cell_range)
    if match:
        groups = match.groupdict()
    else:
        return table

    column_in = column_to_index(groups["column_in"])
    row_in = row_to_index(groups["row_in"])
    column_out = column_to_index(groups["column_out"])
    row_out = row_to_index(groups["row_out"])

    for row in range(row_in, row_out + 1, 1):
        table.append(
            sheet.row_values(
                row, start_colx=column_in, end_colx=column_out + 1
            )
        )

    return table
