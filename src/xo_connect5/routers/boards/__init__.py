
from fastapi import APIRouter
from xo_connect5.routers.boards import board, boards

router = APIRouter()
router.include_router(router=boards.router, tags=['boards'])
router.include_router(router=board.router, prefix='/{board_id}', tags=['board'])
