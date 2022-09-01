
from fastapi.exceptions import HTTPException
from requests.models import Response
from xo_connect5.exceptions.players import PlayersError


def assert_equal_http_exception_404(response: Response):
    expected_exception = HTTPException(status_code=404)
    assert response.status_code == expected_exception.status_code
    assert response.json()['detail'] == expected_exception.detail


def assert_equal_http_exception_409(response: Response):
    expected_exception = HTTPException(status_code=409)
    assert response.status_code == expected_exception.status_code
    print(response.json())
    assert response.json()['detail'] == expected_exception.detail


def assert_equal_players_exception(response: Response, status_code: int, detail: str):
    exception = PlayersError(status_code, detail)
    assert response.status_code == exception.status_code
    assert response.json()['detail'] == exception.detail
