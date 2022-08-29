
from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException
from xo_connect5.models.boards import Board, BoardStatus
from xo_connect5.routers.boards.boards import boards

router = APIRouter()


async def _get_board(board_id: int) -> Board:
    try:
        board = boards.items[board_id]
    except Exception:
        raise HTTPException(status_code=404)
    return board


@router.get('/', response_model=Board)
async def get_board(board: Board = Depends(_get_board)) -> Board:
    return board


@router.get('/status', response_model=BoardStatus)
async def get_status(board: Board = Depends(_get_board)) -> BoardStatus:
    return board.status
