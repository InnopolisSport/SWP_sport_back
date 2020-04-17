import os

import pytz


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


SC_TRAINERS_GROUP_NAME = "SC trainers"
BACHELOR_PREFIX = "B"
TIMEZONE = pytz.timezone("Europe/Moscow")

DEBUG = FAKE_LOGIN = getenv_boolean("DEBUG", False)

API_V1_STR = "/api"
DOCS_STR = "/docs"
REDOC_STR = "/redoc"
BASE_URL = 'https://helpdesk.innopolis.university'
BASE_LOCAL_URL = 'http://188.130.155.115'
API_BASE_URL = BASE_URL + API_V1_STR
DOCS_BASE_URL = BASE_URL + DOCS_STR
REDOC_BASE_URL = BASE_URL + REDOC_STR

SECRET_KEY = os.getenvb(b"SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = os.urandom(32)

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

PROJECT_NAME = os.getenv("PROJECT_NAME")

POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# oAuth credentials
OAUTH_APP_ID = os.getenv("oauth_appID")
OAUTH_SHARED_SECRET = os.getenv("oauth_shared_secret")
OAUTH_AUTHORIZATION_BASE_URL = os.getenv("oauth_authorization_baseURL")
OAUTH_GET_INFO_URL = os.getenv("oauth_get_infoURL")
OAUTH_TOKEN_URL = os.getenv("oauth_tokenURL")
OAUTH_END_SESSION_ENDPOINT = os.getenv("oauth_end_session_endpoint")
