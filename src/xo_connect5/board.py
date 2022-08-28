
from typing import Optional

from fastapi import Depends
from redis import StrictRedis

from xo_connect5.models import (LENGTH_OF_SIDE, BoardStatus, OrderType,
                                PieceType, Point, User)


class RedisClient:
    def __init__(self) -> None:
        self.client = StrictRedis()

    async def get_user_order(self, user: User) -> Optional[OrderType]:
        hget_bytes = self.client.hget(name='order', key=user.name)
        if not hget_bytes:
            return

        order = hget_bytes.decode()
        if order not in [OrderType.FIRST, OrderType.DRAW]:
            return

        return order


async def get_user_order(user: User) -> Optional[OrderType]:
    redis_client = RedisClient()
    order = await redis_client.get_user_order(user)
    return order


async def get_piece_of_this_turn(order: OrderType = Depends(get_user_order)) -> Optional[PieceType]:
    if not order:
        return
    elif order == OrderType.FIRST:
        piece_type = PieceType.XP
    else:
        piece_type = PieceType.OG
    return piece_type


class PutPieceParam:
    def __init__(self, piece_type: Optional[PieceType] = Depends(get_piece_of_this_turn), point: Point = Depends()) -> None:
        self.piece_type = piece_type
        self.point = point


class BoardError(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)
        self.detail = detail


class Board:
    def __init__(self) -> None:
        none_piece = PieceType.NONE
        self.pieces = [[none_piece for j in range(LENGTH_OF_SIDE)] for i in range(LENGTH_OF_SIDE)]
        self.turn = 0
        self.status = BoardStatus.NOT_READY

    def put_piece(self, put_piece_param: PutPieceParam) -> None:
        raw = put_piece_param.point.raw
        column = put_piece_param.point.column

        if not put_piece_param.piece_type:
            raise BoardError(detail='Piece type does not exist for the specified user')
        elif self.pieces[column][raw] != PieceType.NONE:
            raise BoardError(detail='A piece already exists at the specified location')

        self.pieces[column][raw] = put_piece_param.piece_type
        self.turn += 1
