import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
from api.v1.dependencies import get_current_profile
from core.pagination import CustomParams, CustomPage
from db.session import get_db
from models import Profile
from schemas.likes import LikeOutSchema

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get('/', response_model=CustomPage[LikeOutSchema])
def get_own_likes(db: Session = Depends(get_db),
                  profile: Profile = Depends(get_current_profile),
                  params: CustomParams = Depends()):
    """Get own likes by authenticated user"""
    likes_query = crud.get_likes_query_by_profile_id(db, profile.id)
    likes_page = crud.paginate_query_by_params(db, likes_query, params)
    return likes_page
