from sqlalchemy import orm
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.pagination import CustomParams
from models import Post, Like


def get_likes_query_by_profile_id(db: Session, profile_id: int) -> orm.Query:
    posts_ids = select(Post.id).where(Post.profile_id == profile_id)
    likes_query = db.query(Like).options(joinedload(Like.profile)).options(joinedload(Like.post)).filter(
        Like.post_id.in_(posts_ids)).order_by(Like.id.desc())
    return likes_query


def like_exists(db: Session, post_id: int, profile_id: int) -> bool:
    like = db.query(Like).filter(Like.post_id == post_id, Like.profile_id == profile_id).first()
    return like is not None
