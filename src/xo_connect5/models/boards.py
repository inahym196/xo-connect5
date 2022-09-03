
from enum import Enum
from typing import Optional

from pydantic import BaseModel
from xo_connect5.models.pieces import Pieces, PieceType
from xo_connect5.models.users import OrderType, Players


class BoardStatus(str, Enum):
    WAITING = 'waiting'
    STARTING = 'starting'
    END = 'end'


class Board(BaseModel):
    id: int
    pieces: Pieces = [[PieceType.NONE for j in range(10)] for i in range(10)]
    turn: int = 0
    status: BoardStatus = BoardStatus.WAITING
    players: Players = Players()
    winner: Optional[OrderType] = None
