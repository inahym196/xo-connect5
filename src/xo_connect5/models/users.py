
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class OrderType(str, Enum):
    FIRST = 'first'
    DRAW = 'draw'
    NONE = 'none'


class Order(BaseModel):
    type: OrderType = OrderType.NONE


class User(BaseModel):
    name: str


class Players(BaseModel):
    first: Optional[User] = None
    draw: Optional[User] = None
