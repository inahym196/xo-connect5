
from enum import Enum

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
