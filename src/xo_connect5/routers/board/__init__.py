
from fastapi import APIRouter
from xo_connect5.routers.board import boards, pieces

router = APIRouter()
router.include_router(router=boards.router, tags=['board'])
router.include_router(router=pieces.router, prefix='/pieces', tags=['pieces'])
