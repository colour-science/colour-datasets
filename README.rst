Colour - Datasets
=================

.. start-badges

|actions| |coveralls| |codacy| |version|

.. |actions| image:: https://img.shields.io/github/actions/workflow/status/colour-science/colour-datasets/.github/workflows/continuous-integration-quality-unit-tests.yml?branch=develop&style=flat-square
    :target: https://github.com/colour-science/colour-datasets/actions
    :alt: Develop Build Status
.. |coveralls| image:: http://img.shields.io/coveralls/colour-science/colour-datasets/develop.svg?style=flat-square
    :target: https://coveralls.io/r/colour-science/colour-datasets
    :alt: Coverage Status
.. |codacy| image:: https://img.shields.io/codacy/grade/83345fbde65545d2a4499f32e72866ed/develop.svg?style=flat-square
    :target: https://app.codacy.com/gh/colour-science/colour-datasets
    :alt: Code Grade
.. |version| image:: https://img.shields.io/pypi/v/colour-datasets.svg?style=flat-square
    :target: https://pypi.org/project/colour-datasets
    :alt: Package Version

.. end-badges

Colour science datasets for use with
`Colour <https://github.com/colour-science/colour>`__ or any Python package
manipulating colours. The datasets are hosted in `Zenodo <https://zenodo.org>`__
under the
`Colour Science - Datasets <https://zenodo.org/communities/colour-science-datasets>`__
community.

It is open source and freely available under the
`BSD-3-Clause <https://opensource.org/licenses/BSD-3-Clause>`__ terms.

.. contents:: **Table of Contents**
    :backlinks: none
    :depth: 2

.. sectnum::

Features
--------

**Colour - Datasets** was created to overcome issues encountered frequently
when trying to access or use colour science datasets:

- No straightforward ingestion path for dataset content.
- No simple loading mechanism for dataset content.
- Unavailability of the dataset, e.g., download url is down, dataset content is
  passed directly from hand to hand.
- No information regarding the definitive origination of the dataset.

**Colour - Datasets** offers all the above: it allows users to ingest and load
colour science datasets with a single function call. The datasets information
is hosted on `Zenodo <https://zenodo.org/communities/colour-science-datasets>`__
where the record for a dataset typically contain:

- An *urls.txt* file describing the urls to source the dataset files from.
- A copy of those files in the eventuality where the source files are not
  available or the content has changed without notice.
- Information about the authors, content and licensing.

When no explicit licensing information is available, the dataset adopts the
**Other (Not Open)** licensing scheme, implying that assessing usage conditions
is at the sole discretion of the users.

Examples
^^^^^^^^

**Colour - Datasets** can also be used online with
`Google Colab <https://colab.research.google.com/notebook#fileId=1YwIfDTBVP3XUYJAyZVEDWj92DJCB0_3v&offline=true&sandboxMode=true>`__.

Most of the objects are available from the ``colour_datasets`` namespace:

.. code-block:: python

    import colour_datasets

The available datasets are listed with the ``colour_datasets.datasets()``
definition:

.. code-block:: python

    print(colour_datasets.datasets())

.. code-block:: text

    colour-science-datasets
    =======================

    Datasets : 23
    Synced   : 1
    URL      : https://zenodo.org/communities/colour-science-datasets/

    Datasets
    --------

    [ ] 3269926 : Agfa IT8.7/2 Set - Marszalec (n.d.)
    [ ] 8314702 : Camera Dataset - Solomatov and Akkaynak (2023)
    [ ] 3245883 : Camera Spectral Sensitivity Database - Jiang et al. (2013)
    [ ] 3367463 : Constant Hue Loci Data - Hung and Berns (1995)
    [ ] 3362536 : Constant Perceived-Hue Data - Ebner and Fairchild (1998)
    [ ] 3270903 : Corresponding-Colour Datasets - Luo and Rhodes (1999)
    [ ] 3269920 : Forest Colors - Jaaskelainen et al. (1994)
    [ ] 4394536 : LUTCHI Colour Appearance Data - Luo and Rhodes (1997)
    [x] 3245875 : Labsphere SRS-99-020 - Labsphere (2019)
    [ ] 3269924 : Lumber Spectra - Hiltunen (n.d.)
    [ ] 4051012 : Measured Commercial LED Spectra - Brendel (2020)
    [ ] 3269918 : Munsell Colors Glossy (All) (Spectrofotometer Measured) - Orava (n.d.)
    [ ] 3269916 : Munsell Colors Glossy (Spectrofotometer Measured) - Haanpalo (n.d.)
    [ ] 3269914 : Munsell Colors Matt (AOTF Measured) - Hauta-Kasari (n.d.)
    [ ] 3269912 : Munsell Colors Matt (Spectrofotometer Measured) - Hauta-Kasari (n.d.)
    [ ] 3245895 : New Color Specifications for ColorChecker SG and Classic Charts - X-Rite (2016)
    [ ] 3252742 : Observer Function Database - Asano (2015)
    [ ] 3269922 : Paper Spectra - Haanpalo (n.d.)
    [ ] 6590768 : Physlight - Camera Spectral Sensitivity Curves - Winquist et al. (2022)
    [ ] 3372171 : RAW to ACES Utility Data - Dyer et al. (2017)
    [ ] 4642271 : Spectral Database of Commonly Used Cine Lighting - Karge et al. (2015)
    [ ] 4297288 : Spectral Sensitivity Database - Zhao et al. (2009)
    [ ] 4050598 : Spectral Upsampling Coefficient Tables - Jakob and Hanika. (2019)

A ticked checkbox means that the particular dataset has been synced locally.
A dataset is loaded by using its unique number: *3245895*:

.. code-block:: python

    print(colour_datasets.load("3245895").keys())

::

    Pulling "New Color Specifications for ColorChecker SG and Classic Charts" record content...
    Downloading "urls.txt" file: 8.19kB [00:01, 5.05kB/s]
    Downloading "ColorChecker24_After_Nov2014.zip" file: 8.19kB [00:01, 6.52kB/s]
    Downloading "ColorChecker24_Before_Nov2014.zip" file: 8.19kB [00:01, 7.66kB/s]
    Downloading "ColorCheckerSG_After_Nov2014.zip" file: 8.19kB [00:01, 7.62kB/s]
    Downloading "ColorCheckerSG_Before_Nov2014.zip" file: 8.19kB [00:00, 9.39kB/s]
    Unpacking "/Users/kelsolaar/.colour-science/colour-datasets/3245895/dataset/ColorCheckerSG_Before_Nov2014.zip" archive...
    Unpacking "/Users/kelsolaar/.colour-science/colour-datasets/3245895/dataset/ColorCheckerSG_After_Nov2014.zip" archive...
    Unpacking "/Users/kelsolaar/.colour-science/colour-datasets/3245895/dataset/ColorChecker24_After_Nov2014.zip" archive...
    Unpacking "/Users/kelsolaar/.colour-science/colour-datasets/3245895/dataset/ColorChecker24_Before_Nov2014.zip" archive...
    odict_keys(['ColorChecker24 - After November 2014', 'ColorChecker24 - Before November 2014', 'ColorCheckerSG - After November 2014', 'ColorCheckerSG - Before November 2014'])

Alternatively, a dataset can be loaded by using its full title:
*New Color Specifications for ColorChecker SG and Classic Chart - X-Rite (2016)s*

.. code-block:: python

    print(colour_datasets.load("3245895").keys())

.. code-block:: text

    odict_keys(['ColorChecker24 - After November 2014', 'ColorChecker24 - Before November 2014', 'ColorCheckerSG - After November 2014', 'ColorCheckerSG - Before November 2014'])

User Guide
----------

Installation
^^^^^^^^^^^^

Primary Dependencies
~~~~~~~~~~~~~~~~~~~~

**Colour - Datasets** requires various dependencies in order to run:

- `python >= 3.10, < 3.14 <https://www.python.org/download/releases>`__
- `cachetools <https://pypi.org/project/cachetools>`__
- `colour-science >= 4.4 <https://pypi.org/project/colour-science>`__
- `imageio >= 2, < 3 <https://imageio.github.io>`__
- `numpy >= 1.24, < 3 <https://pypi.org/project/numpy>`__
- `scipy >= 1.10, < 2 <https://pypi.org/project/scipy>`__
- `tqdm <https://pypi.org/project/tqdm>`__
- `xlrd >=1.2, <2 <https://pypi.org/project/xlrd>`__

Pypi
~~~~

Once the dependencies are satisfied, **Colour - Datasets** can be installed from
the `Python Package Index <http://pypi.python.org/pypi/colour-datasets>`__ by
issuing this command in a shell::

    pip install --user colour-datasets

The overall development dependencies are installed as follows::

    pip install --user 'colour-datasets[development]'

Contributing
^^^^^^^^^^^^

If you would like to contribute to `Colour - Datasets <https://github.com/colour-science/colour-datasets>`__,
please refer to the following `Contributing <https://www.colour-science.org/contributing>`__
guide for `Colour <https://github.com/colour-science/colour>`__.

Bibliography
^^^^^^^^^^^^

The bibliography is available in the repository in
`BibTeX <https://github.com/colour-science/colour-datasets/blob/develop/BIBLIOGRAPHY.bib>`__
format.

API Reference
-------------

The main technical reference for `Colour - Datasets <https://github.com/colour-science/colour-datasets>`__
is the `API Reference <https://colour-datasets.readthedocs.io/en/latest/reference.html>`__.

Code of Conduct
---------------

The *Code of Conduct*, adapted from the `Contributor Covenant 1.4 <https://www.contributor-covenant.org/version/1/4/code-of-conduct.html>`__,
is available on the `Code of Conduct <https://www.colour-science.org/code-of-conduct>`__ page.

Contact & Social
----------------

The *Colour Developers* can be reached via different means:

- `Email <mailto:colour-developers@colour-science.org>`__
- `Facebook <https://www.facebook.com/python.colour.science>`__
- `Github Discussions <https://github.com/colour-science/colour-datasets/discussions>`__
- `Gitter <https://gitter.im/colour-science/colour>`__
- `Twitter <https://twitter.com/colour_science>`__

About
-----

| **Colour - Datasets** by Colour Developers
| Copyright 2019 Colour Developers – `colour-developers@colour-science.org <colour-developers@colour-science.org>`__
| This software is released under terms of BSD-3-Clause: https://opensource.org/licenses/BSD-3-Clause
| `https://github.com/colour-science/colour-datasets <https://github.com/colour-science/colour-datasets>`__
