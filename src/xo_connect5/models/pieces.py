
from typing import Literal

from pydantic import BaseModel, Field
from typing_extensions import TypeAlias

NonePieceType: TypeAlias = Literal['']
PurplePieceType: TypeAlias = Literal['xp', 'op']
GreenPieceType: TypeAlias = Literal['xg', 'og']
PieceType: TypeAlias = Literal[PurplePieceType, GreenPieceType, NonePieceType]
Pieces: TypeAlias = list[list[PieceType]]

none_piece_type: NonePieceType = ''


class Point(BaseModel):
    raw: int = Field(ge=0, lt=10)
    column: int = Field(ge=0, lt=10)
