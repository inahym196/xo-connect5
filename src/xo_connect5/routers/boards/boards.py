
from fastapi import APIRouter
from starlette.exceptions import HTTPException
from xo_connect5.models.boards import Board, Boards
from xo_connect5.models.users import OrderType, Player, Players, User

router = APIRouter()

boards = Boards()

# dev-init
_first_player = Player(user=User(name='first'), order=OrderType.FIRST)
_draw_player = Player(user=User(name='draw'), order=OrderType.DRAW)
_players = Players(first=_first_player, draw=_draw_player)
_board = Board(id=0, players=_players)
boards.items.append(_board)


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
