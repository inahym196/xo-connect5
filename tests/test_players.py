
import pytest
from requests.models import Response
from xo_connect5.models.users import Order, OrderType, Players, User

from tests import client, http_exception_404

addable_user = [
    (User(name='first'), Order(type=OrderType.FIRST)),
    (User(name='draw'), Order(type=OrderType.DRAW))
]


class TestPlayers:
    def test_get_players_when_no_board(self, no_board):
        response: Response = client.get('/api/v1/boards/0/players/')

        assert response.status_code == http_exception_404.status_code
        assert response.json()['detail'] == http_exception_404.detail

    def test_get_players_when_init_board(self, init_board):
        response: Response = client.get('/api/v1/boards/0/players/')

        assert response.status_code == 200
        assert response.json() == Players()

    def test_put_players_when_no_board(self, no_board):
        response: Response = client.put('/api/v1/boards/0/players/')

        assert response.status_code == http_exception_404.status_code
        assert response.json()['detail'] == http_exception_404.detail

    @pytest.mark.parametrize('user, order', addable_user)
    def test_put_players_when_init_board(self, init_board, user: User, order: Order):
        data = {'user': user.dict(), 'order': order.dict()}
        response: Response = client.put('/api/v1/boards/0/players/', json=data)
        players = Players()
        players = players.copy(update={order.type: user})

        assert response.status_code == 200
        assert response.json() == players

    @pytest.mark.parametrize('user, order', addable_user)
    def test_put_players_when_other_user_exists(self, init_board, user: User, order: Order):
        data = {'user': user.dict(), 'order': order.dict()}
        client.put('/api/v1/boards/0/players/', json=data)
        response: Response = client.put('/api/v1/boards/0/players/', json=data)

        assert response.status_code == 409
        assert response.json()['detail'] == 'Other player is on board'
