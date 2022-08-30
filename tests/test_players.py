
import pytest
from requests.models import Response
from xo_connect5.exceptions.players import PlayersError
from xo_connect5.models.users import Order, OrderType, Players, User

from tests import client, http_exception_404
from tests.conftest import players_on_board

valid_user = [
    (User(name='first'), Order(type=OrderType.FIRST)),
    (User(name='draw'), Order(type=OrderType.DRAW))
]

invalid_user = [
    (User(name='first'), Order(type=OrderType.NONE)),
]


class TestGetPlayers:
    def test_get_players_when_no_board(self, no_board):
        response: Response = client.get('/api/v1/boards/0/players/')

        assert response.status_code == http_exception_404.status_code
        assert response.json()['detail'] == http_exception_404.detail

    def test_get_players_when_init_board(self, init_board):
        response: Response = client.get('/api/v1/boards/0/players/')

        assert response.status_code == 200
        assert response.json() == Players()


class TestPutPlayers:
    def test_put_players_when_no_board(self, no_board):
        response: Response = client.put('/api/v1/boards/0/players/')

        assert response.status_code == http_exception_404.status_code
        assert response.json()['detail'] == http_exception_404.detail

    @pytest.mark.parametrize('user, order', valid_user)
    def test_put_players_when_init_board(self, init_board, user: User, order: Order):
        data = {'user': user.dict(), 'order': order.dict()}
        response: Response = client.put('/api/v1/boards/0/players/', json=data)
        players = Players()
        players = players.copy(update={order.type: user})

        assert response.status_code == 200
        assert response.json() == players

    @pytest.mark.parametrize('user, order', valid_user)
    def test_put_players_when_other_user_exists(self, ready_board, user: User, order: Order):
        data = {'user': user.dict(), 'order': order.dict()}
        response: Response = client.put('/api/v1/boards/0/players/', json=data)
        exception = PlayersError(status_code=409, detail='Other player is on board')

        assert response.status_code == exception.status_code
        assert response.json()['detail'] == exception.detail

    @pytest.mark.parametrize('user, order', invalid_user)
    def test_put_players_when_invalid_order(self, init_board, user: User, order: Order):
        data = {'user': user.dict(), 'order': order.dict()}
        response: Response = client.put('/api/v1/boards/0/players/', json=data)
        exception = PlayersError(status_code=400, detail='NONE is invalid orderType')

        assert response.status_code == exception.status_code
        assert response.json()['detail'] == exception.detail


class TestDeletePlayers:
    @pytest.mark.parametrize('user, order', players_on_board)
    def test_delete_players_when_matched_user_exists(self, ready_board, user: User, order: Order):
        data = {'user': user.dict(), 'order': order.dict()}
        response: Response = client.delete('/api/v1/boards/0/players/', json=data)
        rest_user, rest_order = list(filter(lambda x: x[0] != user and x[1] != order, players_on_board))[0]
        players = Players().copy(update={rest_order.type: rest_user})

        assert response.status_code == 200
        assert response.json() == players

    @pytest.mark.parametrize('user, order', valid_user)
    def test_delete_players_when_no_user(self, init_board, user: User, order: Order):
        data = {'user': user.dict(), 'order': order.dict()}
        response: Response = client.delete('/api/v1/boards/0/players/', json=data)
        exception = PlayersError(status_code=400, detail='There is no user on board')

        assert response.status_code == exception.status_code
        assert response.json()['detail'] == exception.detail

    @pytest.mark.parametrize('user, order', players_on_board)
    def test_delete_players_when_unmatched_user(self, ready_board, user: User, order: Order):
        data = {'user': {'name': 'unmatched_user'}, 'order': order.dict()}
        response: Response = client.delete('/api/v1/boards/0/players/', json=data)
        exception = PlayersError(status_code=400, detail='User does not match')

        assert response.status_code == exception.status_code
        assert response.json()['detail'] == exception.detail
