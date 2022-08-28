
from xo_connect5.models import Point
from xo_connect5.models.boards import Board
from xo_connect5.models.pieces import PieceType
from xo_connect5.models.users import OrderType


class ApplicationError(Exception):
    def __init__(self, detail) -> None:
        self.detail = detail


def check_board_is_ready() -> bool:
    return True


def put_piece(board: Board, order: OrderType, point: Point):
    if not check_board_is_ready():
        raise ApplicationError(detail='board is not ready')
    board.pieces[point.column][point.raw] = PieceType.XG
    return

# if not put_piece_param.piece_type:
#     raise BoardError(detail='Piece type does not exist for the specified user')
# elif self.pieces[column][raw] != PieceType.NONE:
#     raise BoardError(detail='A piece already exists at the specified location')
