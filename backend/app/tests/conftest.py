import logging
from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from starlette.testclient import TestClient

import crud
from core.config import settings
from db.base_class import Base
from db.session import get_db
from main import app
from schemas.users import UserRegisterSchema
from tests.utils.user import get_superuser_headers, get_user_headers
from tests.utils.utils import random_email, random_lower_string

SQLALCHEMY_DATABASE_URL_TEST = settings.DATABASE_URL_TEST
engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST)

SessionLocalTest = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='session')
def db() -> Generator:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield SessionLocalTest()


@pytest.fixture(scope='module')
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope='module')
def superuser_headers(client: TestClient, db: Session) -> dict[str, str]:
    crud.get_or_create_first_superuser(db)
    return get_superuser_headers(client)


@pytest.fixture(scope='module')
def normal_user_headers(client: TestClient, db: Session) -> dict[str, str]:
    password = random_lower_string()
    user_in = UserRegisterSchema(
        email=random_email(),
        password=password,
        repeat_password=password
    )
    user = crud.create_user_and_profile(db, user_in)
    return get_user_headers(client, user_in.email, user_in.password)


def override_get_db():
    try:
        db = SessionLocalTest()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('asyncio').setLevel(logging.WARNING)
