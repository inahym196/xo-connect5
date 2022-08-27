import logging
from typing import Literal

import uvicorn
from fastapi import Depends, FastAPI, Request
from pydantic import BaseModel
from src.xo_connect5.exceptions import APIError
from starlette.responses import JSONResponse
from typing_extensions import TypeAlias

LENGTH_OF_SIDE = 10

logger = logging.getLogger('uvicorn')


class Point(BaseModel):
    raw: int
    column: int


Piece: TypeAlias = Literal['xp', 'op', 'xg', 'og', '_']


class PutPieceParam(BaseModel):
    point: Point
    piece: Piece


app = FastAPI()


class Board:
    def __init__(self) -> None:
        none_piece: Piece = '_'
        self.pieces = [[none_piece for j in range(LENGTH_OF_SIDE)] for i in range(LENGTH_OF_SIDE)]

    def put_piece(self, put_piece_param: PutPieceParam):
        raw_point = put_piece_param.point.raw
        column_point = put_piece_param.point.column
        self.pieces[column_point][raw_point] = put_piece_param.piece
        return


board = Board()


@app.exception_handler(APIError)
async def APIExceptionHandler(request: Request, exception: APIError):
    return JSONResponse(status_code=exception.status_code, content=exception.detail)


@app.get('/')
async def init_piece() -> JSONResponse:
    return JSONResponse({'pieces': board.pieces})


async def put_parameters(piece: str, raw: int, column: int):
    return PutPieceParam(point=Point(raw=raw, column=column), piece=piece)


@app.post('/put-piece')
async def put_piece(put_piece_param: PutPieceParam = Depends(PutPieceParam)) -> JSONResponse:
    board.put_piece(put_piece_param)
    return JSONResponse({'pieces': board.pieces})


def main():
    uvicorn.run('src.xo_connect5.main:app', reload=True, port=8000)


if __name__ == '__main__':
    main()
