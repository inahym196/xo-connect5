import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(verbose=True)
load_dotenv(dotenv_path)

APP_BASE_URL = os.environ["APP_BASE_URL"]
APP_CLIENT_ID = os.environ["APP_CLIENT_ID"]
APP_CLIENT_SECRET = os.environ['APP_CLIENT_SECRET']
APP_REDIRECT_URI = os.environ['APP_REDIRECT_URI']

KEYCLOAK_REALM_NAME = os.environ['KEYCLOAK_REALM_NAME']
KEYCLOAK_BASE_URL_LOCALHOST = os.environ["KEYCLOAK_BASE_URL_LOCALHOST"]
KEYCLOAK_BASE_URL_CONTAINER_NAME = os.environ["KEYCLOAK_BASE_URL_CONTAINER_NAME"]
