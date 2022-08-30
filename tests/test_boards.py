
from fastapi.exceptions import HTTPException
from requests.models import Response
from xo_connect5.models.boards import Board, Boards

from tests import client, http_exception_404, http_exception_409


class TestGetBoards:

    def test_get_boards_when_no_board(self, no_board):
        response: Response = client.get('/api/v1/boards/')
        boards = Boards()

        assert response.status_code == 200
        assert response.json()['items'] == boards.items

    def test_get_boards_when_init_board(self, init_board):
        response: Response = client.get('/api/v1/boards/')
        boards = Boards(items=[Board(id=0)])

        assert response.status_code == 200
        for res_item, board_item in zip(response.json()['items'], boards.items):
            assert res_item == board_item


class TestPostBoards:
    def test_post_boards_when_no_board(self, no_board):
        response: Response = client.post('/api/v1/boards/')
        board = Board(id=0)

        assert response.status_code == 200
        assert response.json() == board

    def test_post_boards_when_init_board(self, init_board):
        response: Response = client.post('/api/v1/boards/')

        assert response.status_code == http_exception_409.status_code
        assert response.json()['detail'] == http_exception_409.detail


class TestGetBoard:

    def test_get_board_when_no_board(self, no_board):
        response: Response = client.get('/api/v1/boards/0/')

        assert response.status_code == http_exception_404.status_code
        assert response.json()['detail'] == http_exception_404.detail

    def test_get_board_when_init_board(self, init_board):
        response: Response = client.get('/api/v1/boards/0/')
        board = Board(id=0)

        assert response.status_code == 200
        assert response.json() == board

    def test_get_board_status_when_no_board(self, no_board):
        response: Response = client.get('/api/v1/boards/0/status')
        exception = HTTPException(status_code=404)

        assert response.status_code == exception.status_code
        assert response.json()['detail'] == exception.detail

    def test_get_board_status_when_init_board(self, init_board):
        response: Response = client.get('/api/v1/boards/0/status')
        board = Board(id=0)

        assert response.status_code == 200
        assert response.json() == board.status


class TestPostBoard:
    def test_post_board_when_no_board(self, no_board):
        response: Response = client.post('/api/v1/boards/')
        board = Board(id=0)

        assert response.status_code == 200
        for key, value in response.json().items():
            assert value == board.dict()[key]

    def test_post_board_when_init_board(self, init_board):
        response: Response = client.post('/api/v1/boards/')

        assert response.status_code == http_exception_409.status_code
        assert response.json()['detail'] == http_exception_409.detail


class TestDeleteBoard:
    def test_delete_board_when_no_board(self, no_board):
        response: Response = client.delete('/api/v1/boards/0')
        assert response.status_code == http_exception_404.status_code
        assert response.json()['detail'] == http_exception_404.detail

    def test_delete_board_when_init_board(self, init_board):
        response: Response = client.delete('/api/v1/boards/0')
        exception = HTTPException(status_code=204)

        assert response.status_code == exception.status_code
        assert response._content == b''
