
from enum import Enum
from typing import Optional

from pydantic import BaseModel
from xo_connect5.models.pieces import PieceType
from xo_connect5.models.users import User


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
    players: Optional[tuple[User, User]] = None


class Boards(BaseModel):
    items: list[Board] = list()
