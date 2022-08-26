
import logging

import uvicorn
from fastapi import FastAPI
from starlette.requests import Request

logger = logging.getLogger('uvicorn')


app = FastAPI()


@app.get('/auth/login')
async def login():
    return


@app.get("/auth/callback")
async def auth(request: Request, code: str, state: str):
    return


def main():
    uvicorn.run(app)


if __name__ == '__main__':
    main()
