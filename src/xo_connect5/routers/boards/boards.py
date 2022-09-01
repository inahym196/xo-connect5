
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from xo_connect5.models.boards import Board, Boards, BoardStatus

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


async def _get_board(board_id: int) -> Board:
    try:
        board = boards.items[board_id]
    except Exception:
        raise HTTPException(status_code=404)
    return board


@router.get('/{board_id}', response_model=Board)
async def get_board(board: Board = Depends(_get_board)) -> Board:
    return board


@router.get('/{board_id}/status', response_model=BoardStatus)
async def get_status(board: Board = Depends(_get_board)) -> BoardStatus:
    return board.status


@router.delete('/{board_id}', response_class=Response)
async def delete_board(board_id: int) -> Response:
    if len(boards.items) == 0:
        raise HTTPException(status_code=404)
    boards.items.pop()
    return Response(status_code=204)
