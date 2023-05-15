import logging
import os
import sys
from distutils.util import strtobool
from pathlib import Path

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig

BASE_DIR = Path(__file__).resolve().parent.parent


logging.basicConfig(level=logging.DEBUG)
logging.getLogger('multipart').setLevel(logging.WARNING)
logging.getLogger('faker').setLevel(logging.WARNING)
logging.getLogger('passlib').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

env_path = BASE_DIR.parent.parent / 'deploy' / '.env_local'
if env_path.exists():
    logger.debug('Loading env from .env_local file (dev environment)')
    load_dotenv(env_path)


class Settings:
    PROJECT_TITLE: str = 'Social_app'
    PROJECT_VERSION: str = '0.0.1'

    POSTGRES_USER: str = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_SERVER: str = os.getenv('POSTGRES_SERVER')
    POSTGRES_PORT: str = os.getenv('POSTGRES_PORT')
    POSTGRES_DB: str = os.getenv('POSTGRES_DB')
    DATABASE_URL: str = f"postgresql://" \
                        f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    ACCESS_TOKEN_EXPIRE_MINUTES_LONG = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES_LONG'))
    JWT_SECRET = os.getenv('JWT_SECRET')
    JWT_ALGORITHM = 'HS256'
    API_URL_PREFIX: str = '/api/v1'

    FRONTEND_URL: str = os.getenv('FRONTEND_URL', 'http://127.0.0.1')

    UPLOADS_PATH = BASE_DIR / Path('uploads')

    SEND_EMAILS = strtobool(os.getenv('SEND_EMAILS', 'True'))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_FROM_NAME = os.getenv('MAIL_FROM_NAME')
    MAIL_TLS = strtobool(os.getenv('MAIL_TLS', 'True'))
    MAIL_SSL = strtobool(os.getenv('MAIL_SSL', 'False'))
    MAIL_USE_CREDENTIALS = strtobool(os.getenv('MAIL_USE_CREDENTIALS', 'True'))
    MAIL_VALIDATE_CERTS = strtobool(os.getenv('MAIL_VALIDATE_CERTS', 'True'))

    email_conf = ConnectionConfig(
        MAIL_USERNAME=MAIL_USERNAME,
        MAIL_PASSWORD=MAIL_PASSWORD,
        MAIL_FROM=MAIL_FROM,
        MAIL_PORT=MAIL_PORT,
        MAIL_SERVER=MAIL_SERVER,
        MAIL_FROM_NAME=MAIL_FROM_NAME,
        MAIL_STARTTLS=MAIL_TLS,
        MAIL_SSL_TLS=MAIL_TLS,
        USE_CREDENTIALS=MAIL_USE_CREDENTIALS,
        VALIDATE_CERTS=MAIL_VALIDATE_CERTS,
        SUPPRESS_SEND=not SEND_EMAILS,
        TEMPLATE_FOLDER=Path(__file__).parent.parent / 'templates'
    )

    FIRST_SUPERUSER_EMAIL: str = os.getenv('FIRST_SUPERUSER_EMAIL')
    FIRST_SUPERUSER_PASSWORD: str = os.getenv('FIRST_SUPERUSER_PASSWORD')
    DEFAULT_USER_PASSWORD = FIRST_SUPERUSER_PASSWORD

    NUMBER_OF_USERS = int(os.getenv('NUMBER_OF_USERS'))
    MAX_POSTS_PER_USER = int(os.getenv('MAX_POSTS_PER_USER'))
    MAX_LIKES_PER_USER = int(os.getenv('MAX_LIKES_PER_USER'))


settings = Settings()
