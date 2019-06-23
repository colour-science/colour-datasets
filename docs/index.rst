Colour - Datasets
=================

Colour science datasets for use with
`Colour <https://github.com/colour-science/colour>`_ or any Python package
manipulating colours. The datasets are hosted in `Zenodo <https://zenodo.org>`_
under the
`Colour Science - Datasets <https://zenodo.org/communities/colour-science-datasets/>`_
community.

It is open source and freely available under the
`New BSD License <https://opensource.org/licenses/BSD-3-Clause>`_ terms.

.. contents:: **Table of Contents**
    :backlinks: none
    :depth: 3

.. sectnum::

Features
--------

Installation
------------

Primary Dependencies
^^^^^^^^^^^^^^^^^^^^

**Colour - Datasets** requires various dependencies in order to run:

-  `Python 2.7 <https://www.python.org/download/releases/>`_ or
   `Python 3.7 <https://www.python.org/download/releases/>`_
-  `Colour Science <https://www.colour-science.org>`_
-  `tqdm <https://tqdm.github.io/>`_
-  `xlrd <https://xlrd.readthedocs.io/>`_

Pypi
^^^^

Once the dependencies satisfied, **Colour - Datasets** can be installed from
the `Python Package Index <http://pypi.python.org/pypi/colour-datasets>`_ by
issuing this command in a shell::

	pip install colour-datasets

The tests suite dependencies are installed as follows::

    pip install 'colour-datasets[tests]'

The documentation building dependencies are installed as follows::

    pip install 'colour-datasets[docs]'

The overall development dependencies are installed as follows::

    pip install 'colour-datasets[development]'

Usage
-----

API
^^^

The main reference for
`Colour - Datasets <https://github.com/colour-science/colour-datasets>`_
is the manual:

.. toctree::
    :maxdepth: 4

    manual

Examples
^^^^^^^^

Most of the objects are available from the ``colour_datasets`` namespace:

.. code-block:: python

    >>> import colour_datasets

The available datasets are listed with the ``colour_datasets.datasets()``
definition:

.. code-block:: python

    >>> print(colour_datasets.datasets())

::

    colour-science-datasets
    =======================

    Datasets : 4
    Synced   : 2
    URL      : https://zenodo.org/communities/colour-science-datasets/

    Datasets
    --------

    [ ] 3245883 : Camera Spectral Sensitivity Database
    [x] 3245875 : Labsphere SRS-99-020
    [ ] 3245895 : New Color Specifications for ColorChecker SG and Classic Charts
    [x] 3252742 : Observer Function Database

A ticked checkbox means that the particular dataset has been synced locally.
A dataset is loaded by using its unique number: *3245895*:

.. code-block:: python

    >>> print(colour_datasets.load('3245895').keys())

::

    Downloading "urls.txt" file: 8.19kB [00:01, 4.49kB/s]
    Downloading "ColorChecker24_After_Nov2014.zip" file: 8.19kB [00:01, 5.20kB/s]
    Downloading "ColorChecker24_Before_Nov2014.zip" file: 8.19kB [00:01, 5.19kB/s]
    Downloading "ColorCheckerSG_After_Nov2014.zip" file: 8.19kB [00:01, 6.27kB/s]
    Downloading "ColorCheckerSG_Before_Nov2014.zip" file: 8.19kB [00:01, 7.48kB/s]
    Unpacking "/Users/kelsolaar/.colour-science/colour-datasets/3245895/dataset/ColorCheckerSG_Before_Nov2014.zip" archive...
    Unpacking "/Users/kelsolaar/.colour-science/colour-datasets/3245895/dataset/ColorCheckerSG_After_Nov2014.zip" archive...
    Unpacking "/Users/kelsolaar/.colour-science/colour-datasets/3245895/dataset/ColorChecker24_After_Nov2014.zip" archive...
    Unpacking "/Users/kelsolaar/.colour-science/colour-datasets/3245895/dataset/ColorChecker24_Before_Nov2014.zip" archive...
    odict_keys(['ColorChecker24 - After November 2014', 'ColorChecker24 - Before November 2014', 'ColorCheckerSG - After November 2014', 'ColorCheckerSG - Before November 2014'])

Alternatively, a dataset can be loaded by using its full title:
*New Color Specifications for ColorChecker SG and Classic Charts*

.. code-block:: python

    >>> print(colour_datasets.load('3245895').keys())
    odict_keys(['ColorChecker24 - After November 2014', 'ColorChecker24 - Before November 2014', 'ColorCheckerSG - After November 2014', 'ColorCheckerSG - Before November 2014'])

Contributing
------------

If you would like to contribute to `Colour - Datasets <https://github.com/colour-science/colour-datasets>`_,
please refer to the following `Contributing <https://www.colour-science.org/contributing/>`_
guide for `Colour <https://github.com/colour-science/colour>`_.

Bibliography
------------

The bibliography is available in the repository in
`BibTeX <https://github.com/colour-science/colour-datasets/blob/develop/BIBLIOGRAPHY.bib>`_
format.

About
-----

| **Colour - Datasets** by Colour Developers
| Copyright © 2019 – Colour Developers – `colour-science@googlegroups.com <colour-science@googlegroups.com>`_
| This software is released under terms of New BSD License: https://opensource.org/licenses/BSD-3-Clause
| `https://github.com/colour-science/colour-datasets <https://github.com/colour-science/colour-datasets>`_
