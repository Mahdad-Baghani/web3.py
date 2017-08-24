import pytest

from web3 import Web3

from web3.utils.module_testing import (
    Web3ModuleTest,
)


@pytest.fixture
def web3():
    _web3 = Web3(Web3.EthereumTesterProvider())
    return _web3


class TestEthereumTester(Web3ModuleTest):
    pass
