

from pydantic import BaseModel, Field

LENGTH_OF_SIDE = 10


class Point(BaseModel):
    raw: int = Field(ge=0, lt=LENGTH_OF_SIDE)
    column: int = Field(ge=0, lt=LENGTH_OF_SIDE)
