
from fastapi import APIRouter
from starlette.exceptions import HTTPException
from xo_connect5.models import Board, Boards, BoardStatus

router = APIRouter()
boards = Boards()


@router.get('/')
async def get_boards() -> Boards:
    return boards


@router.post('/')
async def create_board() -> Board:
    board = Board(id=0)
    if len(boards.items) != 0:
        raise HTTPException(status_code=409)
    boards.items.append(board)
    return board


@router.get('/{board_id}/status', response_model=BoardStatus)
async def get_status(board_id: int) -> BoardStatus:
    try:
        board = boards.items[board_id]
    except Exception:
        raise HTTPException(status_code=404)
    return board.status
