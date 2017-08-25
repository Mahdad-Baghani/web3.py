import functools

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
    contract_factory = web3.eth.contract(abi=MATH_ABI, bytecode=MATH_BYTECODE)
    return contract_factory


@pytest.fixture(scope="session")
def math_contract_deploy_txn_hash(math_contract_factory):
    deploy_txn_hash = math_contract_factory.deploy()
    return deploy_txn_hash


@pytest.fixture(scope="session")
def math_contract(web3, math_contract_factory, math_contract_deploy_txn_hash):
    deploy_receipt = web3.eth.getTransactionReceipt(math_contract_deploy_txn_hash)
    assert is_dict(deploy_receipt)
    contract_address = deploy_receipt['contractAddress']
    assert is_address(contract_address)
    return math_contract_factory(contract_address)


@pytest.fixture(scope="session")
def empty_block(web3):
    web3.testing.mine()
    block = web3.eth.getBlock("latest")
    assert not block['transactions']
    return block


@pytest.fixture(scope="session")
def block_with_txn(web3):
    txn_hash = web3.eth.sendTransaction({
        'from': web3.eth.coinbase,
        'to': web3.eth.coinbase,
        'value': 1,
        'gas': 21000,
        'gas_price': 1,
    })
    txn = web3.eth.getTransaction(txn_hash)
    block = web3.eth.getBlock(txn['blockNumber'])
    return block


@pytest.fixture
def unlocked_account(web3):
    return web3.eth.coinbase


class TestEthereumTesterWeb3Module(Web3ModuleTest):
    def _check_web3_clientVersion(self, client_version):
        assert client_version.startswith('TestRPC/')


def not_implemented(method):
    @functools.wraps(method)
    def inner(*args, **kwargs):
        with pytest.raises(AttributeError):
            method(*args, **kwargs)
    return inner


class TestEthereumTesterEthModule(EthModuleTest):
    #
    # Eth-Testrpc doesn't implement a bunch of methods.
    #
    test_eth_hashrate = not_implemented(EthModuleTest.test_eth_hashrate)

    test_eth_getBlockTransactionCountByHash_empty_block = not_implemented(
        EthModuleTest.test_eth_getBlockTransactionCountByHash_empty_block,
    )
    test_eth_getBlockTransactionCountByNumber_empty_block = not_implemented(
        EthModuleTest.test_eth_getBlockTransactionCountByNumber_empty_block,
    )

    test_eth_getBlockTransactionCountByHash_block_with_txn = not_implemented(
        EthModuleTest.test_eth_getBlockTransactionCountByHash_block_with_txn,
    )
    test_eth_getBlockTransactionCountByNumber_block_with_txn = not_implemented(
        EthModuleTest.test_eth_getBlockTransactionCountByNumber_block_with_txn,
    )

    test_eth_getUncleCountByBlockHash = not_implemented(
        EthModuleTest.test_eth_getUncleCountByBlockHash,
    )
    test_eth_getUncleCountByBlockNumber = not_implemented(
        EthModuleTest.test_eth_getUncleCountByBlockNumber,
    )

    test_eth_sign = not_implemented(
        EthModuleTest.test_eth_sign,
    )


class TestEthereumTesterVersionModule(VersionModuleTest):
    pass


class TestEthereumTesterNetModule(NetModuleTest):
    pass
