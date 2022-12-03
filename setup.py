"""
Colour - Datasets - Setup
=========================
"""

import codecs
from setuptools import setup

packages = [
    "colour_datasets",
    "colour_datasets.examples",
    "colour_datasets.loaders",
    "colour_datasets.loaders.tests",
    "colour_datasets.records",
    "colour_datasets.records.tests",
    "colour_datasets.utilities",
    "colour_datasets.utilities.tests",
]

package_data = {
    "": ["*"],
    "colour_datasets.loaders.tests": ["resources/*"],
    "colour_datasets.utilities.tests": ["resources/*"],
}

install_requires = [
    "cachetools",
    "colour-science>=0.4.2",
    "imageio>=2,<3",
    "numpy>=1.20,<2",
    "opencv-python>=4,<5",
    "scipy>=1.7,<2",
    "tqdm",
    "typing-extensions>=4,<5",
    "xlrd>=1.2,<2",
]

extras_require = {
    "development": [
        "biblib-simple",
        "black",
        "blackdoc",
        "coverage!=6.3",
        "coveralls",
        "flake8",
        "flynt",
        "invoke",
        "mypy",
        "pre-commit",
        "pydata-sphinx-theme",
        "pydocstyle",
        "pytest",
        "pytest-cov",
        "pyupgrade",
        "restructuredtext-lint",
        "sphinx>=4,<5",
        "sphinxcontrib-bibtex",
        "toml",
        "twine",
    ],
    "read-the-docs": ["pydata-sphinx-theme", "sphinxcontrib-bibtex"],
}

setup(
    name="colour-datasets",
    version="0.2.1",
    description="Colour science datasets for use with Colour",
    long_description=codecs.open("README.rst", encoding="utf8").read(),
    author="Colour Developers",
    author_email="colour-developers@colour-science.org",
    maintainer="Colour Developers",
    maintainer_email="colour-developers@colour-science.org",
    url="https://www.colour-science.org/",
    packages=packages,
    package_data=package_data,
    install_requires=install_requires,
    extras_require=extras_require,
    python_requires=">=3.9,<3.12",
)
