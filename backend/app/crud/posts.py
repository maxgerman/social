from typing import Optional, Literal
from uuid import UUID

import sqlalchemy.exc
from sqlalchemy import select, func, orm
from sqlalchemy.orm import Session

from models import Post, Following, Like


def query_all_posts_sorted_by(db: Session, sort_by: Literal['new', 'likes']):
    if sort_by == 'new':
        query = db.query(Post).order_by(Post.id.desc())
    elif sort_by == 'likes':
        post_likes_sq = select(Post.id, func.count(Post.id).label('like_count')).outerjoin(Post.likes).group_by(
            Post.id).subquery()
        query = db.query(Post
                         ).join(post_likes_sq, Post.id == post_likes_sq.c.id
                                ).order_by(post_likes_sq.c.like_count.desc())
    else:
        raise ValueError('Invalid sort string')
    return query


def filter_posts_query(query: orm.Query,
                       filter_by: Literal['all', 'feed'], profile_id: int):
    if filter_by == 'feed':
        subs_sq = select(Following.profile_whom_id
                         ).where(Following.profile_by_id == profile_id)
        query = query.filter(Post.profile_id.in_(subs_sq))

    elif filter_by == 'all':
        pass

    else:
        raise ValueError('Invalid filter string')
    return query


def filter_posts_query_by_profile_id(query: orm.Query, profile_id: int):
    return query.filter(Post.profile_id == profile_id)


def get_post_by_id(db: Session, post_id: int) -> Optional[Post]:
    post = db.query(Post).filter(Post.id == post_id).first()
    return post


def like_post(db: Session, post_id: int, profile_id: int) -> bool:
    like = Like(post_id=post_id, profile_id=profile_id)
    db.add(like)
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return False
    return True


def unlike_post(db: Session, post_id: int, profile_id: int) -> bool:
    like = db.query(Like).filter(Like.post_id == post_id, Like.profile_id == profile_id).first()
    if not like:
        return False
    db.delete(like)
    db.commit()
    return True


def create_post(db: Session, profile_id: int, text: str,
                file_uuid: UUID = None):
    post = Post(profile_id=profile_id, text=text, file_uuid=file_uuid)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
