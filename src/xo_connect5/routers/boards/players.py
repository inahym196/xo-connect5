
from fastapi import APIRouter, Depends
from xo_connect5.exceptions.players import PlayersError
from xo_connect5.models.boards import Board, BoardStatus
from xo_connect5.models.users import Order, User
from xo_connect5.routers.boards.board import _get_board

router = APIRouter()


class PlayersParam:
    def __init__(self, user: User, order: Order, board: Board = Depends(_get_board)) -> None:
        self.user = user
        self.board = board
        self.order = order

    def get_matched_user(self) -> User:
        players_in_board_dict = self.board.players.dict()
        user_in_board_dict = players_in_board_dict.get(self.order.type)
        if user_in_board_dict is None:
            raise PlayersError(status_code=400, detail='There is no user on board')

        user_in_board = User(**user_in_board_dict)
        if user_in_board != self.user:
            raise PlayersError(status_code=400, detail='User does not match')

        return user_in_board

    def exists_user_in_board(self) -> bool:
        user_in_board_dict = self.board.players.dict().get(self.order.type)
        if user_in_board_dict:
            return True
        return False


@router.put('/', response_model=Board)
async def join_player(param: PlayersParam = Depends()) -> Board:
    join_user, order, board = param.user, param.order, param.board
    if param.exists_user_in_board():
        raise PlayersError(status_code=409, detail='Other player is on board')

    board.players = board.players.copy(update={order.type: join_user}, deep=True)
    if board.players.first and board.players.draw:
        board.status = BoardStatus.STARTING
    return param.board


@router.delete('/', response_model=Board)
async def leave_player(param: PlayersParam = Depends()) -> Board:
    order, board = param.order, param.board
    _ = param.get_matched_user()

    board.players = board.players.copy(update={order.type: None})
    board.status = BoardStatus.WAITING
    return board
