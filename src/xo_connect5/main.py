import logging

import uvicorn
from fastapi import FastAPI
from src.xo_connect5.routers import pieces
from starlette.responses import JSONResponse

logger = logging.getLogger('uvicorn')

app = FastAPI()
app.include_router(pieces.router)


@app.get('/turn')
async def get_turn() -> JSONResponse:
    return JSONResponse(content=pieces.board.turn)


def main():
    uvicorn.run('src.xo_connect5.main:app', reload=True, port=8000)


if __name__ == '__main__':
    main()
