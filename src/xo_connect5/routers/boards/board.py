import xo_connect5.core.main as core
from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException
from xo_connect5.core.main import ApplicationError
from xo_connect5.models import Point
from xo_connect5.models.boards import Board, BoardStatus
from xo_connect5.models.pieces import Pieces
from xo_connect5.models.users import OrderType, User
from xo_connect5.redis import RedisClient
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


@router.get('/pieces')
async def get_pieces(board: Board = Depends(_get_board)) -> Pieces:
    return board.pieces


async def get_order_from_db(user: User) -> OrderType:
    redis_client = RedisClient()
    order = await redis_client.get_order_from_db(user)
    return order


@router.put('/pieces')
async def put_piece(
    order: OrderType = Depends(get_order_from_db),
    board: Board = Depends(_get_board),
    point: Point = Depends()
) -> Board:
    if order == OrderType.NONE:
        raise HTTPException(status_code=401)
    try:
        core.put_piece(board=board, order=order, point=point)
    except ApplicationError as e:
        raise HTTPException(status_code=500, detail=e.detail)
    except Exception:
        raise HTTPException(status_code=500)
    return board
