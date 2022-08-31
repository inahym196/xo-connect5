

from requests.models import Response

from tests import client
from tests.helpers import assert_equal_players_exception


class TestGetPieces:

    def test_get_pieces_when_init_board(self, init_board):
        response: Response = client.get('/api/v1/boards/0/pieces/')
        pieces = [['_' for j in range(10)] for i in range(10)]

        assert response.json() == pieces


class TestPutPieces:

    def test_put_pieces_when_no_user(self, init_board):
        params = {'raw': 0, 'column': 0}
        data = {
            'user': {'name': 'first'},
            'order': {'type': 'first'}
        }
        response: Response = client.patch('/api/v1/boards/0/pieces/', params=params, json=data)
        assert_equal_players_exception(response, 400, detail='There is no user on board')
