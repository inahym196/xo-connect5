import pytest
from xo_connect5.models.users import Order, OrderType, User

from tests import client

pytest.register_assert_rewrite('test.helpers')


@pytest.fixture(autouse=True)
def no_board():
    client.delete('/api/v1/boards/0')


@pytest.fixture
def init_board():
    client.post('/api/v1/boards/')


players_on_board = [
    (User(name='first'), Order(type=OrderType.FIRST)),
    (User(name='draw'), Order(type=OrderType.DRAW))
]


@pytest.fixture
def starting_board(init_board):
    client.delete('/api/v1/boards/0')
    client.post('/api/v1/boards/')
    for user, order in players_on_board:
        data = {'user': user.dict(), 'order': order.dict()}
        client.put('/api/v1/boards/0/players/', json=data)
