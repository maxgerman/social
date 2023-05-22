from sqlalchemy.orm import Session
from starlette.testclient import TestClient

import crud
from core.config import settings
from schemas.users import UserRegisterSchema
from tests.utils.utils import random_email, random_lower_string


def test_get_superuser_me(
        client: TestClient, superuser_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_URL_PREFIX}/auth/me", headers=superuser_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is True
    assert current_user["email"] == settings.FIRST_SUPERUSER_EMAIL


def test_users_list_and_pagination(db: Session, client: TestClient,
                                   superuser_headers: dict[str, str]) -> None:
    # add 2 users
    email = random_email()
    password = random_lower_string()
    user_in = UserRegisterSchema(email=email, password=password, repeat_password=password)
    user = crud.create_user_and_profile(db, user_in=user_in)
    email = random_email()
    password = random_lower_string()
    user_in = UserRegisterSchema(email=email, password=password, repeat_password=password)
    user = crud.create_user_and_profile(db, user_in=user_in)

    r = client.get(f'{settings.API_URL_PREFIX}/users/',
                   headers=superuser_headers)
    resp = r.json()
    assert resp['total'] >= 2
    assert resp['current_page'] == 1
    assert resp['total_pages']


def test_normal_user_cant_list_users(db: Session, client: TestClient,
                                     normal_user_headers: dict[str, str]) -> None:
    r = client.get(f'{settings.API_URL_PREFIX}/users',
                   headers=normal_user_headers)
    assert r.status_code == 403


def test_get_normal_user_me(
    client: TestClient, normal_user_headers: dict[str, str]
) -> None:
    r = client.get(f'{settings.API_URL_PREFIX}/auth/me', headers=normal_user_headers)
    current_user = r.json()
    assert current_user
    assert current_user['is_active'] is True
    assert current_user['is_superuser'] is False
