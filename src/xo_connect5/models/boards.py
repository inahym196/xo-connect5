
from enum import Enum

from pydantic import BaseModel
from xo_connect5.models.pieces import PieceType
from xo_connect5.models.users import Players


class BoardStatus(str, Enum):
    NOT_READY = 'not ready'
    READY = 'ready'
    STARTING = 'starting'
    END = 'end'


class Board(BaseModel):
    id: int
    pieces: list[list[PieceType]]
    round: int = 0
    status: BoardStatus = BoardStatus.NOT_READY
    players = Players()


class Boards(BaseModel):
    items: list[Board] = list()
