import logging
from math import floor
from typing import Optional

from fastapi import APIRouter, Depends
from xo_connect5.exceptions.pieces import PiecesError
from xo_connect5.models.boards import Board, BoardStatus
from xo_connect5.models.pieces import Pieces, PieceType, Point, none_piece_type
from xo_connect5.models.users import OrderType
from xo_connect5.routers.boards.players import PlayersParam
from xo_connect5.utils.logger import setup_logger

router = APIRouter()

logger = setup_logger(__name__, logging.DEBUG)


def get_piece_type(turn: int, order_type: OrderType) -> PieceType:
    is_special_turn = floor((turn % 8) / 6) == 1
    piece_type: PieceType
    if is_special_turn:
        if order_type == OrderType.FIRST:
            piece_type = 'og'
        else:
            piece_type = 'xp'
    else:
        if order_type == OrderType.FIRST:
            piece_type = 'xg'
        else:
            piece_type = 'op'
    return piece_type


def is_your_turn(turn: int, order_type: OrderType) -> bool:
    first_turn = floor(turn % 2) == 0
    if order_type == OrderType.FIRST and first_turn:
        return True
    elif order_type == OrderType.DRAW and not first_turn:
        return True
    return False


class UnitVector:
    def __init__(self) -> None:
        self.x: int = -1
        self.y: int = -1

    def rotate_end(self) -> bool:
        if (self.x, self.y) == (0, 0):
            return False
        return True

    def rotate(self) -> None:
        self.reverse()
        if self.x != 1:
            self.x += 1
        elif self.x == 1:
            self.x = -1
            self.y += 1

    def reverse(self) -> None:
        self.x = -self.x
        self.y = -self.y


class Vector:
    def __init__(self, put_point: Point, unit_vector: UnitVector):
        self.origin_x = put_point.raw
        self.origin_y = put_point.column
        self.unit_vector = unit_vector
        self.raw = self.origin_x + self.unit_vector.x
        self.column = self.origin_y + self.unit_vector.y

    def is_in_board(self) -> bool:
        if 0 <= self.raw < 10 and 0 <= self.column < 10:
            return True
        return False

    def grow(self) -> None:
        self.raw += self.unit_vector.x
        self.column += self.unit_vector.y

    @property
    def norm(self) -> int:
        return max(abs(self.origin_x - self.raw), abs(self.origin_y - self.column)) - 1


class LineCounter:
    def __init__(self, pieces: Pieces, put_point: Point, piece_type: PieceType) -> None:
        self.pieces = pieces
        self.unit_vector = UnitVector()
        self.piece_type = piece_type
        self.put_point = put_point

    def count_half_line(self) -> int:
        vector = Vector(self.put_point, self.unit_vector)
        logger.debug(f'  unit_vector {self.unit_vector.y,self.unit_vector.x}, vector{vector.column,vector.raw}')
        while vector.is_in_board():
            logger.debug(f'    vector({vector.column},{vector.raw}) is in board.')
            check_piece = self.pieces[vector.column][vector.raw]
            if 'g' in self.piece_type and check_piece in ['xg', 'og', 'xp'] or \
                    'p' in self.piece_type and check_piece in ['op', 'xp', 'og']:
                logger.debug(f'    vector({vector.column},{vector.raw}) piece is "{check_piece}". grow.')
                vector.grow()
            else:
                logger.debug(f'    vector({vector.column},{vector.raw}) piece is "{check_piece}". break.')
                break
        return vector.norm

    def count_line(self) -> int:
        line: int = 1
        line += self.count_half_line()
        self.unit_vector.reverse()
        line += self.count_half_line()
        logger.debug(f'  full line is {line}. unit_vector rotate.')
        return line

    def lined_up_five(self) -> bool:
        while self.unit_vector.rotate_end():
            line = self.count_line()
            if line >= 5:
                return True
            self.unit_vector.rotate()
        return False


def get_connect5_winner(board: Board) -> Optional[OrderType]:
    put_point, pieces = board.last_put_point, board.pieces
    if put_point is None:
        raise
    piece_type = pieces[put_point.column][put_point.raw]
    logger.debug(f'Put {piece_type} piece in {put_point.column,put_point.raw}')
    line_counter = LineCounter(pieces, put_point, piece_type)
    if not line_counter.lined_up_five():
        logger.debug('not lined up five.')
        return
    elif 'g' in piece_type:
        logger.debug(f'lined up five! {OrderType.FIRST} win!')
        return OrderType.FIRST
    elif 'p' in piece_type:
        logger.debug(f'lined up five! {OrderType.DRAW} win!')
        return OrderType.DRAW


@router.put('/')
async def put_piece(point: Point = Depends(), players_param: PlayersParam = Depends()) -> Board:
    order, board = players_param.order, players_param.board
    piece_type = get_piece_type(board.turn, order.type)
    players_param.get_matched_user()

    if board.status != BoardStatus.STARTING:
        raise PiecesError(status_code=404, detail='Board is not ready')
    elif not is_your_turn(board.turn, order.type):
        raise PiecesError(status_code=404, detail='It\'s not your turn')

    if board.pieces[point.column][point.raw] != none_piece_type:
        raise PiecesError(status_code=404, detail='Piece is already exist')

    board.pieces[point.column][point.raw] = piece_type
    board.last_put_point = point
    board.winner = get_connect5_winner(board)
    board.turn += 1
    if board.winner:
        board.status = BoardStatus.END
    return board
