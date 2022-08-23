import logging

import requests
from authlib.integrations.requests_client import OAuth2Session

logger = logging.getLogger('uvicorn').getChild(__name__)


class OpenIDClient:
    def __init__(self, app_client_id: str, app_client_secret: str, auth_realm_name: str, app_redirect_uri: str, auth_issuer_url: str) -> None:

        meta_data_url = f'{auth_issuer_url}/realms/{auth_realm_name}/.well-known/openid-configuration'
        meta_data = requests.get(url=meta_data_url).json()
        self.auth_endpoint = meta_data['authorization_endpoint']
        self.userinfo_endpoint = meta_data['userinfo_endpoint']

        self.session = OAuth2Session(
            client_id=app_client_id,
            client_secret=app_client_secret,
            scope='profile',
            redirect_uri=app_redirect_uri,
            token_endpoint=meta_data['token_endpoint']
        )
