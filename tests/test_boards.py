
from fastapi.exceptions import HTTPException
from requests.models import Response
from xo_connect5.models.boards import Board, BoardStatus

from tests import client
from tests.helpers import (assert_equal_http_exception_404,
                           assert_equal_http_exception_409)


class TestGetBoards:

    def test_get_boards_when_no_board(self, no_board):
        response: Response = client.get('/api/v1/boards/')

        assert response.status_code == 200
        assert response.json()['items'] == []

    def test_get_boards_when_init_board(self, init_board):
        response: Response = client.get('/api/v1/boards/')

        expected_json = {'items': [
            {
                'id': 0,
                'pieces': [['_' for j in range(10)] for i in range(10)],
                'round': 0,
                'status': 'waiting',
                'players': {'first': None, 'draw': None},
            }
        ]}
        assert response.status_code == 200
        assert response.json() == expected_json


class TestPostBoards:

    def test_post_boards_when_no_board(self, no_board):
        response: Response = client.post('/api/v1/boards/')

        expected_json = {
            'id': 0,
            'pieces': [['_' for j in range(10)] for i in range(10)],
            'round': 0,
            'status': 'waiting',
            'players': {'first': None, 'draw': None},
        }
        assert response.status_code == 200
        assert response.json() == expected_json

    def test_post_boards_when_init_board(self, init_board):
        response: Response = client.post('/api/v1/boards/')
        assert_equal_http_exception_409(response)


class TestGetBoard:

    def test_get_board_when_no_board(self, no_board):
        response: Response = client.get('/api/v1/boards/0/')
        assert_equal_http_exception_404(response)

    def test_get_board_when_init_board(self, init_board):
        response: Response = client.get('/api/v1/boards/0/')

        expected_json = {
            'id': 0,
            'pieces': [['_' for j in range(10)] for i in range(10)],
            'round': 0,
            'status': 'waiting',
            'players': {'first': None, 'draw': None},
        }
        assert response.status_code == 200
        assert response.json() == expected_json


class TestGetBoardStatus:
    def test_get_board_status_when_no_board(self, no_board):
        response: Response = client.get('/api/v1/boards/0/status')
        assert_equal_http_exception_404(response)

    def test_get_board_status_when_init_board(self, init_board):
        response: Response = client.get('/api/v1/boards/0/status')

        assert response.status_code == 200
        assert response.json() == BoardStatus.WAITING

    def test_get_board_status_when_two_players_exist(self, ready_board):
        response: Response = client.get('/api/v1/boards/0/status')

        assert response.status_code == 200
        assert response.json() == BoardStatus.STARTING


class TestPostBoard:
    def test_post_board_when_no_board(self, no_board):
        response: Response = client.post('/api/v1/boards/')
        board = Board(id=0)

        assert response.status_code == 200
        for key, value in response.json().items():
            assert value == board.dict()[key]

    def test_post_board_when_init_board(self, init_board):
        response: Response = client.post('/api/v1/boards/')
        assert_equal_http_exception_409(response)


class TestDeleteBoard:
    def test_delete_board_when_no_board(self, no_board):
        response: Response = client.delete('/api/v1/boards/0')
        assert_equal_http_exception_404(response)

    def test_delete_board_when_init_board(self, init_board):
        response: Response = client.delete('/api/v1/boards/0')
        exception = HTTPException(status_code=204)

        assert response.status_code == exception.status_code
        assert response._content == b''
