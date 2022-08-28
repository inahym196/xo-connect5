
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from src.xo_connect5.board import Board, PutPieceParam
from starlette.responses import JSONResponse

router = APIRouter()
board = Board()


@router.get('/pieces')
async def init_piece() -> JSONResponse:
    return JSONResponse({'pieces': board.pieces})


@router.put('/pieces')
async def put_piece(put_piece_param: PutPieceParam = Depends()) -> JSONResponse:
    if not put_piece_param.piece_type:
        raise HTTPException(status_code=404)
    board.put_piece(put_piece_param)

    return JSONResponse({'pieces': board.pieces})
