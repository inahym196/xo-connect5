

from typing import Any

from requests.models import Response

from tests import client
from tests.conftest import BoardFixture
from tests.helpers import assert_equal_http_exception_409


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
        assert response.json() == [expected_json]


class TestPostBoards:
    def test_post_boards_when_no_board(self, init_board: BoardFixture):
        response, expected_json = init_board
        assert response.status_code == 200
        assert response.json() == expected_json

    def test_post_boards_when_init_board(self, init_board: BoardFixture):
        response: Response = client.post('/api/v1/boards/')
        assert_equal_http_exception_409(response)
