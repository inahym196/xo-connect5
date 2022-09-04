
import uvicorn
from fastapi import FastAPI

from xo_connect5 import handlers
from xo_connect5.routers import boards

app = FastAPI()
app.include_router(router=boards.router, prefix='/api/v1/boards')
handlers.include_handler(app)


def main():
    uvicorn.run('src.xo_connect5.main:app', reload=True, port=8000, reload_dirs=['src'])


if __name__ == '__main__':
    main()
