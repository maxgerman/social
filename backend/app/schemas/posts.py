from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic.utils import GetterDict


class PostBaseSchema(BaseModel):
    text: str
    file_uuid: Optional[UUID]
    created: datetime
    profile_id: int


class PostInSchema(PostBaseSchema):
    pass


class PostIdSchema(BaseModel):
    id: int


class PostOutSchema(PostBaseSchema, PostIdSchema):
    pass

    class Config:
        orm_mode = True


class PostLikeCountGetter(GetterDict):
    def get(self, key, default=None):
        if key == 'like_count':
            return len(self._obj.likes)
        return super().get(key, default)


class PostOutWithLikesSchema(PostOutSchema):
    like_count: int = 0

    class Config:
        orm_mode = True
        getter_dict = PostLikeCountGetter
