from datetime import datetime
import logging
from typing import Optional

from fastapi import Depends, HTTPException, Path
from jose import JWTError
from sqlalchemy.orm import Session, joinedload
from starlette import status

from core.auth import oauth2_scheme, jwt_decode
from db.session import get_db
from models.profiles import Profile
from models.users import User

logger = logging.getLogger(__name__)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get current user by JWT token in Authorization header. If token expired, 401"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    if not token:
        raise credentials_exception
    try:
        token_data = jwt_decode(token)
    except JWTError:
        raise credentials_exception
    user = db.query(User).options(joinedload(User.profile)).filter(User.id == token_data.get('sub')).first()
    if not user or not user.is_active:
        raise credentials_exception
    user.last_activity = datetime.now()
    db.add(user)
    db.commit()
    return user


def get_current_user_or_none(token: str = Depends(oauth2_scheme),
                             db: Session = Depends(get_db)):
    """Return user or None if no token is provided"""
    if not token:
        return
    return get_current_user(token=token, db=db)


def get_current_profile_or_none(user: User = Depends(get_current_user), db: Session = Depends(get_db)
                                ) -> Optional[Profile]:
    if not user.profile:
        return None
    return user.profile


def get_current_profile(profile: Optional[Profile] = Depends(get_current_profile_or_none),
                        db: Session = Depends(get_db)) -> Profile:
    if not profile:
        raise HTTPException(status_code=400, detail='No profile exists for this user')
    return profile


def super_user(user: User = Depends(get_current_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail='You are not superuser')
    return user
