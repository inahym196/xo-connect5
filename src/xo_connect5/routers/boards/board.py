from typing import Optional

import xo_connect5.core.main as core
from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException
from xo_connect5.core.main import ApplicationError
from xo_connect5.models import Point
from xo_connect5.models.boards import Board, BoardStatus
from xo_connect5.models.pieces import Pieces
from xo_connect5.models.users import OrderType, Player, Players, User
from xo_connect5.routers.boards.boards import boards

router = APIRouter()


async def _get_board(board_id: int) -> Board:
    try:
        board = boards.items[board_id]
    except Exception:
        raise HTTPException(status_code=404)
    return board


@router.get('/', response_model=Board)
async def get_board(board: Board = Depends(_get_board)) -> Board:
    return board


@router.get('/status', response_model=BoardStatus)
async def get_status(board: Board = Depends(_get_board)) -> BoardStatus:
    return board.status


@router.get('/pieces')
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


@router.put('/pieces')
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


@router.get('/players', response_model=Players)
async def get_players(board: Board = Depends(_get_board)) -> Players:
    return board.players


@router.patch('/players', response_model=Players)
async def join_player(player: Player = Depends(), board: Board = Depends(_get_board)) -> Players:
    order = player.order
    if order == OrderType.NONE:
        raise HTTPException(status_code=400, detail='request order is none')
    elif board.players.dict().get(order):
        raise HTTPException(status_code=409, detail='There is already other player')
    board.players = board.players.copy(update={order: player})
    return board.players
