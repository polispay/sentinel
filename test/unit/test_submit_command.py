import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))


@pytest.fixture
def superblock():
    from models import Superblock
    # NOTE: no governance_object_id is set
    sbobj = Superblock(
        event_block_height=62500,
        payment_addresses='TXDSaTXerg68SCyLkWw2ERsqoTMWRBZiZQ|TDWz9KfMo55wzj2brbgaXxnDz28nAbdPcY',
        payment_amounts='5|3',
        proposal_hashes='e8a0057914a2e1964ae8a945c4723491caae2077a90a00a2aabee22b40081a87|d1ce73527d7cd6f2218f8ca893990bc7d5c6b9334791ce7973bfa22f155f826e',
    )

    return sbobj


def test_submit_command(superblock):
    cmd = superblock.get_submit_command()

    assert re.match(r'^gobject$', cmd[0]) is not None
    assert re.match(r'^submit$', cmd[1]) is not None
    assert re.match(r'^[\da-f]+$', cmd[2]) is not None
    assert re.match(r'^[\da-f]+$', cmd[3]) is not None
    assert re.match(r'^[\d]+$', cmd[4]) is not None
    assert re.match(r'^[\w-]+$', cmd[5]) is not None

    submit_time = cmd[4]

    gobject_command = ['gobject', 'submit', '0', '1', submit_time, '5b5b2274726967676572222c207b226576656e745f626c6f636b5f686569676874223a2036323530302c20227061796d656e745f616464726573736573223a20225458445361545865726736385343794c6b577732455273716f544d5752425a695a517c5444577a394b664d6f3535777a6a32627262676158786e447a32386e416264506359222c20227061796d656e745f616d6f756e7473223a2022357c33222c202270726f706f73616c5f686173686573223a2022653861303035373931346132653139363461653861393435633437323334393163616165323037376139306130306132616162656532326234303038316138377c64316365373335323764376364366632323138663863613839333939306263376435633662393333343739316365373937336266613232663135356638323665222c202274797065223a20327d5d5d']
    assert cmd == gobject_command
