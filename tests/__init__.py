
from fastapi.testclient import TestClient
from xo_connect5.main import app

client = TestClient(app)
