
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from xo_connect5.exceptions.app import ApplicationError
from xo_connect5.exceptions.pieces import PiecesError
from xo_connect5.exceptions.players import PlayersError


def include_handler(app: FastAPI):
    app.add_exception_handler(PlayersError, players_handler)
    app.add_exception_handler(PiecesError, pieces_handler)


def players_handler(request: Request, exc: PlayersError):
    return JSONResponse(status_code=exc.status_code, content={'detail': exc.detail})


def pieces_handler(request: Request, exc: PiecesError):
    return JSONResponse(status_code=exc.status_code, content={'detail': exc.detail})


def app_handler(request: Request, exc: ApplicationError):
    return JSONResponse(status_code=exc.status_code, content={'detail': exc.detail})
