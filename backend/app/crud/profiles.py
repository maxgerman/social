from typing import Optional, Literal
from uuid import UUID

import sqlalchemy.exc
from fastapi import HTTPException
from fastapi_paginate.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from sqlalchemy import select, func, orm

from models import Post, Following
from schemas.profiles import ProfileUpdateSchema
from core.pagination import CustomParams
from models.profiles import Profile

PROFILE_SORTING_TYPE = Literal['new', 'likes', 'posts']
PROFILE_FILTER_TYPE = Literal['all', 'subbed', 'followers']


def get_profile_by_id(db: Session, profile_id: int) -> Optional[Profile]:
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    return profile


def update_profile_by_id(db: Session, profile_id: int, profile_in: ProfileUpdateSchema):
    profile = get_profile_by_id(db, profile_id)
    if not profile:
        return None
    for field, value in profile_in.dict(exclude_unset=True).items():
        setattr(profile, field, value)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def get_posts_count_by_profile_id(db: Session, profile_id: int) -> int:
    """Return count of posts by profile id"""
    profile = get_profile_by_id(db, profile_id)
    return len(profile.posts)


def query_all_profiles_sorted_by(db, sort_by: PROFILE_SORTING_TYPE):
    if sort_by == 'new':
        query = db.query(Profile).order_by(Profile.id.desc())

    elif sort_by == 'likes':
        # TODO: who got the most likes (which profile)
        raise HTTPException(status_code=501, detail='Not implemented yet')

    elif sort_by == 'posts':
        subq = select(Post.profile_id, func.count(Post.id).label('post_count')).group_by(Post.profile_id).subquery()
        subq2 = select(Profile.id, func.coalesce(subq.c.post_count, 0).label('post_count')).outerjoin(
            subq, Profile.id == subq.c.profile_id).subquery()
        query = db.query(Profile).join(subq2, Profile.id == subq2.c.id).order_by(subq2.c.post_count.desc())

    else:
        raise ValueError('Invalid sort string, must be in PROFILE_SORTING_TYPE')

    return query


def filter_profiles_query(query: orm.Query,
                          filter_by: PROFILE_FILTER_TYPE, profile_id: int):
    if filter_by == 'followers':
        followers_ids_subq = select(Following.profile_by_id).where(Following.profile_whom_id == profile_id).distinct(
        ).subquery()
        query = query.filter(Profile.id.in_(followers_ids_subq))
    elif filter_by == 'subbed':
        subbed_ids_subq = select(Following.profile_whom_id).where(Following.profile_by_id == profile_id).distinct(
        ).subquery()
        query = query.filter(Profile.id.in_(subbed_ids_subq))
    elif filter_by == 'all':
        pass
    return query


def paginate_query_by_params(db: Session, query: orm.Query, params: CustomParams):
    page = paginate(query, params)
    return page


def set_profile_image_uuid(db: Session, profile_id: int, image_uuid: UUID) -> bool:
    profile = get_profile_by_id(db, profile_id)
    if not profile:
        return False
    profile.image_id = image_uuid
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return True


def delete_profile_image(db: Session, profile_id: int) -> bool:
    profile = get_profile_by_id(db, profile_id)
    if not profile:
        return False
    profile.image_id = None
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return True


def follow_profile(db: Session, profile_by_id: int, profile_whom_id: int) -> bool:
    following = Following(profile_by_id=profile_by_id, profile_whom_id=profile_whom_id)
    try:
        db.add(following)
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        return False
    return True


def unfollow_profile(db: Session, profile_by_id: int, profile_whom_id: int) -> bool:
    following = db.query(Following).filter(Following.profile_by_id == profile_by_id,
                                           Following.profile_whom_id == profile_whom_id).first()
    if not following:
        return False
    db.delete(following)
    db.commit()
    return True
