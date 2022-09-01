
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from xo_connect5.models.boards import Board, Boards

router = APIRouter()

boards = Boards()

# dev-init
# _first_player = User(name='first')
# _draw_player = User(name='draw')
# _players = Players(first=_first_player, draw=_draw_player)
# _board = Board(id=0, players=_players, status=BoardStatus.STARTING)
# boards.items.append(_board)


@router.get('/')
async def get_boards() -> Boards:
    return boards


@router.post('/')
async def create_board() -> Board:
    if len(boards.items) != 0:
        raise HTTPException(status_code=409)
    board = Board(id=0)
    boards.items.append(board)
    return board
