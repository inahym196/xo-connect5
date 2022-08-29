

import pytest
from fastapi.testclient import TestClient
from requests.models import Response
from starlette.exceptions import HTTPException
from xo_connect5.main import app
from xo_connect5.models.boards import Board, BoardStatus
from xo_connect5.models.users import Players, User

client = TestClient(app)


@pytest.fixture
def board():
    players = Players(first=User(name='first'), draw=User(name='draw'))
    board = Board(id=0, players=players, status=BoardStatus.STARTING)
    return board


def test_get_board(board: Board):
    response: Response = client.get('/api/v1/boards/0/')

    assert response.status_code == 200
    assert response.json() == board


def test_get_board_fail():
    response: Response = client.get('/api/v1/boards/1/')
    exception = HTTPException(status_code=404)

    assert response.status_code == exception.status_code
    assert response.json()['detail'] == exception.detail


def test_get_board_status(board: Board):
    response: Response = client.get('/api/v1/boards/0/status')
    response_str = response.json()

    assert response.status_code == 200
    assert response_str == board.status
