from eth_utils import (
    is_address,
    is_text,
    is_boolean,
    is_dict,
    is_integer,
    is_list_like,
)


class EthModuleTest(object):
    def test_eth_protocolVersion(self, web3):
        protocol_version = web3.version.ethereum

        assert is_text(protocol_version)
        assert protocol_version.isdigit()

    def test_eth_syncing(self, web3):
        syncing = web3.eth.syncing

        assert is_boolean(syncing) or is_dict(syncing)

        if is_boolean(syncing):
            assert syncing is False
        elif is_dict(syncing):
            assert 'startingBlock' in syncing
            assert 'currentBlock' in syncing
            assert 'highestBlock' in syncing

            assert is_integer(syncing['startingBlock'])
            assert is_integer(syncing['currentBlock'])
            assert is_integer(syncing['highestBlock'])

    def test_eth_coinbase(self, web3):
        coinbase = web3.eth.coinbase
        assert is_address(coinbase)

    def test_eth_mining(self, web3):
        mining = web3.eth.mining
        assert is_boolean(mining)

    def test_eth_hashrate(self, web3):
        hashrate = web3.eth.hashrate
        assert is_integer(hashrate)
        assert hashrate >= 0

    def test_eth_gasPrice(self, web3):
        gas_price = web3.eth.gasPrice
        assert is_integer(gas_price)
        assert gas_price > 0

    def test_eth_accounts(self, web3):
        accounts = web3.eth.accounts
        assert is_list_like(accounts)
        assert len(accounts) != 0
        assert all((
            is_address(account)
            for account
            in accounts
        ))
        assert web3.eth.coinbase in accounts

    def test_eth_blockNumber(self, web3):
        block_number = web3.eth.blockNumber
        assert is_integer(block_number)
        assert block_number >= 0

    def test_eth_getBalance(self, web3):
        coinbase = web3.eth.coinbase
        balance = web3.eth.getBalance(coinbase)

        assert is_integer(balance)
        assert balance >= 0

    def test_eth_getStorageAt(self, web3):
        # TODO: implement deployed contracts
        pass

    def test_eth_getTransactionCount(self, web3):
        coinbase = web3.eth.coinbase
        transaction_count = web3.eth.getTransactionCount(coinbase)

        assert is_integer(transaction_count)
        assert transaction_count >= 0

    def test_eth_getBlockTransactionCountByHash(self, web3, empty_block):
        transaction_count = web3.eth.getBlockTransactionCount(empty_block['hash'])

        assert is_integer(transaction_count)
        assert transaction_count == 0

    def test_eth_getBlockTransactionCountByNumber(self, web3, empty_block):
        transaction_count = web3.eth.getBlockTransactionCount(empty_block['number'])

        assert is_integer(transaction_count)
        assert transaction_count == 0

    def test_eth_getUncleCountByBlockHash(self, web3, empty_block):
        uncle_count = web3.eth.getUncleCount(empty_block['hash'])

        assert is_integer(uncle_count)
        assert uncle_count == 0

    def test_eth_getUncleCountByBlockNumber(self, web3, empty_block):
        uncle_count = web3.eth.getUncleCount(empty_block['number'])

        assert is_integer(uncle_count)
        assert uncle_count == 0
