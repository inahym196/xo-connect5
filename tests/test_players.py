
import pytest
from requests.models import Response

from tests import client
from tests.conftest import players_on_board
from tests.helpers import assert_equal_players_exception

valid_user = [
    ({'name': 'first'}, {'type': 'first'}),
    ({'name': 'draw'}, {'type': 'draw'}),
]

invalid_user = [
    ({'name': 'first'}, {'type': 'none'}),
    ({'name': 'draw'}, {'type': 'none'}),
]

init_players_json = {'first': None, 'draw': None}


class TestGetPlayers:
    def test_get_players_when_init_board(self, init_board):
        response: Response = client.get('/api/v1/boards/0/players/')
        assert response.status_code == 200
        assert response.json() == init_players_json


class TestPutPlayers:
    @pytest.mark.parametrize('user, order', valid_user)
    def test_put_players_when_init_board(self, init_board, user, order):
        data = {'user': user, 'order': order}
        response: Response = client.put('/api/v1/boards/0/players/', json=data)

        players_json = init_players_json | {order['type']: user}
        assert response.status_code == 200
        assert response.json() == players_json

    @pytest.mark.parametrize('user, order', valid_user)
    def test_put_players_when_other_user_exists(self, starting_board, user, order):
        data = {'user': user, 'order': order}
        response: Response = client.put('/api/v1/boards/0/players/', json=data)
        assert_equal_players_exception(response, 409, 'Other player is on board')

    @pytest.mark.parametrize('user, order', invalid_user)
    def test_put_players_when_invalid_order(self, init_board, user, order):
        data = {'user': user, 'order': order}
        response: Response = client.put('/api/v1/boards/0/players/', json=data)
        assert_equal_players_exception(response, 400, 'NONE is invalid orderType')


class TestDeletePlayers:
    @pytest.mark.parametrize('user, order', players_on_board)
    def test_delete_players_when_matched_user_exists(self, starting_board, user, order):
        data = {'user': user, 'order': order}
        response: Response = client.delete('/api/v1/boards/0/players/', json=data)
        rest_user, rest_order = list(filter(lambda x: x[0] != user and x[1] != order, players_on_board))[0]
        players_json = init_players_json | {rest_order['type']: rest_user}

        assert response.status_code == 200
        assert response.json() == players_json

    @pytest.mark.parametrize('user, order', valid_user)
    def test_delete_players_when_no_user(self, init_board, user, order):
        data = {'user': user, 'order': order}
        response: Response = client.delete('/api/v1/boards/0/players/', json=data)
        assert_equal_players_exception(response, 400, detail='There is no user on board')

    @pytest.mark.parametrize('user, order', players_on_board)
    def test_delete_players_when_unmatched_user(self, starting_board, user, order):
        user['name'] = 'unmatched_user'
        data = {'user': user, 'order': order}
        response: Response = client.delete('/api/v1/boards/0/players/', json=data)
        assert_equal_players_exception(response, 400, detail='User does not match')
