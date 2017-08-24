import pytest

from web3 import Web3

from web3.utils.module_testing import (
    Web3ModuleTest,
    EthModuleTest,
)


@pytest.fixture
def web3():
    _web3 = Web3(Web3.EthereumTesterProvider())
    return _web3


class TestEthereumTesterWeb3Module(Web3ModuleTest):
    def _check_web3_clientVersion(self, client_version):
        assert client_version.startswith('TestRPC/')


class TestEthereumTesterEthModule(EthModuleTest):
    pass
