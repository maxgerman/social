from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from core.config import settings
from db.base_class import Base
from db.session import get_db
from main import app

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


def override_get_db():
    try:
        db = SessionLocalTest()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
