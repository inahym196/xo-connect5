
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class OrderType(str, Enum):
    FIRST = 'first'
    DRAW = 'draw'
    NONE = 'none'


class User(BaseModel):
    name: str


class UserInDB(BaseModel):
    name: str
    order: OrderType = OrderType.NONE


class Players(BaseModel):
    first: Optional[User] = None
    draw: Optional[User] = None
