# -*- coding: utf-8 -*-
import codecs
from setuptools import setup

packages = \
['colour_datasets',
 'colour_datasets.examples',
 'colour_datasets.loaders',
 'colour_datasets.loaders.tests',
 'colour_datasets.records',
 'colour_datasets.records.tests',
 'colour_datasets.utilities',
 'colour_datasets.utilities.tests']

package_data = \
{'': ['*'],
 'colour_datasets.loaders.tests': ['resources/*'],
 'colour_datasets.utilities.tests': ['resources/*']}

install_requires = \
['cachetools', 'colour-science>=0.3.14,<0.4.0', 'tqdm', 'xlrd']

extras_require = \
{'development': ['biblib-simple',
                 'coverage',
                 'coveralls',
                 'flake8',
                 'invoke',
                 'mock',
                 'nose',
                 'pre-commit',
                 'pytest',
                 'restructuredtext-lint',
                 'sphinx',
                 'sphinx_rtd_theme',
                 'sphinxcontrib-bibtex',
                 'toml',
                 'twine',
                 'yapf==0.23'],
 'read-the-docs': ['mock', 'numpy', 'sphinxcontrib-bibtex']}

    setup(
    name='colour-datasets',
    version='0.1.0',
    description='Colour science datasets for use with Colour',
    long_description=codecs.open('README.rst', encoding='utf8').read(),
    author='Colour Developers',
    author_email='colour-developers@colour-science.org',
    maintainer='Colour Developers',
    maintainer_email='colour-developers@colour-science.org',
    url='https://www.colour-science.org/',
    packages=packages,
    package_data=package_data,
    install_requires=install_requires,
    extras_require=extras_require,
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    )
    