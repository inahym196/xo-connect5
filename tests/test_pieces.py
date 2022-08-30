

from requests.models import Response
from xo_connect5.models.pieces import Pieces, PieceType

from tests import client, http_exception_404


class TestGetPieces:

    def test_get_pieces_when_no_board(self, no_board):
        response: Response = client.get('/api/v1/boards/0/pieces/')

        assert response.status_code == http_exception_404.status_code
        assert response.json()['detail'] == http_exception_404.detail

    def test_get_pieces_when_init_board(self, init_board):
        response: Response = client.get('/api/v1/boards/0/pieces/')
        pieces: Pieces = [[PieceType.NONE for j in range(10)] for i in range(10)]

        assert response.json() == pieces


class TestPutPieces:
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

    def test_put_pieces_when_user_unmatch(self, ready_board):
        params = {'raw': 0, 'column': 0}
        data = {
            'user': {'name': 'hoge'},
            'order': {'type': 'first'}
        }
        response: Response = client.patch('/api/v1/boards/0/pieces/', params=params, json=data)
