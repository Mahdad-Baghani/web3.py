import pytest


class Web3ModuleTest(object):
    @pytest.mark.parametrize(
        'params,expected',
        (
            (
                ['0x68656c6c6f20776f726c64'],
                '0x47173285a8d7341e5e972fc677286384f802f8ef42a5ec5f03bbfa254cb01fad',
            ),
        ),
    )
    def test_web3_sha3(self, web3, params, expected):
        actual = web3.sha3(*params)
        assert actual == expected

    def test_web3_clientVersion(self, web3):
        client_version = web3.version.node
        self._check_web3_clientVersion(client_version)

    def _check_web3_clientVersion(self, client_version):
        raise NotImplementedError("Must be implemented by subclasses")
