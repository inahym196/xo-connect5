
from requests.models import Response

from tests import client
from tests.helpers import (assert_equal_http_exception_404,
                           assert_equal_http_exception_409)

no_boards_json = {'items': []}


class TestGetBoards:
    def test_get_boards_when_no_board(self):
        response: Response = client.get('/api/v1/boards/')
        assert response.status_code == 200
        assert response.json() == no_boards_json

    def test_get_boards_when_init_board(self, init_board):
        response: Response = client.get('/api/v1/boards/')
        assert response.status_code == 200
        assert response.json() == {'items': [init_board]}


class TestPostBoards:
    def test_post_boards_when_no_board(self):
        response: Response = client.post('/api/v1/boards/')
        assert response.status_code == 200
        assert response.json() == {
            'id': 0,
            'pieces': [['_' for j in range(10)] for i in range(10)],
            'round': 0,
            'status': 'waiting',
            'players': {'first': None, 'draw': None},
        }

    def test_post_boards_when_init_board(self, init_board):
        response: Response = client.post('/api/v1/boards/')
        assert_equal_http_exception_409(response)


class TestGetBoard:
    def test_get_board_when_no_board(self):
        response: Response = client.get('/api/v1/boards/0/')
        assert_equal_http_exception_404(response)

    def test_get_board_when_init_board(self, init_board):
        response: Response = client.get('/api/v1/boards/0/')
        assert response.status_code == 200
        assert response.json() == init_board


class TestGetBoardStatus:
    def test_get_board_status_when_no_board(self):
        response: Response = client.get('/api/v1/boards/0/status')
        assert_equal_http_exception_404(response)

    def test_get_board_status_when_init_board(self, init_board):
        response: Response = client.get('/api/v1/boards/0/status')
        assert response.status_code == 200
        assert response.json() == 'waiting'

    def test_get_board_status_when_starting_board(self, starting_board):
        response: Response = client.get('/api/v1/boards/0/status')
        assert response.status_code == 200
        assert response.json() == 'starting'


class TestDeleteBoard:
    def test_delete_board_when_no_board(self):
        response: Response = client.delete('/api/v1/boards/0')
        assert_equal_http_exception_404(response)

    def test_delete_board_when_init_board(self, init_board):
        response: Response = client.delete('/api/v1/boards/0')
        assert response.status_code == 204
        assert response._content == b''
