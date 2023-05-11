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
logger = logging.getLogger(__name__)

env_path = BASE_DIR.parent.parent / 'deploy' / '.env_local'
if not env_path.exists():
    env_path = BASE_DIR.parent.parent / 'deploy' / '.env'
if not env_path.exists():
    logger.warning(f'env file not found: {env_path}')
    sys.exit(1)

load_dotenv(env_path)
logger.debug(f'loaded env from {env_path}')


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

    CHAT_FILE_UPLOAD_MAX_SIZE = int(os.getenv('CHAT_FILE_UPLOAD_MAX_SIZE'))

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


settings = Settings()
