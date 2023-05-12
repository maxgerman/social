from fastapi import APIRouter

from app.api.v1.auth import auth
from app.api.v1.users import users
from app.api.v1.profiles import profiles
from app.api.v1.storage import storage
from app.api.v1.posts import posts
from app.core.config import settings

api_router = APIRouter()
url_prefix = settings.API_URL_PREFIX

api_router.include_router(auth.router, prefix=url_prefix + "/auth", tags=["auth"])
api_router.include_router(users.router, prefix=url_prefix + "/users", tags=["users"])
api_router.include_router(profiles.router, prefix=url_prefix + "/profiles", tags=["profiles"])
api_router.include_router(storage.router, prefix=url_prefix + "/storage", tags=["storage"])
api_router.include_router(posts.router_common, prefix=url_prefix + "/posts", tags=["posts"])
api_router.include_router(posts.router_create, prefix=url_prefix + "/posts", tags=["posts"])
