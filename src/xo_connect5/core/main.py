
from xo_connect5.exceptions.app import ApplicationError
from xo_connect5.models import Point
from xo_connect5.models.boards import Board, BoardStatus
from xo_connect5.models.pieces import PieceType
from xo_connect5.models.users import Order


def check_board_is_ready(board: Board) -> bool:
    if board.status not in [BoardStatus.STARTING]:
        return False
    return True


def put_piece(board: Board, order: Order, point: Point):
    if check_board_is_ready(board):
        raise ApplicationError(detail='board is not ready')
        ...
    board.pieces[point.column][point.raw] = PieceType.XG
    return

# if not put_piece_param.piece_type:
#     raise BoardError(detail='Piece type does not exist for the specified user')
# elif self.pieces[column][raw] != PieceType.NONE:
#     raise BoardError(detail='A piece already exists at the specified location')
