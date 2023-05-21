from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import crud
from core.auth import authenticate
from core.security import verify_password
from models import User
from schemas.users import UserRegisterSchema, UserUpdateSchema
from tests.utils.utils import random_email, random_lower_string


def test_create_user_and_profile(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserRegisterSchema(email=email, password=password, repeat_password=password)
    user = crud.create_user_and_profile(db, user_in=user_in)
    assert user.email == email
    assert user.password != user_in.password
    assert user.profile
    assert not user.is_superuser
    assert user.last_activity
    assert user.last_login
    assert user.created


def test_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserRegisterSchema(email=email, password=password, repeat_password=password)
    user = crud.create_user_and_profile(db, user_in=user_in)
    authenticated_user = authenticate(email=email, password=password, db=db)
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = authenticate(email=email, password=password, db=db)
    assert user is None


def test_check_if_user_is_active(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserRegisterSchema(email=email, password=password, repeat_password=password)
    user = crud.create_user_and_profile(db, user_in=user_in)
    assert user.is_active is True


def test_get_user_and_profile_id_by_user_id(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserRegisterSchema(email=email, password=password, repeat_password=password)
    user = crud.create_user_and_profile(db, user_in=user_in)
    user_id = user.id
    user, profile_id = crud.get_user_and_profile_id_by_user_id(db, user_id)
    assert isinstance(user, User)
    assert isinstance(profile_id, int)


def test_get_user_by_id(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserRegisterSchema(email=email, password=password, repeat_password=password)
    user = crud.create_user_and_profile(db, user_in=user_in)

    user_2 = crud.get_user_by_id(db, user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_get_user_by_email(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserRegisterSchema(email=email, password=password, repeat_password=password)
    user = crud.create_user_and_profile(db, user_in=user_in)

    user_2 = crud.get_user_by_email(db, user.email)
    assert user_2
    assert user.id == user_2.id
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_update_user_hash_password(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserRegisterSchema(email=email, password=password, repeat_password=password)
    user = crud.create_user_and_profile(db, user_in=user_in)

    new_email = random_email()
    new_password = random_lower_string()
    user_upd = UserUpdateSchema(
        email=new_email,
        password=new_password
    )
    crud.update_user_by_id(db, user.id, user_upd)
    user_2 = crud.get_user_by_id(db, user.id)
    assert user_2
    assert user_2.id == user.id
    assert user_2.email == new_email
    assert user_2.password != new_password
    assert verify_password(new_password, user_2.password)
