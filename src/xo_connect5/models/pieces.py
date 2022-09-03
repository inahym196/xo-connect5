from enum import Enum

from pydantic import BaseModel, Field


class PieceType(str, Enum):
    XP = 'xp'
    OP = 'op'
    XG = 'xg'
    OG = 'og'
    NONE = ''


Pieces = list[list[PieceType]]


class Point(BaseModel):
    raw: int = Field(ge=0, lt=10)
    column: int = Field(ge=0, lt=10)
