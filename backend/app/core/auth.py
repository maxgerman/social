from datetime import datetime, timedelta
from typing import Optional, MutableMapping, List, Union

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm.session import Session

from app.core.config import settings
from app.core.security import verify_password
from app.models.users import User

JWTPayloadMapping = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_URL_PREFIX}/auth/login", auto_error=False)


def authenticate(
        *,
        email: str,
        password: str,
        db: Session,
) -> Optional[User]:
    """Authenticate user by email and password. Return user or None"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(*, sub: str, remember=False) -> str:  # 2
    if remember:
        token_period = settings.ACCESS_TOKEN_EXPIRE_MINUTES_LONG
    else:
        token_period = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=token_period),
        sub=sub,
    )


def create_pwd_reset_token(sub: str, extra: dict = None) -> str:
    """Create password reset token. Uses 'extra' dict with last login date."""
    return _create_token(
        token_type="pwd_reset_token",
        lifetime=timedelta(hours=24),
        sub=sub,
        extra=extra,
    )


def _create_token(
        token_type: str,
        lifetime: timedelta,
        sub: str,
        extra: dict = None,
) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = str(sub)
    if extra:
        payload.update(extra)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def jwt_decode(token):
    """Decode and verify JWT token. For last_login verification, also use 'verify_last_login'"""
    options = {'verify_exp': True}
    payload = jwt.decode(token, settings.JWT_SECRET, settings.JWT_ALGORITHM, options=options)
    return payload


def verify_last_login(token_data: dict, last_login: str) -> bool:
    if 'jti' not in token_data or token_data['jti'] != last_login:
        return False
    return True
