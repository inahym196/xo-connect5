
import logging

import requests
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
    uri, state = openid_client.session.create_authorization_url(url=openid_client.auth_endpoint)
    response = RedirectResponse(uri)
    response.set_cookie(key='AUTH_STATE', value=state)
    return response


@app.get("/auth/callback")
async def auth(request: Request, code: str, state: str) -> JSONResponse:
    if state != request.cookies.get("AUTH_STATE"):
        return JSONResponse(content={"error": "state_verification_failed"}, status_code=401)
    token: dict[str, str] = openid_client.session.fetch_access_token(code=code, state=state)
    access_token = token['access_token']
    res = requests.get(url=openid_client.userinfo_endpoint,
                       headers={'Authorization': f'Bearer {access_token}'}
                       )
    logger.info(res.json())
    return JSONResponse(content=token)


def main():
    uvicorn.run(app)


if __name__ == '__main__':
    main()
