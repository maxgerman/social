from sqlalchemy.orm import Session

from ..core.security import get_password_hash
from ..models.users import User
from ..models.profiles import Profile
from ..schemas.users import UserRegisterSchema


def create_user_and_profile(db: Session, user_in: UserRegisterSchema):
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


def get_user_by_id(db: Session, user_id: int):
    """Return user by id or None"""
    return db.query(User).filter(User.id == user_id).first()
