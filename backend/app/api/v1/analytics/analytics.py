import logging

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

import crud
from api.v1.dependencies import get_current_profile, get_current_user
from core.pagination import CustomParams, CustomPage
from db.session import get_db
from models import Profile, User
from schemas.likes import LikeOutSchema, LikeStatByDayOutSchema

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get('/', response_model=list[LikeStatByDayOutSchema])
def get_like_analytics(*, db: Session = Depends(get_db),
                       user: User = Depends(get_current_user),
                       date_from: str, date_to: str,
                       params: CustomParams = Body(None)):
    """Get likes analytics (count by grouped by day) by authenticated user"""
    try:
        date_from_date, date_to_date = crud.validate_date_range(date_from, date_to)
    except ValueError as e:
        raise HTTPException(400, str(e))
    likes_analytics = crud.get_likes_analytics_query(db, date_from_date, date_to_date)
    return likes_analytics.all()

