
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

LENGTH_OF_SIDE = 10


class PieceType(str, Enum):
    XP = 'xp'
    OP = 'op'
    XG = 'xg'
    OG = 'og'
    NONE = '_'


class Piece(BaseModel):
    type: PieceType


class OrderType(str, Enum):
    FIRST = 'first'
    DRAW = 'draw'


class Point(BaseModel):
    raw: int = Field(ge=0, lt=LENGTH_OF_SIDE)
    column: int = Field(ge=0, lt=LENGTH_OF_SIDE)


class User(BaseModel):
    name: str


class BoardStatus(str, Enum):
    NOT_READY = 'not ready'
    READY = 'ready'
    STARTING = 'starting'
    END = 'end'


class Board(BaseModel):
    id: int
    pieces: Optional[list[list[PieceType]]] = None
    round: Optional[int] = None
    status: BoardStatus = BoardStatus.NOT_READY


class Boards(BaseModel):
    items: list[Board] = list()
