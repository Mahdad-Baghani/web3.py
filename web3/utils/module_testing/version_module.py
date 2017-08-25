from eth_utils import (
    is_text,
)


class VersionModuleTest(object):
    def test_net_version(self, web3):
        version = web3.version.network

        assert is_text(version)
        assert version.isdigit()
