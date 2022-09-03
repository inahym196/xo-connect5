from math import floor
from typing import Optional

from fastapi import APIRouter, Depends
from xo_connect5.exceptions.pieces import PiecesError
from xo_connect5.models.boards import Board, BoardStatus
from xo_connect5.models.pieces import PieceType, Point
from xo_connect5.models.users import OrderType
from xo_connect5.routers.boards.players import PlayersParam

router = APIRouter()


def get_piece_type(turn: int, order_type: OrderType) -> PieceType:
    is_special_turn = floor((turn % 8) / 6) == 1
    if is_special_turn:
        if order_type == OrderType.FIRST:
            piece_type = PieceType.OG
        else:
            piece_type = PieceType.XP
    else:
        if order_type == OrderType.FIRST:
            piece_type = PieceType.XG
        else:
            piece_type = PieceType.OP
    return piece_type


def is_your_turn(turn: int, order_type: OrderType) -> bool:
    first_turn = floor(turn % 2) == 0
    if order_type == OrderType.FIRST and first_turn:
        return True
    elif order_type == OrderType.DRAW and not first_turn:
        return True
    return False


def get_connect5_winner(board: Board) -> Optional[OrderType]:

    return


@router.put('/')
async def put_piece(point: Point = Depends(), players_param: PlayersParam = Depends()) -> Board:
    order, board = players_param.order, players_param.board
    piece_type = get_piece_type(board.turn, order.type)
    _ = players_param.get_matched_user()

    if board.status != BoardStatus.STARTING:
        raise PiecesError(status_code=404, detail='Board is not ready')
    elif not is_your_turn(board.turn, order.type):
        raise PiecesError(status_code=404, detail='It\'s not your turn')
    elif board.pieces[point.raw][point.column] != PieceType.NONE:
        raise PiecesError(status_code=404, detail='Piece is already exist')

    board.pieces[point.column][point.raw] = piece_type
    board.winner = get_connect5_winner(board)
    board.turn += 1
    board.last_put_point = point
    if board.winner:
        board.status = BoardStatus.END
    return board
