import logging

import requests
from authlib.integrations.requests_client import OAuth2Session
from starlette.responses import RedirectResponse

logger = logging.getLogger('uvicorn').getChild(__name__)


class OpenIDClient:
    def __init__(self, app_client_id: str, app_client_secret: str, auth_realm_name: str, app_redirect_uri: str, auth_issuer_url: str) -> None:

        meta_data_url = f'{auth_issuer_url}/realms/{auth_realm_name}/.well-known/openid-configuration'
        meta_data = requests.get(url=meta_data_url).json()
        self.auth_endpoint = meta_data['authorization_endpoint']

        self.client = OAuth2Session(
            client_id=app_client_id,
            client_secret=app_client_secret,
            scope='profile',
            redirect_uri=app_redirect_uri,
            token_endpoint=meta_data['token_endpoint']
        )

    def create_redirect_response(self) -> RedirectResponse:
        uri, state = self.client.create_authorization_url(url=self.auth_endpoint)
        response = RedirectResponse(uri)
        response.set_cookie(key='AUTH_STATE', value=state)
        return response

    def retrieve_token(self, code: str, state: str) -> str:
        token = self.client.fetch_access_token(code=code, state=state)
        return token
