

from fastapi.exceptions import HTTPException
from fastapi.testclient import TestClient
from requests.models import Response
from xo_connect5.main import app
from xo_connect5.models.boards import Board, Boards, BoardStatus
from xo_connect5.models.users import Players, User

client = TestClient(app)


def test_get_boards():
    response: Response = client.get('/api/v1/boards/')
    _players = Players(first=User(name='first'), draw=User(name='draw'))
    _board = Board(id=0, players=_players, status=BoardStatus.STARTING)
    boards = Boards(items=[_board])

    assert response.status_code == 200
    assert response.json()['items'] == boards.items


def test_post_boards():
    response: Response = client.post('/api/v1/boards/')
    boards = HTTPException(status_code=409)
    assert response.status_code == boards.status_code
    assert response.json()['detail'] == boards.detail
