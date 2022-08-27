import logging
from enum import Enum

import uvicorn
from fastapi import Depends, FastAPI, Request
from pydantic import BaseModel
from src.xo_connect5.exceptions import APIError
from starlette.responses import JSONResponse

LENGTH_OF_SIDE = 10

logger = logging.getLogger('uvicorn')


class Point(BaseModel):
    raw: int
    column: int


class PieceType(str, Enum):
    XP = 'xp'
    OP = 'op'
    XG = 'xg'
    OG = 'og'
    NONE = '_'


class Piece(BaseModel):
    type: PieceType


app = FastAPI()


class Board:
    def __init__(self) -> None:
        none_piece = PieceType.NONE
        self.pieces = [[none_piece for j in range(LENGTH_OF_SIDE)] for i in range(LENGTH_OF_SIDE)]

    def put_piece(self, piece: Piece, point: Point):
        raw = point.raw
        column = point.column
        self.pieces[column][raw] = piece.type


board = Board()


@app.exception_handler(APIError)
async def APIExceptionHandler(request: Request, exception: APIError):
    return JSONResponse(status_code=exception.status_code, content=exception.detail)


@app.get('/pieces')
async def init_piece() -> JSONResponse:
    return JSONResponse({'pieces': board.pieces})


@app.put('/pieces')
async def put_piece(piece: Piece, point: Point = Depends()) -> JSONResponse:
    board.put_piece(piece=piece, point=point)
    return JSONResponse({'pieces': board.pieces})


def main():
    uvicorn.run('src.xo_connect5.main:app', reload=True, port=8000)


if __name__ == '__main__':
    main()
