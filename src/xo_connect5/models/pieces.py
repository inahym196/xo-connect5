from enum import Enum

from pydantic import BaseModel


class PieceType(str, Enum):
    XP = 'xp'
    OP = 'op'
    XG = 'xg'
    OG = 'og'
    NONE = ''


class Piece(BaseModel):
    type: PieceType


Pieces = list[list[PieceType]]
