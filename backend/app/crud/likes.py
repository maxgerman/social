from datetime import datetime, date

from sqlalchemy import orm, cast, Date, func
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from models import Post, Like


def get_likes_query_by_profile_id(db: Session, profile_id: int) -> orm.Query:
    posts_ids = select(Post.id).where(Post.profile_id == profile_id)
    likes_query = db.query(Like).options(joinedload(Like.profile)).options(joinedload(Like.post)).filter(
        Like.post_id.in_(posts_ids)).order_by(Like.id.desc())
    return likes_query


def like_exists(db: Session, post_id: int, profile_id: int) -> bool:
    like = db.query(Like).filter(Like.post_id == post_id, Like.profile_id == profile_id).first()
    return like is not None


def validate_date_range(date_from: str, date_to: str) -> tuple[date, date]:
    if date_from is None or date_to is None:
        raise ValueError('Date range is not specified')
    if date_from > date_to:
        raise ValueError('Invalid date range')
    try:
        date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        date_to = datetime.strptime(date_to, '%Y-%m-%d').date()

    except ValueError:
        raise ValueError('Invalid date format')
    return date_from, date_to


def get_likes_analytics_query(db: Session, date_from: date, date_to: date):
    query = db.query(
        cast(Like.created, Date).label('date'),
        func.count(Like.id).label('like_count')
    ).filter(
        cast(Like.created, Date) >= date_from,
        cast(Like.created, Date) <= date_to
    ).group_by(cast(Like.created, Date)).order_by(cast(Like.created, Date))
    return query
