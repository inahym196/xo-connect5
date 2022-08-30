

import pytest
from fastapi.testclient import TestClient
from requests.models import Response
from xo_connect5.main import app
from xo_connect5.models.boards import Board, BoardStatus
from xo_connect5.models.pieces import Pieces, PieceType
from xo_connect5.models.users import Players, User

client = TestClient(app)


@pytest.fixture
def pieces():
    pieces = [[PieceType.NONE for j in range(10)] for i in range(10)]
    return pieces


@pytest.fixture
def board():
    players = Players(first=User(name='first'), draw=User(name='draw'))
    board = Board(id=0, players=players, status=BoardStatus.STARTING)
    return board


def test_get_pieces(pieces: Pieces):
    response: Response = client.get('/api/v1/boards/0/pieces/')

    assert response.status_code == 200
    assert response.json() == pieces


def test_put_pieces_fail_no_user():
    params = {'raw': 0, 'column': 0}
    data = {
        'user': {'name': 'first'},
        'order': {'type': 'first'}
    }
    response: Response = client.patch('/api/v1/boards/0/pieces/', params=params, json=data)

    assert response.status_code == 400
    assert response.json() == {'detail': 'There is no user on board'}
