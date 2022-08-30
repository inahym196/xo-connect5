

import xo_connect5.core.main as core
from fastapi import APIRouter, Depends
from xo_connect5.models import Point
from xo_connect5.models.boards import Board
from xo_connect5.models.pieces import Pieces
from xo_connect5.routers.boards.boards import _get_board
from xo_connect5.routers.boards.players import PlayersParam

router = APIRouter()


@router.get('/')
async def get_pieces(board: Board = Depends(_get_board)) -> Pieces:
    return board.pieces


@router.patch('/')
async def put_piece(point: Point = Depends(), players_param: PlayersParam = Depends()) -> Board:
    order, board = players_param.order, players_param.board
    _ = players_param.get_matched_user()

    core.put_piece(board, order, point)

    return board
