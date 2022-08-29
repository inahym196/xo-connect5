
from http.client import HTTPException


class PlayersError(HTTPException):
    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
