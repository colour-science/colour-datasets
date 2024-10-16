"""Define the unit tests for the :mod:`colour_datasets.loaders.dyer2017` module."""


import numpy as np
from colour.constants import TOLERANCE_ABSOLUTE_TESTS

from colour_datasets.loaders import DatasetLoader_Dyer2017, build_Dyer2017

__author__ = "Colour Developers"
__copyright__ = "Copyright 2019 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestDatasetLoader_Dyer2017",
    "TestBuildDyer2017",
]


class TestDatasetLoader_Dyer2017:
    """
    Define :class:`colour_datasets.loaders.dyer2017.DatasetLoader_Dyer2017`
    class unit tests methods.
    """

    def test_required_attributes(self):
        """Test the presence of required attributes."""

        required_attributes = ("ID",)

        for attribute in required_attributes:
            assert attribute in dir(DatasetLoader_Dyer2017)

    def test_required_methods(self):
        """Test the presence of required methods."""

        required_methods = ("__init__", "load")

        for method in required_methods:
            assert method in dir(DatasetLoader_Dyer2017)

    def test_load(self):
        """
        Test :func:`colour_datasets.loaders.dyer2017.DatasetLoader_Dyer2017.\
load` method.
        """

        dataset = DatasetLoader_Dyer2017()
        assert sorted(dataset.load().keys()) == [
            "camera",
            "cmf",
            "illuminant",
            "training",
        ]

        np.testing.assert_allclose(
            dataset.load()["camera"]["canon eos 5d mark ii"][555],
            np.array(
                [
                    0.165200000000000,
                    0.802800000000000,
                    0.028300000000000,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )
        np.testing.assert_allclose(
            dataset.load()["cmf"]["cie-1931"][555],
            np.array(
                [
                    0.512050100000000,
                    1.000000000000000,
                    0.005749999000000,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )
        np.testing.assert_allclose(
            dataset.load()["illuminant"]["iso7589"][555],
            np.array([0.485000000000000]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )
        np.testing.assert_allclose(
            dataset.load()["training"]["190-patch"][555],
            np.array(
                [
                    0.016543747000000,
                    0.089454049000000,
                    0.775860114000000,
                    0.199500000000000,
                    0.589294177000000,
                    0.426983879000000,
                    0.299315241000000,
                    0.195307174000000,
                    0.113005514000000,
                    0.065695622000000,
                    0.030550537000000,
                    0.185923210000000,
                    0.138998782000000,
                    0.253323493000000,
                    0.116890395000000,
                    0.059878320000000,
                    0.386424591000000,
                    0.242522104000000,
                    0.042793898000000,
                    0.039108407000000,
                    0.340616303000000,
                    0.109391839000000,
                    0.024575114000000,
                    0.013437553000000,
                    0.165550372000000,
                    0.044162979000000,
                    0.038362653000000,
                    0.050943800000000,
                    0.060706606000000,
                    0.017150009000000,
                    0.030958883000000,
                    0.294163695000000,
                    0.094815764000000,
                    0.013631268000000,
                    0.011556292000000,
                    0.102712966000000,
                    0.014063110000000,
                    0.088584881000000,
                    0.019506551000000,
                    0.049543471000000,
                    0.216543615000000,
                    0.148685793000000,
                    0.426425448000000,
                    0.066590491000000,
                    0.185951857000000,
                    0.161431933000000,
                    0.046959872000000,
                    0.337386898000000,
                    0.044950244000000,
                    0.186142255000000,
                    0.217803413000000,
                    0.176242473000000,
                    0.180234723000000,
                    0.573066803000000,
                    0.396281106000000,
                    0.130612404000000,
                    0.489232284000000,
                    0.086611731000000,
                    0.482820917000000,
                    0.285489705000000,
                    0.390752390000000,
                    0.553103082000000,
                    0.761045838000000,
                    0.448310405000000,
                    0.751459057000000,
                    0.296973364000000,
                    0.845515046000000,
                    0.600851468000000,
                    0.790979892000000,
                    0.116890676000000,
                    0.471334928000000,
                    0.796627165000000,
                    0.318975867000000,
                    0.365398300000000,
                    0.663541772000000,
                    0.243604910000000,
                    0.817055901000000,
                    0.746637464000000,
                    0.142703616000000,
                    0.060728679000000,
                    0.244645070000000,
                    0.525056690000000,
                    0.125884506000000,
                    0.159583709000000,
                    0.333025306000000,
                    0.099145922000000,
                    0.115960832000000,
                    0.142817663000000,
                    0.105357260000000,
                    0.154603755000000,
                    0.136542750000000,
                    0.235944300000000,
                    0.322853029000000,
                    0.636786365000000,
                    0.478067566000000,
                    0.357385246000000,
                    0.233766382000000,
                    0.313229098000000,
                    0.470989753000000,
                    0.219620176000000,
                    0.087619811000000,
                    0.181083141000000,
                    0.237307524000000,
                    0.134183724000000,
                    0.052929690000000,
                    0.335421880000000,
                    0.355101839000000,
                    0.051487691000000,
                    0.225285679000000,
                    0.208450311000000,
                    0.137336941000000,
                    0.069794973000000,
                    0.311496347000000,
                    0.655141187000000,
                    0.092340917000000,
                    0.446097178000000,
                    0.595113151000000,
                    0.051742762000000,
                    0.308310085000000,
                    0.218221361000000,
                    0.459776672000000,
                    0.483055996000000,
                    0.209489271000000,
                    0.270752508000000,
                    0.581475704000000,
                    0.150634167000000,
                    0.162358582000000,
                    0.576733107000000,
                    0.327650514000000,
                    0.341401404000000,
                    0.153771821000000,
                    0.402136399000000,
                    0.079694635000000,
                    0.068407983000000,
                    0.534616880000000,
                    0.183116936000000,
                    0.171525933000000,
                    0.037855717000000,
                    0.168182056000000,
                    0.559997393000000,
                    0.144518923000000,
                    0.108677750000000,
                    0.075848465000000,
                    0.106230967000000,
                    0.271748990000000,
                    0.108267178000000,
                    0.363043033000000,
                    0.041006456000000,
                    0.031950058000000,
                    0.173380906000000,
                    0.359966187000000,
                    0.044712750000000,
                    0.100602091000000,
                    0.175245406000000,
                    0.061063126000000,
                    0.258613296000000,
                    0.026866789000000,
                    0.197704679000000,
                    0.543435154000000,
                    0.113192419000000,
                    0.267300817000000,
                    0.135820481000000,
                    0.154000795000000,
                    0.045469997000000,
                    0.408044588000000,
                    0.011999794000000,
                    0.047949059000000,
                    0.052502489000000,
                    0.065332167000000,
                    0.151156617000000,
                    0.132535937000000,
                    0.037475628000000,
                    0.138033009000000,
                    0.210685187000000,
                    0.265259355000000,
                    0.523381186000000,
                    0.105874515000000,
                    0.164640208000000,
                    0.109354860000000,
                    0.437779019000000,
                    0.024237616000000,
                    0.144939306000000,
                    0.297763330000000,
                    0.178469229000000,
                    0.312304014000000,
                    0.327352013000000,
                    0.026469427000000,
                    0.431901773000000,
                    0.015418874000000,
                    0.158126080000000,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )


class TestBuildDyer2017:
    """
    Define :func:`colour_datasets.loaders.dyer2017.build_Dyer2017`
    definition unit tests methods.
    """

    def test_build_Dyer2017(self):
        """
        Test :func:`colour_datasets.loaders.dyer2017.build_Dyer2017`
        definition.
        """

        assert build_Dyer2017() is build_Dyer2017()
