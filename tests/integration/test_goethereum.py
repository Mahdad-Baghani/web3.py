import json
import os
import signal
import socket
import subprocess
import time
import tempfile

import pytest

from eth_utils import (
    to_wei,
    remove_0x_prefix,
)

from web3 import Web3

from web3.utils.module_testing import (
    Web3ModuleTest,
)


@pytest.fixture(scope='session')
def coinbase():
    return '0xdc544d1aa88ff8bbd2f2aec754b1f1e99e1812fd'


@pytest.fixture(scope='session')
def private_key():
    return '0x58d23b55bc9cdce1f18c2500f40ff4ab7245df9a89505e9b1fa4851f623d241d'


KEYFILE_DATA = '{"address":"dc544d1aa88ff8bbd2f2aec754b1f1e99e1812fd","crypto":{"cipher":"aes-128-ctr","ciphertext":"52e06bc9397ea9fa2f0dae8de2b3e8116e92a2ecca9ad5ff0061d1c449704e98","cipherparams":{"iv":"aa5d0a5370ef65395c1a6607af857124"},"kdf":"scrypt","kdfparams":{"dklen":32,"n":262144,"p":1,"r":8,"salt":"9fdf0764eb3645ffc184e166537f6fe70516bf0e34dc7311dea21f100f0c9263"},"mac":"4e0b51f42b865c15c485f4faefdd1f01a38637e5247f8c75ffe6a8c0eba856f6"},"id":"5a6124e0-10f1-4c1c-ae3e-d903eacb740a","version":3}'  # noqa: E501

KEYFILE_PW = 'web3py-test'


@pytest.fixture(scope='session')
def datadir(tmpdir_factory):
    _datadir = tmpdir_factory.mktemp('geth-datadir')
    return _datadir


@pytest.fixture(scope='session')
def keystore(datadir):
    _keystore = datadir.mkdir('keystore')
    return _keystore


@pytest.fixture(scope='session')
def keyfile(keystore):
    _keyfile = keystore.join('UTC--2017-08-24T19-42-47.517572178Z--dc544d1aa88ff8bbd2f2aec754b1f1e99e1812fd')
    _keyfile.write(KEYFILE_DATA)
    return _keyfile


@pytest.fixture(scope='session')
def genesis_data(coinbase):
    return {
        "nonce": "0xdeadbeefdeadbeef",
        "timestamp": "0x0",
        "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",  # noqa: E501
        "extraData": "0x7765623370792d746573742d636861696e",
        "gasLimit": "0x47d5cc",
        "difficulty": "0x01",
        "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",  # noqa: E501
        "coinbase": "0x3333333333333333333333333333333333333333",
        "alloc": {
            remove_0x_prefix(coinbase): {
                'balance': str(to_wei(1000000000, 'ether')),
            },
        },
        "config": {
            "chainId": 131277322940537,  # the string 'web3py' as an integer
            "homesteadBlock": 0,
            "eip155Block": 0,
            "eip158Block": 0
        },
    }


@pytest.fixture(scope='session')
def genesis_file(datadir, genesis_data):
    _genesis_file = datadir.join('genesis.json')
    _genesis_file.write(json.dumps(genesis_data))
    return _genesis_file


@pytest.fixture(scope='session')
def geth_ipc_path(datadir):
    geth_ipc_dir_path = tempfile.mkdtemp()
    _geth_ipc_path = os.path.join(geth_ipc_dir_path, 'geth.ipc')
    yield _geth_ipc_path

    if os.path.exists(_geth_ipc_path):
        os.remove(_geth_ipc_path)


class Timeout(Exception):
    pass


def wait_for_popen(proc, timeout):
    start = time.time()
    try:
        while time.time() < start + timeout:
            if proc.poll() is None:
                time.sleep(0.1)
            else:
                break
    except Timeout:
        pass


def kill_proc_gracefully(proc):
    if proc.poll() is None:
        proc.send_signal(signal.SIGINT)
        wait_for_popen(proc, 13)

    if proc.poll() is None:
        proc.terminate()
        wait_for_popen(proc, 5)

    if proc.poll() is None:
        proc.kill()
        wait_for_popen(proc, 2)


@pytest.fixture(scope='session')
def geth_process(datadir, genesis_file, keyfile, geth_ipc_path):
    geth_binary = os.environ.get('GETH_BINARY', 'geth')
    init_datadir_command = (
        geth_binary,
        'init',
        '--datadir', str(datadir),
        str(genesis_file),
    )
    subprocess.check_output(init_datadir_command)

    # keystore = datadir.mkdir('keystore')
    run_geth_command = (
        geth_binary,
        '--datadir', str(datadir),
        '--ipcpath', geth_ipc_path,
        '--nodiscover',
        '--mine',
        '--minerthreads', '1',
    )
    proc = subprocess.Popen(
        run_geth_command,
        #stdin=subprocess.PIPE,
        #stdout=subprocess.PIPE,
        #stderr=subprocess.PIPE,
        bufsize=1,
    )
    yield proc

    kill_proc_gracefully(proc)


def wait_for_socket(ipc_path, timeout=30):
    start = time.time()
    while time.time() < start + timeout:
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(ipc_path)
            sock.settimeout(timeout)
        except socket.error:
            time.sleep(0.1)
        else:
            break


@pytest.fixture
def web3(geth_process, geth_ipc_path):
    wait_for_socket(geth_ipc_path)
    _web3 = Web3(Web3.IPCProvider(geth_ipc_path))
    return _web3


class TestGoEthereum(Web3ModuleTest):
    pass
