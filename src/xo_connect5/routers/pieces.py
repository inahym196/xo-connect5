
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from src.xo_connect5.board import Board, BoardError, PutPieceParam
from starlette.responses import JSONResponse

router = APIRouter()
board = Board()


@router.get('/pieces')
async def init_piece() -> JSONResponse:
    return JSONResponse({'pieces': board.pieces})


@router.put('/pieces')
async def put_piece(put_piece_param: PutPieceParam = Depends()) -> JSONResponse:
    try:
        board.put_piece(put_piece_param)
    except BoardError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    return JSONResponse({'pieces': board.pieces})
