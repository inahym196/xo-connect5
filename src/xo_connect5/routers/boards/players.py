
from typing import Optional

from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException
from xo_connect5.models.boards import Board
from xo_connect5.models.users import OrderType, Player, Players
from xo_connect5.routers.boards.board import _get_board

router = APIRouter()


class PlayersParam:
    def __init__(self, player: Player = Depends(), board: Board = Depends(_get_board)) -> None:
        self.player = player
        self.board = board


@router.get('/', response_model=Players)
async def get_players(board: Board = Depends(_get_board)) -> Players:
    return board.players


def get_player_from_order_in_board(order: OrderType, board: Board) -> Optional[Player]:
    sitting_player_dict = board.players.dict().get(order)
    if sitting_player_dict:
        return Player(**sitting_player_dict)


@router.put('/{order}', response_model=Players)
async def join_player(order: OrderType, param: PlayersParam = Depends()) -> Players:
    join_player, board = param.player, param.board
    if order == OrderType.NONE:
        raise HTTPException(status_code=400, detail='Request order is none')

    board_player = get_player_from_order_in_board(order, param.board)
    if board_player:
        raise HTTPException(status_code=409, detail='Other player is on board')

    board.players = board.players.copy(update={order: join_player}, deep=True)
    return board.players


@router.delete('/{order}', response_model=Players)
async def leave_player(order: OrderType, param: PlayersParam = Depends()) -> Players:
    leave_player, board = param.player, param.board
    if order == OrderType.NONE:
        raise HTTPException(status_code=400, detail='request order is none')

    board_player = get_player_from_order_in_board(order, param.board)
    if board_player is None:
        raise HTTPException(status_code=400, detail='There is no player')
    elif board_player != leave_player:
        raise HTTPException(status_code=400, detail='player does not match')

    board.players = board.players.copy(update={order: None})
    return board.players
