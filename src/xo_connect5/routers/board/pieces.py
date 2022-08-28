
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.responses import JSONResponse
from xo_connect5.board import Board, BoardError, PutPieceParam

router = APIRouter()
board = Board()


@router.get('/')
async def init_piece() -> JSONResponse:
    return JSONResponse({'pieces': board.pieces})


@router.put('/')
async def put_piece(put_piece_param: PutPieceParam = Depends()) -> JSONResponse:
    try:
        board.put_piece(put_piece_param)
    except BoardError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    return JSONResponse({'pieces': board.pieces})
