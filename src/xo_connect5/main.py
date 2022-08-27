import logging
from enum import Enum
from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from redis import StrictRedis
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


class OrderType(str, Enum):
    FIRST = 'first'
    DRAW = 'draw'


class RedisClient:
    def __init__(self) -> None:
        self.client = StrictRedis()

    async def get_user_order(self, user: str) -> Optional[OrderType]:
        hget_bytes = self.client.hget(name='order', key=user)
        if not hget_bytes:
            return

        order = hget_bytes.decode()
        if order in [OrderType.FIRST, OrderType.DRAW]:
            return order


app = FastAPI()


class Board:
    def __init__(self) -> None:
        none_piece = PieceType.NONE
        self.pieces = [[none_piece for j in range(LENGTH_OF_SIDE)] for i in range(LENGTH_OF_SIDE)]

    def put_piece(self, order: OrderType, point: Point):
        if order == OrderType.FIRST:
            piece = PieceType.XP
        else:
            piece = PieceType.OG
        raw = point.raw
        column = point.column
        self.pieces[column][raw] = piece


board = Board()


@app.get('/pieces')
async def init_piece() -> JSONResponse:
    return JSONResponse({'pieces': board.pieces})


@app.put('/pieces')
async def put_piece(user: str, point: Point = Depends()) -> JSONResponse:
    redis_client = RedisClient()
    order = await redis_client.get_user_order(user)
    if not order:
        raise HTTPException(status_code=404, detail='User not found')
    board.put_piece(order=order, point=point)

    return JSONResponse({'pieces': board.pieces})


def main():
    uvicorn.run('src.xo_connect5.main:app', reload=True, port=8000)


if __name__ == '__main__':
    main()
