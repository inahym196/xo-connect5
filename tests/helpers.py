
from fastapi.exceptions import HTTPException
from requests.models import Response


def assert_equal_http_exception_404(response: Response):
    expected_exception = HTTPException(status_code=404)
    assert response.status_code == expected_exception.status_code
    assert response.json()['detail'] == expected_exception.detail


def assert_equal_http_exception_409(response: Response):
    expected_exception = HTTPException(status_code=409)
    assert response.status_code == expected_exception.status_code
    assert response.json()['detail'] == expected_exception.detail
