from logging import getLogger
from math import floor
from typing import Optional

from fastapi import APIRouter, Depends
from xo_connect5.exceptions.pieces import PiecesError
from xo_connect5.models.boards import Board, BoardStatus
from xo_connect5.models.pieces import Pieces, PieceType, Point, none_piece_type
from xo_connect5.models.users import OrderType
from xo_connect5.routers.boards.players import PlayersParam

router = APIRouter()
logger = getLogger('uvicorn').getChild(__name__)


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


class Vector:
    def __init__(self, x: int, y: int):
        self.unit_x: int = -1
        self.unit_y: int = -1
        self.origin_x = x
        self.origin_y = y
        self.grow_reset()
        self.is_reverse: bool = False

    def rotate_end(self) -> bool:
        if (self.unit_x, self.unit_y) == (0, 0):
            return False
        return True

    def grow_reset(self):
        self.raw = self.origin_x + self.unit_x
        self.column = self.origin_y + self.unit_y

    def rotate(self) -> None:
        if self.unit_x != 1:
            self.unit_x += 1
        elif self.unit_x == 1:
            self.unit_x = -1
            self.unit_y += 1
        self.grow_reset()

    def is_in_board(self) -> bool:
        if 0 <= self.raw < 10 and 0 <= self.column < 10:
            return True
        return False

    def grow(self) -> None:
        self.raw += self.unit_x
        self.column += self.unit_y

    def reverse(self) -> None:
        self.is_reverse = True
        self.unit_x = -self.unit_x
        self.unit_y = -self.unit_y
        self.grow_reset()

    @property
    def norm(self) -> int:
        return max(abs(self.origin_x - self.raw), abs(self.origin_y - self.column)) - 1


class LineCounter:
    def __init__(self, pieces: Pieces, put_point: Point, piece_type: PieceType) -> None:
        self.pieces = pieces
        self.vector = Vector(x=put_point.raw, y=put_point.column)
        self.piece_type = piece_type

    def count_harf_line(self) -> int:
        while self.vector.is_in_board():
            logger.info(f'      vector({self.vector.column},{self.vector.raw}) is in board.')
            check_piece = self.pieces[self.vector.column][self.vector.raw]
            if 'g' in self.piece_type and check_piece in ['xg', 'og', 'xp'] or \
                    'p' in self.piece_type and check_piece in ['op', 'xp', 'og']:
                logger.info(f'      vector({self.vector.column},{self.vector.raw}) piece is ({check_piece}). grow')
                self.vector.grow()
            else:
                break
        return self.vector.norm

    def count_line(self) -> int:
        line = self.count_harf_line()
        logger.info(f'    harf line is {line}. reverse')
        self.vector.reverse()
        line += self.count_harf_line()
        logger.info(f'    full line is {line}. reverse')
        self.vector.reverse()
        return line

    def lined_up_five(self) -> bool:
        count = 0
        while self.vector.rotate_end() and count < 10:
            count += 1
            line = self.count_line()
            if line >= 4:
                return True
            self.vector.rotate()
        return False


def get_connect5_winner(board: Board) -> Optional[OrderType]:
    put_point, pieces = board.last_put_point, board.pieces
    if put_point is None:
        raise
    piece_type = pieces[put_point.column][put_point.raw]
    line_counter = LineCounter(pieces, put_point, piece_type)
    if not line_counter.lined_up_five():
        logger.info('not lined up five.')
        return
    elif 'g' in piece_type:
        return OrderType.FIRST
    elif 'p' in piece_type:
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

    logger.info('===============================')
    logger.info(f'{order.type} put {piece_type} piece in {point.column,point.raw}')
    board.pieces[point.column][point.raw] = piece_type
    board.last_put_point = point
    board.winner = get_connect5_winner(board)
    board.turn += 1
    if board.winner:
        board.status = BoardStatus.END
    return board
