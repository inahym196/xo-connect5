import logging

import uvicorn
from fastapi import FastAPI

from xo_connect5.routers import board

logger = logging.getLogger('uvicorn')

app = FastAPI()
app.include_router(router=board.router, prefix='/api/v1/boards')


def main():
    uvicorn.run('src.xo_connect5.main:app', reload=True, port=8000)


if __name__ == '__main__':
    main()
