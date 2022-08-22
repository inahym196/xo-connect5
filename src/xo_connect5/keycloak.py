import ast
from urllib.parse import urljoin

import requests
from authlib.integrations.requests_client import OAuth2Session
from starlette.responses import RedirectResponse


class KeyCloak:
    def __init__(self, app_base_url: str, keycloak_base_url: str, app_client_id: str, app_client_secret: str, keycloak_realm_name: str, app_redirect_uri: str) -> None:
        self.app_base_url = app_base_url
        self.keycloak_base_url = keycloak_base_url
        self.app_client_id = app_client_id
        self.app_client_secret = app_client_secret
        self.keycloak_realm_name = keycloak_realm_name
        self.app_redirect_url = app_redirect_uri

        self.client = OAuth2Session(
            client_id=self.app_client_id,
            client_secret=self.app_client_secret,
            scope='profile',
            redirect_uri=self.app_redirect_url
        )

        self.auth_url = urljoin(self.keycloak_base_url,
                                f'realms/{self.keycloak_realm_name}/protocol/openid-connect/auth')
        self.token_url = urljoin(self.keycloak_base_url,
                                 f'realms/{self.keycloak_realm_name}/protocol/openid-connect/token')

    def create_redirect_response(self) -> RedirectResponse:
        uri, state = self.client.create_authorization_url(url=self.auth_url)
        response = RedirectResponse(uri)
        response.set_cookie(key='AUTH_STATE', value=state)
        return response

    def retrieve_token(self, code: str) -> str:
        params: dict[str, str] = {
            'client_id': self.app_client_id,
            'client_secret': self.app_client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': self.app_redirect_url,
            'code': code
        }
        post_content: str = requests.post(self.token_url, params, verify=False).content.decode('utf-8')
        token = ast.literal_eval(post_content)
        return token
