from typing import Any

import pytest
from requests.models import Response

from tests import client
from tests.conftest import BoardFixture
from tests.helpers import assert_equal_players_exception


class TestPutPlayers:
    @pytest.mark.parametrize('user, order', [
        ({'name': 'first'}, {'type': 'first'}),
        ({'name': 'hoge'}, {'type': 'first'}),
        ({'name': 'draw'}, {'type': 'draw'}),
        ({'name': 'huga'}, {'type': 'draw'}),
    ])
    def test_put_players_when_init_board(self, init_board: BoardFixture, user, order):
        _, init_expected_json = init_board
        data = {'user': user, 'order': order}
        response: Response = client.put('/api/v1/boards/0/players/', json=data)
        players_json = init_expected_json['players'] | {order['type']: user}
        expected_json = init_expected_json | {'players': players_json}
        assert response.status_code == 200
        assert response.json() == expected_json

    @pytest.mark.parametrize('order', [{'type': 'first'}, {'type': 'draw'}])
    def test_put_players_when_other_user_exists(self, starting_board, order: dict[str, str]):
        data = {'user': {'name': 'cannot-join-user'}, 'order': order}
        response: Response = client.put('/api/v1/boards/0/players/', json=data)
        assert_equal_players_exception(response, 409, 'Other player is on board')

    @pytest.mark.parametrize('user', [{'name': 'first'}, {'name': 'draw'}])
    def test_put_players_when_invalid_order(self, init_board, user: dict[str, str]):
        data = {'user': user, 'order': {'type': 'none'}}
        response: Response = client.put('/api/v1/boards/0/players/', json=data)
        assert_equal_players_exception(response, 400, 'NONE is invalid orderType')


class TestDeletePlayers:
    @pytest.mark.parametrize('order', [{'type': 'first'}, {'type': 'draw'}])
    def test_delete_players_when_matched_user_exists(self, starting_board: dict[str, Any], order: dict[str, str]):
        starting_expected_json = starting_board
        user = starting_expected_json['players'][order['type']]
        data = {'user': user, 'order': order}
        response: Response = client.delete('/api/v1/boards/0/players/', json=data)
        players_json = starting_expected_json['players'] | {order['type']: None}
        expected_json = starting_expected_json | {'players': players_json, 'status': 'waiting'}
        assert response.status_code == 200
        assert response.json() == expected_json

    @pytest.mark.parametrize('order', [{'type': 'first'}, {'type': 'draw'}])
    def test_delete_players_when_no_user(self, init_board, order: dict[str, str]):
        data = {'user': {'name': 'join-user'}, 'order': order}
        response: Response = client.delete('/api/v1/boards/0/players/', json=data)
        assert_equal_players_exception(response, 400, detail='There is no user on board')

    @pytest.mark.parametrize('order', [{'type': 'first'}, {'type': 'draw'}])
    def test_delete_players_when_unmatched_user(self, starting_board, order: dict[str, str]):
        data = {'user': {'name': 'unmatched_user'}, 'order': order}
        response: Response = client.delete('/api/v1/boards/0/players/', json=data)
        assert_equal_players_exception(response, 400, detail='User does not match')
