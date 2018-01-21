import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from polisd import PolisDaemon
from polis_config import PolisConfig


def test_polisd():
    config_text = PolisConfig.slurp_config_file(config.polis_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'000009701eb781a8113b1af1d814e2f060f6408a2c990db291bc5108a1345c1e'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'000000ca90aac9a933dd4cfc07d8e6731e2054a137ba88c4848d21ad7ac289c5'

    creds = PolisConfig.get_rpc_creds(config_text, network)
    polisd = PolisDaemon(**creds)
    assert polisd.rpc_command is not None

    assert hasattr(polisd, 'rpc_connection')

    # Polis testnet block 0 hash == 000000ca90aac9a933dd4cfc07d8e6731e2054a137ba88c4848d21ad7ac289c5
    # test commands without arguments
    info = polisd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert polisd.rpc_command('getblockhash', 0) == genesis_hash
