import uvicorn
from fastapi import FastAPI
from src.xo_connect5 import settings
from src.xo_connect5.keycloak import KeyCloak
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

keycloak = KeyCloak(
    app_base_url=settings.APP_BASE_URL,
    keycloak_base_url=settings.KEYCLOAK_BASE_URL_LOCALHOST,
    app_client_id=settings.APP_CLIENT_ID,
    app_client_secret=settings.APP_CLIENT_SECRET,
    keycloak_realm_name=settings.KEYCLOAK_REALM_NAME,
    app_redirect_uri=settings.APP_REDIRECT_URI
)


app = FastAPI()


@app.get('/auth/login')
async def login() -> RedirectResponse:
    response = keycloak.assemble_redirect_url()
    return response


@app.get("/auth/callback")
async def auth(request: Request, code: str, state: str) -> JSONResponse:
    if state != request.cookies.get("AUTH_STATE"):
        return JSONResponse(content={"error": "state_verification_failed"}, status_code=401)
    token = keycloak.retrieve_token(code)
    return token


def main():
    uvicorn.run(app)


if __name__ == '__main__':
    main()
