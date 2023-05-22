import sqlalchemy.exc
from fastapi import HTTPException
from fastapi_paginate.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from core.config import settings
from core.pagination import CustomParams
from core.security import get_password_hash
from models.profiles import Profile
from models.users import User
from schemas.users import UserRegisterSchema, UserUpdateSchema


def create_user_and_profile(db: Session, user_in: UserRegisterSchema) -> User:
    """Creates user and profile"""
    password_hash = get_password_hash(user_in.password)
    user_db = User(email=user_in.email, password=password_hash)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    profile = Profile(user_id=user_db.id)
    db.add(profile)
    db.commit()
    return user_db


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Return user by id or None"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Return user by email or None"""
    return db.query(User).filter(User.email == email).first()


def get_user_and_profile_id_by_user_id(db: Session, user_id: int
                                       ) -> tuple[User | None, int | None]:
    """Return user and profile by id or None"""
    if res := db.query(User, Profile.id
                       ).join(Profile, User.id == Profile.user_id, isouter=True
                              ).filter(User.id == user_id).first():
        user, profile_id = res
        return user, profile_id
    else:
        return None, None


def get_all_users_paginated(db: Session, params: CustomParams, asc: bool):
    """Return all users paginated"""
    users = db.query(User)
    if asc:
        users = users.order_by(User.id)
    else:
        users = users.order_by(User.id.desc())
    page = paginate(users, params)
    return page


def update_user_by_id(db: Session, user_id: int, user_in: UserUpdateSchema):
    """Update user by id"""
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    for field, value in user_in.dict(exclude_unset=True).items():
        if field == 'password':
            value = get_password_hash(value)
        setattr(user, field, value)
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")
    db.refresh(user)
    return user


def get_or_create_first_superuser(db: Session) -> User:
    su = get_user_by_email(db, settings.FIRST_SUPERUSER_EMAIL)
    if not su:
        su = create_user_and_profile(db, UserRegisterSchema(
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            repeat_password=settings.FIRST_SUPERUSER_PASSWORD
        ))
        su.is_superuser = True
        db.add(su)
        db.commit()
    return su
