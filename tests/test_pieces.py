

import copy

import pytest
from requests.models import Response

from tests import client
from tests.helpers import assert_equal_players_exception

init_pieces = [['_' for j in range(10)] for i in range(10)]


class TestGetPieces:
    def test_get_pieces_when_init_board(self, init_board):
        response: Response = client.get('/api/v1/boards/0/pieces/')
        assert response.json() == init_pieces


class TestPutPieces:

    def test_put_pieces_when_no_user(self, init_board):
        params = {'raw': 0, 'column': 0}
        data = {
            'user': {'name': 'first'},
            'order': {'type': 'first'}
        }
        response: Response = client.patch('/api/v1/boards/0/pieces/', params=params, json=data)
        assert_equal_players_exception(response, 400, detail='There is no user on board')

    def test_put_pieces_when_unmatched_user(self, starting_board):
        params = {'raw': 0, 'column': 0}
        data = {
            'user': {'name': 'unmatched_name'},
            'order': {'type': 'first'}
        }
        response: Response = client.patch('/api/v1/boards/0/pieces/', params=params, json=data)
        assert_equal_players_exception(response, 400, detail='User does not match')

    @pytest.mark.parametrize('raw, column', [(0, 0)])
    def test_put_pieces_when_matched_user(self, starting_board, raw, column):
        params = {'raw': raw, 'column': column}
        data = {
            'user': {'name': 'first'},
            'order': {'type': 'first'}
        }
        response: Response = client.patch('/api/v1/boards/0/pieces/', params=params, json=data)
        pieces = copy.copy(init_pieces)
        pieces[column][raw] = 'xg'
        starting_board['pieces'] = pieces
        assert response.status_code == 200
        assert response.json() == starting_board

    @pytest.mark.parametrize('raw, column', [(0, 0)])
    def test_put_pieces_when_init_board(self, waiting_board, raw, column):
        params = {'raw': raw, 'column': column}
        data = {
            'user': {'name': 'first'},
            'order': {'type': 'first'}
        }
        response: Response = client.patch('/api/v1/boards/0/pieces/', params=params, json=data)
        assert response.status_code == 500
        assert response.json()['detail'] == '[app] board is not ready'
