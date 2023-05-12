import uuid
from typing import Optional, Literal

from pydantic import BaseModel


class ProfileOutSchema(BaseModel):
    id: int
    user_id: int
    name: str
    image_id: Optional[uuid.UUID]
    bio: str
    gender: str | None

    class Config:
        orm_mode = True


class ProfileUpdateSchema(BaseModel):
    name: str = ''
    image_id: Optional[uuid.UUID] = None
    bio: str = ''
    gender: Literal['MALE', 'FEMALE'] | None = None


class ProfileOutWithPostsCountSchema(ProfileOutSchema):
    posts_count: int = 0

    class Config:
        orm_mode = True
