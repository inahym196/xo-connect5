
from typing import Any

from fastapi.testclient import TestClient
from requests.models import Response
from starlette.exceptions import HTTPException
from xo_connect5.main import app
from xo_connect5.models.boards import Board, Boards, BoardStatus
from xo_connect5.models.users import Players, User

client = TestClient(app)


def test_read_boards():
    response: Response = client.get('/api/v1/boards')
    response_dict: dict[str, Any] = response.json()
    expected = Boards()
    _players = Players(first=User(name='first'), draw=User(name='draw'))
    _board = Board(id=0, players=_players, status=BoardStatus.STARTING)
    expected.items.append(_board)

    assert response.status_code == 200
    assert response_dict['items'] == expected.items


def test_post_boards():
    response: Response = client.post('/api/v1/boards/')
    response_dict: dict[str, Any] = response.json()
    expected = HTTPException(status_code=409)
    assert response.status_code == expected.status_code
    assert response_dict['detail'] == expected.detail
