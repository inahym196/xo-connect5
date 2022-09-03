from typing import Any

import pytest
from requests.models import Response

from tests import client
from tests.helpers import assert_equal_players_exception

init_pieces = [['_' for j in range(10)] for i in range(10)]


class TestPutPieces:

    def test_put_pieces_when_no_user(self, init_board):
        params = {'raw': 0, 'column': 0}
        data = {
            'user': {'name': 'first'},
            'order': {'type': 'first'}
        }
        response: Response = client.put('/api/v1/boards/0/pieces/', params=params, json=data)
        assert_equal_players_exception(response, 400, detail='There is no user on board')

    def test_put_pieces_when_unmatched_user(self, starting_board):
        params = {'raw': 0, 'column': 0}
        data = {
            'user': {'name': 'unmatched_name'},
            'order': {'type': 'first'}
        }
        response: Response = client.put('/api/v1/boards/0/pieces/', params=params, json=data)
        assert_equal_players_exception(response, 400, detail='User does not match')

    @pytest.mark.parametrize('raw, column', [(0, 0)])
    def test_put_pieces_when_matched_user(self, starting_board: dict[str, Any], raw, column):
        expected_json = starting_board
        params = {'raw': raw, 'column': column}
        data = {'user': {'name': 'first'}, 'order': {'type': 'first'}}
        response: Response = client.put('/api/v1/boards/0/pieces/', params=params, json=data)

        expected_json['pieces'][column][raw] = 'xg'
        expected_json['turn'] = 1
        expected_json['last_put_point'] = {'raw': raw, 'column': column}
        assert response.status_code == 200
        assert response.json() == expected_json

    @pytest.mark.parametrize('raw, column', [(0, 0)])
    def test_put_pieces_when_waiting_board(self, waiting_draw_user_board, raw, column):
        params = {'raw': raw, 'column': column}
        data = {'user': {'name': 'first'}, 'order': {'type': 'first'}}
        response: Response = client.put('/api/v1/boards/0/pieces/', params=params, json=data)
        assert response.status_code == 404
        assert response.json()['detail'] == 'Board is not ready'
