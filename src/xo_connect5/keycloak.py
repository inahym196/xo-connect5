import ast
import hashlib
import os
from typing import Optional
from urllib.parse import urlencode, urljoin

import requests
from starlette.responses import JSONResponse, RedirectResponse


class KeyCloak:
    def __init__(self, app_base_url: str, keycloak_base_url: str, app_client_id: str, app_client_secret: Optional[str], keycloak_realm_name: str, app_redirect_uri: str) -> None:
        self.app_base_url = app_base_url
        self.keycloak_base_url = keycloak_base_url
        self.app_client_id = app_client_id
        self.app_client_secret = app_client_secret
        self.keycloak_realm_name = keycloak_realm_name
        self.app_redirect_url = app_redirect_uri

        self.auth_base_url = urljoin(self.keycloak_base_url,
                                     f'realms/{self.keycloak_realm_name}/protocol/openid-connect/auth')
        self.token_url = urljoin(self.keycloak_base_url,
                                 f'realms/{self.keycloak_realm_name}/protocol/openid-connect/token')

    def assemble_redirect_url(self) -> RedirectResponse:
        state = hashlib.sha256(os.urandom(32)).hexdigest()
        params = urlencode({
            'client_id': self.app_client_id,
            'redirect_uri': self.app_redirect_url,
            'state': state,
            'response_type': 'code'
        })
        auth_url = f'{self.auth_base_url}?{params}'
        response = RedirectResponse(auth_url)
        response.set_cookie(key="AUTH_STATE", value=state)
        print(response.body)
        return response

    def retrieve_token(self, code: str):
        params: dict[str, Optional[str]] = {
            'client_id': self.app_client_id,
            'client_secret': self.app_client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': self.app_redirect_url,
            'code': code
        }
        post_content: str = requests.post(self.token_url, params, verify=False).content.decode('utf-8')
        token_response = JSONResponse(content=ast.literal_eval(post_content))
        return token_response
