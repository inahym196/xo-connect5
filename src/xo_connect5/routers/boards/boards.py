
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from xo_connect5.models.boards import Board, BoardStatus
from xo_connect5.models.users import Players, User

router = APIRouter()

boards: list[Board] = list()

# dev-init
_first_player = User(name='first')
_draw_player = User(name='draw')
_players = Players(first=_first_player, draw=_draw_player)
_board = Board(id=0, players=_players, status=BoardStatus.STARTING)
boards.append(_board)


@router.get('/')
async def get_boards() -> list[Board]:
    return boards


@router.post('/')
async def create_board() -> Board:
    if len(boards) != 0:
        raise HTTPException(status_code=409)
    board = Board(id=0)
    boards.append(board)
    return board
