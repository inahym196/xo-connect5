
from fastapi import HTTPException


class ApplicationError(HTTPException):
    def __init__(self, status_code: int = 500, detail=None) -> None:
        super().__init__(status_code, detail=detail)
        self.detail = f'[app] {detail}'
