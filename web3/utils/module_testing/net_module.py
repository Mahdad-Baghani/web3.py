from eth_utils import (
    is_text,
)


class NetModuleTest(object):
    def test_net_version(self, web3):
        version = web3.net.version

        assert is_text(version)
        assert version.isdigit()
