import pytest

from eth_utils import (
    is_address,
    is_dict,
)

from web3 import Web3

from web3.utils.module_testing import (
    EthModuleTest,
    NetModuleTest,
    VersionModuleTest,
    Web3ModuleTest,
)
from web3.utils.module_testing.math_contract import (
    MATH_BYTECODE,
    MATH_ABI,
)


@pytest.fixture(scope="session")
def web3():
    _web3 = Web3(Web3.EthereumTesterProvider())
    return _web3


@pytest.fixture(scope="session")
def math_contract_factory(web3):
    contract_factory = web3.eth.contract(abi=MATH_ABI, code=MATH_BYTECODE)
    return contract_factory


@pytest.fixture(scope="session")
def math_contract_deploy_txn_hash(math_contract_factory):
    deploy_txn_hash = math_contract_factory.deploy()
    return deploy_txn_hash


@pytest.fixture(scope="session")
def math_contract(web3, math_contract_factory, math_contract_deploy_txn_hash):
    deploy_txn = web3.eth.getTransactionReceipt(math_contract_deploy_txn_hash)
    assert is_dict(deploy_txn)
    contract_address = deploy_txn['contractAddress']
    assert is_address(contract_address)
    return math_contract_factory(contract_address)


@pytest.fixture(scope="session")
def empty_block(web3):
    web3.testing.mine()
    block = web3.eth.getBlock("latest")
    assert not block['transactions']
    return block


class TestEthereumTesterWeb3Module(Web3ModuleTest):
    def _check_web3_clientVersion(self, client_version):
        assert client_version.startswith('TestRPC/')


class TestEthereumTesterEthModule(EthModuleTest):
    #
    # Eth-Testrpc doesn't implement a bunch of methods.
    #
    def test_eth_hashrate(self, web3):
        with pytest.raises(AttributeError):
            super(TestEthereumTesterEthModule, self).test_eth_hashrate(web3)

    def test_eth_getBlockTransactionCountByHash(self, web3, empty_block):
        with pytest.raises(AttributeError):
            super(TestEthereumTesterEthModule, self).test_eth_getBlockTransactionCountByHash(
                web3,
                empty_block,
            )

    def test_eth_getBlockTransactionCountByNumber(self, web3, empty_block):
        with pytest.raises(AttributeError):
            super(TestEthereumTesterEthModule, self).test_eth_getBlockTransactionCountByNumber(
                web3,
                empty_block,
            )

    def test_eth_getUncleCountByBlockHash(self, web3, empty_block):
        with pytest.raises(AttributeError):
            super(TestEthereumTesterEthModule, self).test_eth_getUncleCountByBlockHash(
                web3,
                empty_block,
            )

    def test_eth_getUncleCountByBlockNumber(self, web3, empty_block):
        with pytest.raises(AttributeError):
            super(TestEthereumTesterEthModule, self).test_eth_getUncleCountByBlockNumber(
                web3,
                empty_block,
            )


class TestEthereumTesterVersionModule(VersionModuleTest):
    pass


class TestEthereumTesterNetModule(NetModuleTest):
    pass
