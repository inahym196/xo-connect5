
from fastapi import APIRouter
from starlette.exceptions import HTTPException
from xo_connect5.models.boards import Board, Boards

router = APIRouter()

boards = Boards()

# dev-init
boards.items.append(Board(id=0))


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
