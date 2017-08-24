from eth_utils import (
    is_address,
)


class EthModuleTest(object):
    def test_eth_coinbase(self, web3):
        coinbase = web3.eth.coinbase
        assert is_address(coinbase)
