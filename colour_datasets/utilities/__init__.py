"""
Utilities
=========

Common utilities for dataset processing and manipulation.

This subpackage provides file handling utilities, data compression tools,
and spreadsheet processing functions to support dataset operations.
"""

from .common import (
    hash_md5,
    json_open,
    suppress_stdout,
    unpack_gzipfile,
    url_download,
)

# isort: split

from .spreadsheet import (
    cell_range_values,
    column_to_index,
    index_to_column,
    index_to_row,
    row_to_index,
)

__all__ = [
    "hash_md5",
    "json_open",
    "suppress_stdout",
    "unpack_gzipfile",
    "url_download",
]
__all__ += [
    "cell_range_values",
    "column_to_index",
    "index_to_column",
    "index_to_row",
    "row_to_index",
]
