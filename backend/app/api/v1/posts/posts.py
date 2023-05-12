import logging
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
from api.v1.dependencies import get_current_profile
from core.pagination import CustomParams, CustomPage
from db.session import get_db
from models import Profile
from schemas.posts import PostOutWithLikesSchema

router_common = APIRouter()
router_create = APIRouter()
logger = logging.getLogger(__name__)


@router_common.get('/', response_model=CustomPage[PostOutWithLikesSchema])
def get_posts(db: Session = Depends(get_db),
              sort_by: Literal['new', 'likes'] = Query(default='new'),
              filter_by: Literal['all', 'feed'] = Query(default='all'),
              profile: Profile = Depends(get_current_profile),
              params: CustomParams = Depends(),
              profile_id: int = None,
              ):
    """Get posts by authenticated user. Sorting and filtering is available"""
    all_posts_sorted_query = crud.query_all_posts_sorted_by(db, sort_by)
    posts_filtered_query = crud.filter_posts_query(all_posts_sorted_query, filter_by, profile.id)
    if profile_id:
        # used in case of access via profiles/{profile_id}/posts
        posts_filtered_query = crud.filter_posts_query_by_profile_id(posts_filtered_query, profile_id)
    posts_page = crud.paginate_query_by_params(db, posts_filtered_query, params)
    return posts_page


@router_common.get('/{post_id}', response_model=PostOutWithLikesSchema)
def get_post_by_id(post_id: int,
                   db: Session = Depends(get_db),
                   profile: Profile = Depends(get_current_profile),
                   profile_id: int = None):
    """Get post by id by authenticated user"""
    post = crud.get_post_by_id(db, post_id)
    if not post or (profile_id and post.profile_id != profile_id):
        # raised too when post_is doesn't match the profile_id if accessed via profiles/{profile_id}/posts
        raise HTTPException(404, 'Post not found')
    return post


@router_common.post('/{post_id}/like')
def like_post(post_id: int,
              db: Session = Depends(get_db),
              profile: Profile = Depends(get_current_profile),
              profile_id: int = None):
    """Like post by authenticated user"""
    post = crud.get_post_by_id(db, post_id)
    if not post or (profile_id and post.profile_id != profile_id):
        # raised too when post_is doesn't match the profile_id if accessed via profiles/{profile_id}/posts
        raise HTTPException(404, 'Post not found')
    if not crud.like_post(db, post_id, profile.id):
        raise HTTPException(400, 'Post already liked')
    return {'detail': 'Post liked',
            'post_id': post_id,
            'profile_id': profile.id}


@router_common.delete('/{post_id}/like')
def unlike_post(post_id: int,
                db: Session = Depends(get_db),
                profile: Profile = Depends(get_current_profile),
                profile_id: int = None):
    """Unlike post by authenticated user"""
    post = crud.get_post_by_id(db, post_id)
    if not post or (profile_id and post.profile_id != profile_id):
        # raised too when post_is doesn't match the profile_id if accessed via profiles/{profile_id}/posts
        raise HTTPException(404, 'Post not found')
    if not crud.unlike_post(db, post_id, profile.id):
        raise HTTPException(400, 'Post already unliked')
    return {'detail': 'Post unliked',
            'post_id': post_id,
            'profile_id': profile.id}