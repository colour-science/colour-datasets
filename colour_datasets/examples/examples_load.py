# -*- coding: utf-8 -*-
"""
Showcases *Colour - Datasets* loading.
"""

from colour.utilities import message_box

import colour_datasets

message_box('Listing the available datasets.\n\n'
            'Note: A ticked checkbox means that the particular dataset '
            'has been synced locally.')
print(colour_datasets.datasets())

message_box('A dataset is loaded by using its unique number: "3245895"')
print(colour_datasets.load('3245895'))

message_box('Or alternatively its full title: "New Color Specifications '
            'for ColorChecker SG and Classic Charts"')
print(
    colour_datasets.load(
        'New Color Specifications for ColorChecker SG and Classic Charts'))
