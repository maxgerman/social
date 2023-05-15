import logging

from fastapi import Depends, HTTPException, APIRouter, Path, Body, Query
from sqlalchemy.orm.session import Session

import crud
from api.v1.dependencies import get_current_user, super_user
from core.pagination import CustomPage, CustomParams
from db.session import get_db
from models.users import User
from schemas.users import UserUpdateSchema, \
    UserOutWithProfileIdSchema, UserOutSchema, UserActivitySchema

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/', response_model=CustomPage[UserOutSchema])
def get_users(su: User = Depends(super_user), db: Session = Depends(get_db),
              asc: bool = Query(True, description="Sort by ascending order"),
              params: CustomParams = Depends()):
    """Get users by superuser. Pagination."""
    users_page = crud.get_all_users_paginated(db, params=params, asc=asc)
    return users_page


@router.get('/{user_id}', response_model=UserOutWithProfileIdSchema)
def get_user(su: User = Depends(super_user), db: Session = Depends(get_db),
             user_id: int = Path(default=..., gt=0)):
    """Get user by superuser."""
    user, profile_id = crud.get_user_and_profile_id_by_user_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.profile_id = profile_id
    return user


@router.get('/{user_id}/activity', response_model=UserActivitySchema)
def get_user_activity(su: User = Depends(super_user), db: Session = Depends(get_db),
                      user_id: int = Path(default=..., gt=0)):
    """Get user activity by superuser."""
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete('/{user_id}')
def deactivate_user(
        *,
        db: Session = Depends(get_db),
        user_id: int = Path(default=..., gt=0),
        user=Depends(get_current_user),
):
    """Set is_active to False for a user. By the same user or superuser."""
    user_db = crud.get_user_by_id(db, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    if not user_id == user.id and not user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to deactivate this user")

    user_db.is_active = False
    db.add(user_db)
    db.commit()
    return {'deactivated user id': user_id}


@router.patch('/{user_id}', response_model=UserOutSchema)
def update_user(su: User = Depends(super_user),
                db: Session = Depends(get_db),
                user_id: int = Path(default=..., gt=0),
                user_in: UserUpdateSchema = Body(...)):
    """Update user including password (with hashing). Only for superuser."""
    if not user_in.dict(exclude_unset=True):
        raise HTTPException(status_code=400, detail="No data provided")
    user_db = crud.update_user_by_id(db, user_id, user_in)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db
