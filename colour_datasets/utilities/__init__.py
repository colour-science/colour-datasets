"""
Utilities
=========

Common utilities for dataset processing and manipulation.

This subpackage provides file handling utilities, data compression tools,
and spreadsheet processing functions to support dataset operations.
"""

# isort: skip_file

from .common import (
    suppress_stdout,
    hash_md5,
    url_download,
    json_open,
    unpack_gzipfile,
)
from .spreadsheet import (
    row_to_index,
    index_to_row,
    column_to_index,
    index_to_column,
    cell_range_values,
)

__all__ = [
    "suppress_stdout",
    "hash_md5",
    "url_download",
    "json_open",
    "unpack_gzipfile",
]
__all__ += [
    "row_to_index",
    "index_to_row",
    "column_to_index",
    "index_to_column",
    "cell_range_values",
]
