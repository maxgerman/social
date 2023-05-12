from datetime import datetime

from pydantic import BaseModel

from schemas.posts import PostOutSchema
from schemas.profiles import ProfileOutSchema


class LikeOutSchema(BaseModel):
    id: int
    profile_id: int
    profile: ProfileOutSchema
    post: PostOutSchema
    created: datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }
