
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


@router.put('/{order}', response_model=Players)
async def join_player(order: OrderType, param: PlayersParam = Depends()) -> Players:
    join_player, players = param.player, param.board.players
    if order == OrderType.NONE:
        raise HTTPException(status_code=400, detail='request order is none')

    sitting_player_dict = players.dict().get(order)
    if sitting_player_dict:
        raise HTTPException(status_code=409, detail='There is already other player')

    param.board.players = players.copy(update={order: join_player}, deep=True)
    return param.board.players


@router.delete('/{order}', response_model=Players)
async def leave_player(order: OrderType, param: PlayersParam = Depends()) -> Players:
    leave_player, board = param.player, param.board
    if order == OrderType.NONE:
        raise HTTPException(status_code=400, detail='request order is none')

    sitting_player_dict = board.players.dict().get(order)
    if not sitting_player_dict:
        raise HTTPException(status_code=400, detail='There is no player')

    sitting_player = Player(**sitting_player_dict)
    if sitting_player != leave_player:
        raise HTTPException(status_code=400, detail='player does not match')

    board.players = board.players.copy(update={order: None})
    return board.players
