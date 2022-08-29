
from typing import Optional

from fastapi import HTTPException


class PlayersError(HTTPException):
    def __init__(self, status_code: int, detail: Optional[str] = None) -> None:
        self.status_code = status_code
        self.detail = detail
