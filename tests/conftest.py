
import pytest

from tests import client

pytest.register_assert_rewrite('test.helpers')


@pytest.fixture(autouse=True)
def no_board():
    client.delete('/api/v1/boards/0')


@pytest.fixture
def init_board():
    client.post('/api/v1/boards/')
    return {
        'id': 0,
        'pieces': [['_' for j in range(10)] for i in range(10)],
        'round': 0,
        'status': 'waiting',
        'players': {'first': None, 'draw': None},
    }


players_on_board = [
    ({'name': 'first'}, {'type': 'first'}),
    ({'name': 'draw'}, {'type': 'draw'}),
]


@pytest.fixture
def starting_board(init_board):
    for user, order in players_on_board:
        data = {'user': user, 'order': order}
        client.put('/api/v1/boards/0/players/', json=data)
    return {
        'id': 0,
        'pieces': [['_' for j in range(10)] for i in range(10)],
        'round': 0,
        'status': 'starting',
        'players': {'first': {'name': 'first'}, 'draw': {'name': 'draw'}},
    }
