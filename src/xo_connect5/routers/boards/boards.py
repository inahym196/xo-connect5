
from fastapi import APIRouter
from starlette.exceptions import HTTPException
from xo_connect5.models.boards import Board, Boards
from xo_connect5.models.pieces import PieceType
from xo_connect5.redis import init_players

router = APIRouter()

boards = Boards()


@router.get('/')
async def get_boards() -> Boards:
    return boards


@router.post('/')
async def create_board() -> Board:
    if len(boards.items) != 0:
        raise HTTPException(status_code=409)
    init_pieces = [[PieceType.NONE for j in range(10)] for i in range(10)]
    board = Board(id=0, pieces=init_pieces)
    boards.items.append(board)
    await init_players(board_id=0)
    return board
