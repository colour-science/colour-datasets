Installation Guide
==================

Primary Dependencies
--------------------

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
----

Once the dependencies are satisfied, **Colour - Datasets** can be installed from
the `Python Package Index <http://pypi.python.org/pypi/colour-datasets>`__ by
issuing this command in a shell::

    pip install --user colour-datasets

The overall development dependencies are installed as follows::

    pip install --user 'colour-datasets[development]'
