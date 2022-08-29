
from fastapi import APIRouter
from starlette.exceptions import HTTPException
from xo_connect5.models.boards import Board, Boards
from xo_connect5.models.pieces import PieceType

router = APIRouter()

boards = Boards()

# dev-init
_init_pieces = [[PieceType.NONE for j in range(10)] for i in range(10)]
_board = Board(id=0, pieces=_init_pieces)
boards.items.append(_board)


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
    return board
