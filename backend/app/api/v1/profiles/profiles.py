import logging

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query, Form
from sqlalchemy.orm import Session

import crud
from api.v1.dependencies import get_current_profile
from core import storage
from core.pagination import CustomParams, CustomPage
from crud import PROFILE_SORTING_TYPE, PROFILE_FILTER_TYPE
from db.session import get_db
from models import Profile
from schemas.profiles import ProfileOutSchema, ProfileUpdateSchema, ProfileOutWithPostsCountSchema

router = APIRouter()
logger = logging.getLogger(__name__)


@router.patch('/', response_model=ProfileOutSchema)
def update_profile(db: Session = Depends(get_db),
                   profile: Profile = Depends(get_current_profile),
                   profile_in: ProfileUpdateSchema = Form()):
    """Update own profile by any user"""
    if not profile_in.dict(exclude_unset=True):
        raise HTTPException(400, 'No data provided')
    profile = crud.update_profile_by_id(db, profile.id, profile_in)
    return profile


@router.get('/me', response_model=ProfileOutWithPostsCountSchema)
def get_own_profile(profile: Profile = Depends(get_current_profile),
                    db: Session = Depends(get_db)):
    """Get own profile by any user"""
    profile.posts_count = crud.get_posts_count_by_profile_id(db, profile.id)
    return profile


@router.get('/', response_model=CustomPage[ProfileOutSchema])
def get_profiles(db: Session = Depends(get_db),
                 sort_by: PROFILE_SORTING_TYPE = Query(default='new'),
                 filter_by: PROFILE_FILTER_TYPE = Query(default='all'),
                 profile: Profile = Depends(get_current_profile),
                 params: CustomParams = Depends(),
                 ):
    all_profiles_sorted_query = crud.query_all_profiles_sorted_by(db, sort_by)
    profiles_filtered_query = crud.filter_profiles_query(all_profiles_sorted_query, filter_by, profile.id)
    profiles_page = crud.paginate_profile_query(db, profiles_filtered_query, params)
    return profiles_page


@router.post('/image', status_code=201)
def upload_profile_image(db: Session = Depends(get_db),
                         file: UploadFile = File(default=...),
                         profile: Profile = Depends(get_current_profile)):
    """Upload profile image for current user/profile"""
    image_uuid = storage.storage_save(db=db, user_id=profile.user_id, file=file)
    if not image_uuid:
        raise HTTPException(500, 'Error uploading image')
    if not crud.set_profile_image_uuid(db, profile.id, image_uuid):
        raise HTTPException(500, 'Error setting profile image')

    return {'message': 'profile image set',
            'profile_id': profile.id,
            'image_uuid': image_uuid}


@router.delete('/image', status_code=200)
def delete_profile_image(db: Session = Depends(get_db),
                         profile: Profile = Depends(get_current_profile)):
    """Delete profile image for current profile"""
    if not crud.delete_profile_image(db, profile.id):
        raise HTTPException(500, 'Error deleting profile image')
    return {'message': 'profile image deleted',
            'profile_id': profile.id}


@router.get('/{profile_id}', response_model=ProfileOutWithPostsCountSchema)
def get_profile(profile_id: int,
                db: Session = Depends(get_db),
                profile: Profile = Depends(get_current_profile)):
    """Get profile by id"""
    profile = crud.get_profile_by_id(db, profile_id)
    if not profile:
        raise HTTPException(404, 'Profile not found')
    profile.posts_count = crud.get_posts_count_by_profile_id(db, profile.id)
    return profile
