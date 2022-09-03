

from fastapi import APIRouter, Depends
from xo_connect5.exceptions.pieces import PiecesError
from xo_connect5.models import Point
from xo_connect5.models.boards import Board, BoardStatus
from xo_connect5.models.pieces import PieceType
from xo_connect5.routers.boards.players import PlayersParam

router = APIRouter()


def check_board_is_ready(board: Board) -> bool:
    if board.status not in [BoardStatus.STARTING]:
        return False
    return True


def check_piece_is_exist(board: Board, point: Point) -> bool:
    piece = board.pieces[point.column][point.raw]
    if piece == PieceType.NONE:
        return False
    return True


def check_connect5(board) -> bool:
    return False


@router.put('/')
async def put_piece(point: Point = Depends(), players_param: PlayersParam = Depends()) -> Board:
    _, board = players_param.order, players_param.board
    piece_type = PieceType.XG
    _ = players_param.get_matched_user()
    if not check_board_is_ready(board):
        raise PiecesError(status_code=404, detail='board is not ready')
    elif check_piece_is_exist(board, point):
        raise PiecesError(status_code=404, detail='piece is already exist')

    board.pieces[point.column][point.raw] = piece_type
    if check_connect5(board):
        board.status = BoardStatus.END

    return board
