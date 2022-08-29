
from fastapi import FastAPI
from fastapi.requests import Request
from starlette.responses import JSONResponse

from xo_connect5.exceptions.players import PlayersError


def include_handler(app: FastAPI):
    app.add_exception_handler(PlayersError, players_handler)


def players_handler(request: Request, exc: PlayersError):
    return JSONResponse(status_code=exc.status_code, content={'detail': exc.detail})
