
from typing import Any

import pytest
from requests.models import Response

from tests import client

pytest.register_assert_rewrite('test.helpers')

BoardFixture = tuple[Response, dict[str, Any]]


@pytest.fixture(autouse=True)
def no_board() -> list:
    client.delete('/api/v1/boards/0/')
    expected = []
    return expected


@pytest.fixture
def init_board() -> BoardFixture:
    response = client.post('/api/v1/boards/')
    expected = {
        'id': 0,
        'pieces': [['_' for j in range(10)] for i in range(10)],
        'turn': 0,
        'status': 'waiting',
        'players': {'first': None, 'draw': None},
    }
    return response, expected


players_on_board = [
    ({'name': 'first'}, {'type': 'first'}),
    ({'name': 'draw'}, {'type': 'draw'}),
]


@pytest.fixture
def waiting_draw_user_board(init_board: BoardFixture) -> BoardFixture:
    _, init_board_expected_json = init_board
    user, order = {'name': 'first'}, {'type': 'first'}
    data = {'user': user, 'order': order}
    response = client.put('/api/v1/boards/0/players/', json=data)
    expected = init_board_expected_json | {'players': {order['type']: user}}
    return response, expected


@pytest.fixture
def starting_board(init_board: BoardFixture) -> dict[str, Any]:
    _, init_board_expected = init_board
    players = {}
    for user, order in players_on_board:
        data = {'user': user, 'order': order}
        client.put('/api/v1/boards/0/players/', json=data)
        players |= {order['type']: user}
    expected = init_board_expected | {'players': players, 'status': 'starting'}
    return expected
