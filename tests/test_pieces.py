

import pytest
from requests.models import Response
from xo_connect5.models.boards import Board, BoardStatus
from xo_connect5.models.pieces import Pieces, PieceType
from xo_connect5.models.users import Players, User

from tests import client, http_exception_404


@pytest.fixture
def pieces():
    pieces = [[PieceType.NONE for j in range(10)] for i in range(10)]
    return pieces


@pytest.fixture
def board():
    players = Players(first=User(name='first'), draw=User(name='draw'))
    board = Board(id=0, players=players, status=BoardStatus.STARTING)
    return board


class TestPieces:

    def test_get_pieces_when_no_board(self, no_board):
        response: Response = client.get('/api/v1/boards/0/pieces/')

        assert response.status_code == http_exception_404.status_code
        assert response.json()['detail'] == http_exception_404.detail

    def test_get_pieces_when_init_board(self, init_board):
        response: Response = client.get('/api/v1/boards/0/pieces/')
        pieces: Pieces = [[PieceType.NONE for j in range(10)] for i in range(10)]

        assert response.json() == pieces

    def test_put_pieces_when_no_board(self, no_board):
        params = {'raw': 0, 'column': 0}
        data = {
            'user': {'name': 'first'},
            'order': {'type': 'first'}
        }
        response: Response = client.patch('/api/v1/boards/0/pieces/', params=params, json=data)

        assert response.status_code == http_exception_404.status_code
        assert response.json()['detail'] == http_exception_404.detail

    def test_put_pieces_when_no_user(self, init_board):
        params = {'raw': 0, 'column': 0}
        data = {
            'user': {'name': 'first'},
            'order': {'type': 'first'}
        }
        response: Response = client.patch('/api/v1/boards/0/pieces/', params=params, json=data)

        assert response.status_code == 400
        assert response.json()['detail'] == 'There is no user on board'

    def test_put_pieces_when_user_unmatch(self, init_board):
        params = {'raw': 0, 'column': 0}
        data = {
            'user': {'name': 'hoge'},
            'order': {'type': 'first'}
        }
        response: Response = client.patch('/api/v1/boards/0/pieces/', params=params, json=data)
