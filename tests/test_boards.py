

from typing import Any

from requests.models import Response

from tests import client
from tests.conftest import BoardFixture
from tests.helpers import (assert_equal_http_exception_404,
                           assert_equal_http_exception_409)


class TestGetBoards:
    def test_get_boards_when_no_board(self, no_board: dict[str, Any]):
        expected_json = no_board
        response: Response = client.get('/api/v1/boards/')
        assert response.status_code == 200
        assert response.json() == expected_json

    def test_get_boards_when_init_board(self, init_board: BoardFixture):
        _, expected_json = init_board
        response: Response = client.get('/api/v1/boards/')
        assert response.status_code == 200
        assert response.json() == {'items': [expected_json]}


class TestPostBoards:
    def test_post_boards_when_no_board(self, init_board: BoardFixture):
        response, expected_json = init_board
        assert response.status_code == 200
        assert response.json() == expected_json

    def test_post_boards_when_init_board(self, init_board: BoardFixture):
        response: Response = client.post('/api/v1/boards/')
        assert_equal_http_exception_409(response)


class TestGetBoard:
    def test_get_board_when_no_board(self):
        response: Response = client.get('/api/v1/boards/0/')
        assert_equal_http_exception_404(response)

    def test_get_board_when_init_board(self, init_board: BoardFixture):
        _, expected_json = init_board
        response: Response = client.get('/api/v1/boards/0/')
        assert response.status_code == 200
        assert response.json() == expected_json


class TestGetBoardStatus:
    def test_get_board_status_when_no_board(self):
        response: Response = client.get('/api/v1/boards/0/status')
        assert_equal_http_exception_404(response)

    def test_get_board_status_when_init_board(self, init_board: BoardFixture):
        _, expected_json = init_board
        response: Response = client.get('/api/v1/boards/0/status')
        assert response.status_code == 200
        assert response.json() == expected_json['status']

    def test_get_board_status_when_starting_board(self, starting_board: dict[str, Any]):
        response: Response = client.get('/api/v1/boards/0/status')
        assert response.status_code == 200
        assert response.json() == starting_board['status']


class TestDeleteBoard:
    def test_delete_board_when_no_board(self):
        response: Response = client.delete('/api/v1/boards/0')
        assert_equal_http_exception_404(response)

    def test_delete_board_when_init_board(self, init_board: BoardFixture):
        response: Response = client.delete('/api/v1/boards/0')
        assert response.status_code == 204
        assert response._content == b''

        response = client.get('/api/v1/boards/0/')
        assert_equal_http_exception_404(response)
