import pytest


@pytest.fixture
def coinbase():
    return '0xdc544d1aa88ff8bbd2f2aec754b1f1e99e1812fd'


@pytest.fixture
def private_key():
    return '0x58d23b55bc9cdce1f18c2500f40ff4ab7245df9a89505e9b1fa4851f623d241d'


KEYFILE = '{"address":"dc544d1aa88ff8bbd2f2aec754b1f1e99e1812fd","crypto":{"cipher":"aes-128-ctr","ciphertext":"52e06bc9397ea9fa2f0dae8de2b3e8116e92a2ecca9ad5ff0061d1c449704e98","cipherparams":{"iv":"aa5d0a5370ef65395c1a6607af857124"},"kdf":"scrypt","kdfparams":{"dklen":32,"n":262144,"p":1,"r":8,"salt":"9fdf0764eb3645ffc184e166537f6fe70516bf0e34dc7311dea21f100f0c9263"},"mac":"4e0b51f42b865c15c485f4faefdd1f01a38637e5247f8c75ffe6a8c0eba856f6"},"id":"5a6124e0-10f1-4c1c-ae3e-d903eacb740a","version":3}'  # noqa: E501
