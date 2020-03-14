import os


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


API_V1_STR = "/api"
BASE_URL = 'https://helpdesk.innopolis.university/api/'

SECRET_KEY = os.getenvb(b"SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = os.urandom(32)

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

PROJECT_NAME = os.getenv("PROJECT_NAME")

POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
)

FIRST_SUPERUSER = os.getenv("FIRST_SUPERUSER")
FIRST_SUPERUSER_PASSWORD = os.getenv("FIRST_SUPERUSER_PASSWORD")

USERS_OPEN_REGISTRATION = getenv_boolean("USERS_OPEN_REGISTRATION")

# oAuth credentials
OAUTH_APP_ID = os.getenv("oauth_appID")
OAUTH_SHARED_SECRET = os.getenv("oauth_shared_secret")
OAUTH_AUTHORIZATION_BASE_URL = os.getenv("oauth_authorization_baseURL")
OAUTH_GET_INFO_URL = os.getenv("oauth_get_infoURL")
OAUTH_TOKEN_URL = os.getenv("oauth_tokenURL")
OAUTH_END_SESSION_ENDPOINT = os.getenv("oauth_end_session_endpoint")
