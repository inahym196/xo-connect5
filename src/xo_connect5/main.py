
import logging

import uvicorn
from fastapi import FastAPI
from src.xo_connect5 import settings
from src.xo_connect5.openid_client import OpenIDClient
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

logger = logging.getLogger('uvicorn')

openid_client = OpenIDClient(
    app_client_id=settings.APP_CLIENT_ID,
    app_client_secret=settings.APP_CLIENT_SECRET,
    app_redirect_uri=settings.APP_REDIRECT_URI,
    auth_issuer_url=settings.AUTH_ISSUER_URL,
    auth_realm_name=settings.AUTH_SERVER_REALM_NAME,
)

app = FastAPI()


@app.get('/auth/login')
async def login() -> RedirectResponse:
    response = openid_client.create_redirect_response()
    return response


@app.get("/auth/callback")
async def auth(request: Request, code: str, state: str) -> JSONResponse:
    if state != request.cookies.get("AUTH_STATE"):
        return JSONResponse(content={"error": "state_verification_failed"}, status_code=401)
    token = openid_client.retrieve_token(code, state)
    return JSONResponse(content=token)


def main():
    uvicorn.run(app)


if __name__ == '__main__':
    main()
