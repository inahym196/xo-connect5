import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(verbose=True)
load_dotenv(dotenv_path)

APP_CLIENT_ID = os.environ["APP_CLIENT_ID"]
APP_CLIENT_SECRET = os.environ['APP_CLIENT_SECRET']
APP_REDIRECT_URI = os.environ['APP_REDIRECT_URI']
AUTH_SERVER_REALM_NAME = os.environ['AUTH_SERVER_REALM_NAME']
AUTH_SERVER_BASE_URL = os.environ["AUTH_SERVER_BASE_URL"]
