

import pytest
from fastapi.exceptions import HTTPException
from fastapi.testclient import TestClient
from requests.models import Response
from xo_connect5.main import app
from xo_connect5.models.boards import Board, Boards, BoardStatus
from xo_connect5.models.users import Players, User

client = TestClient(app)


@pytest.fixture
def init_board():
    _ = client.delete('/api/v1/boards/0')


@pytest.fixture
def ready_board():
    ...


class TestBoards:

    def test_get_boards(self):
        response: Response = client.get('/api/v1/boards/')
        _players = Players(first=User(name='first'), draw=User(name='draw'))
        _board = Board(id=0, players=_players, status=BoardStatus.STARTING)
        boards = Boards(items=[_board])

        assert response.status_code == 200
        assert response.json()['items'] == boards.items

    def test_post_boards(self):
        response: Response = client.post('/api/v1/boards/')
        boards = HTTPException(status_code=409)
        assert response.status_code == boards.status_code
        assert response.json()['detail'] == boards.detail


class TestBoard:

    def test_get_board(self):
        response: Response = client.get('/api/v1/boards/0/')
        players = Players(first=User(name='first'), draw=User(name='draw'))
        board = Board(id=0, players=players, status=BoardStatus.STARTING)

        assert response.status_code == 200
        assert response.json() == board

    def test_get_board_fail(self):
        response: Response = client.get('/api/v1/boards/1/')
        exception = HTTPException(status_code=404)

        assert response.status_code == exception.status_code
        assert response.json()['detail'] == exception.detail

    def test_get_board_status(self):
        response: Response = client.get('/api/v1/boards/0/status')
        players = Players(first=User(name='first'), draw=User(name='draw'))
        board = Board(id=0, players=players, status=BoardStatus.STARTING)

        assert response.status_code == 200
        assert response.json() == board.status

    def test_delete_board(self):
        response: Response = client.delete('/api/v1/boards/0')
        exception = HTTPException(status_code=204)

        assert response.status_code == exception.status_code
        assert response._content == b''

    def test_post_board(self):
        response: Response = client.post('/api/v1/boards/')
        players = Players(first=User(name='first'), draw=User(name='draw'))
        board = Board(id=0, players=players, status=BoardStatus.STARTING)

        assert response.status_code == 200
        assert response.json()['id'] == board.id
        assert response.json()['status'] == BoardStatus.WAITING
        assert response.json()['pieces'] == board.pieces
        assert response.json()['players'] == {'first': None, 'draw': None}
        assert response.json()['round'] == board.round
