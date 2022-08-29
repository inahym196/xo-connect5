
from typing import Optional

import xo_connect5.core.main as core
from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException
from xo_connect5.core.main import ApplicationError
from xo_connect5.models import Point
from xo_connect5.models.boards import Board
from xo_connect5.models.pieces import Pieces
from xo_connect5.models.users import OrderType, Players, User
from xo_connect5.routers.boards.board import _get_board

router = APIRouter()


@router.get('/')
async def get_pieces(board: Board = Depends(_get_board)) -> Pieces:
    return board.pieces


def get_user_order(user: User, players: Players) -> Optional[OrderType]:
    if user == players.first:
        order = OrderType.FIRST
    elif user == players.draw:
        order = OrderType.DRAW
    else:
        return
    return order


@router.put('/')
async def put_piece(user: User,
                    board: Board = Depends(_get_board),
                    point: Point = Depends()) -> Board:
    order = get_user_order(user, board.players)
    if not order:
        raise HTTPException(status_code=401)

    try:
        core.put_piece(board, order, point)
    except ApplicationError as e:
        raise HTTPException(status_code=500, detail=e.detail)
    except Exception:
        raise HTTPException(status_code=500)
    return board
