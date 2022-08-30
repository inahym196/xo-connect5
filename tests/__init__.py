
from fastapi.exceptions import HTTPException
from fastapi.testclient import TestClient
from xo_connect5.main import app

client = TestClient(app)

http_exception_404 = HTTPException(status_code=404)
http_exception_409 = HTTPException(status_code=409)
