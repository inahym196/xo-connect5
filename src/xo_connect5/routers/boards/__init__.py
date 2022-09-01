
from fastapi import APIRouter
from xo_connect5.routers.boards import board, boards, pieces, players

router = APIRouter()
router.include_router(router=boards.router, tags=['boards'])
router.include_router(router=board.router, prefix='/{board_id}', tags=['board'])
router.include_router(router=players.router, prefix='/{board_id}/players', tags=['players'])
router.include_router(router=pieces.router, prefix='/{board_id}/pieces', tags=['pieces'])
