

import xo_connect5.core.main as core
from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException
from xo_connect5.core.main import ApplicationError
from xo_connect5.models import Point
from xo_connect5.models.boards import Board
from xo_connect5.models.pieces import Pieces
from xo_connect5.models.users import OrderType, Player
from xo_connect5.routers.boards.board import _get_board

router = APIRouter()


@router.get('/')
async def get_pieces(board: Board = Depends(_get_board)) -> Pieces:
    return board.pieces


@router.patch('/')
async def put_piece(player: Player = Depends(), point: Point = Depends(), board: Board = Depends(_get_board)) -> Board:
    players = board.players
    order = player.order
    if order == OrderType.NONE:
        raise HTTPException(status_code=400, detail='Parameter order is required')

    sitting_player_dict = players.dict().get(order)
    if sitting_player_dict is None:
        raise HTTPException(status_code=400, detail='Player is not on this board')

    try:
        core.put_piece(board, order, point)
    except ApplicationError as e:
        raise HTTPException(status_code=500, detail=e.detail)
    except Exception:
        raise HTTPException(status_code=500)

    return board
