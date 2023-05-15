from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, validator, ValidationError


class UserOutSchema(BaseModel):
    id: int
    email: str
    is_active: bool
    is_superuser: bool
    last_login: datetime
    last_activity: datetime
    created: datetime

    class Config:
        orm_mode = True


class UserOutWithProfileIdSchema(UserOutSchema):
    profile_id: Optional[int] = None

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    email: EmailStr = None
    is_superuser: bool = None
    is_active: bool = None
    password: str = None


class UserLoginSchema(BaseModel):
    email: str = ''
    password: str = ''
    remember: bool = False


class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    repeat_password: str

    @validator('repeat_password')
    def validate_passwords_match(cls, value, values):
        if 'password' in values and value != values['password']:
            raise ValueError('Passwords do not match')


class UserOutWithTokenSchema(UserOutSchema):
    access_token: str = ''
    token_type: str = 'bearer'

    class Config:
        orm_mode = True


class UserOutWithTokenAndProfileIdSchema(UserOutWithTokenSchema):
    profile_id: Optional[int] = None

    class Config:
        orm_mode = True


class UserActivitySchema(BaseModel):
    id: int
    last_login: datetime = None
    last_activity: datetime = None

    class Config:
        orm_mode = True
