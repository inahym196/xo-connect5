import logging

import numpy
import uvicorn
from fastapi import FastAPI
from starlette.responses import JSONResponse

logger = logging.getLogger('uvicorn')


app = FastAPI()


class Board:
    def __init__(self) -> None:
        self.pieses = numpy.zeros((10, 10), dtype=int).tolist()


board = Board()


@app.get('/')
async def init_piese() -> JSONResponse:
    return JSONResponse({'pieses': board.pieses})


def main():
    uvicorn.run(app)


if __name__ == '__main__':
    main()
