import pytest


class BaseWeb3ModuleTest(object):
    @pytest.parametrize(
        'params,expected',
        (
            ['0x68656c6c6f20776f726c64'],
            '0x47173285a8d7341e5e972fc677286384f802f8ef42a5ec5f03bbfa254cb01fad',
        ),
    )
    def test_sha3(self, web3, params, expected):
        actual = web3.sha3(*params)
        assert actual == expected
