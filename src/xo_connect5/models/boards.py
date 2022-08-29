
from enum import Enum

from pydantic import BaseModel
from xo_connect5.models.pieces import Pieces, PieceType
from xo_connect5.models.users import Players


class BoardStatus(str, Enum):
    NOT_READY = 'not ready'
    WAITING = 'waiting'
    READY = 'ready'
    STARTING = 'starting'
    END = 'end'


class Board(BaseModel):
    id: int
    pieces: Pieces = [[PieceType.NONE for j in range(10)] for i in range(10)]
    round: int = 0
    status: BoardStatus = BoardStatus.NOT_READY
    players: Players = Players()


class Boards(BaseModel):
    items: list[Board] = list()
